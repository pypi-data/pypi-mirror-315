# Copyright © 2009-2022 Jakub Wilk <jwilk@jwilk.net>
# Copyright © 2022-2024 FriedrichFroebel
#
# This file is part of ocrodjvu.
#
# ocrodjvu is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# ocrodjvu is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

import codecs
import glob
import html
import locale
import os
import re
import shlex
import sys
import warnings

from ocrodjvu.engines import common
from ocrodjvu import errors
from ocrodjvu import image_io
from ocrodjvu import ipc
from ocrodjvu import iso639
from ocrodjvu import temporary
from ocrodjvu import text_zones
from ocrodjvu import utils


const = text_zones.const

_LANGUAGE_PATTERN = re.compile('^([a-z]{3})(?:[-_]([a-z]+))?$')
_ERROR_PATTERN = re.compile(
    r"^(Error openn?ing data|Unable to load unicharset) file (?P<dir>/.*)/nonexistent[.](?P<ext>[a-z]+)$",
    re.MULTILINE
)

_BBOX_EXTRAS_TEMPLATE = '''\
<!-- The following script was appended to hOCR by ocrodjvu for internal purposes. -->
<script type='application/x-ocrodjvu-tesseract'>
//<![CDATA[
{0}
//]]>
</script>
'''


def _filter_boring_stderr(stderr):
    if not stderr:
        return
    if stderr[0].startswith('Tesseract Open Source OCR Engine'):
        # Tesseract prints its own name on standard error even if nothing went wrong.
        del stderr[0]
    if stderr and stderr[0] == 'Page 1':
        # We also don't want page numbers, because we always pass just a single page to Tesseract.
        del stderr[0]


def _wait_for_worker(worker):
    stderr = codecs.getreader(sys.stderr.encoding or locale.getpreferredencoding())(worker.stderr)
    stderr = stderr.read().splitlines()

    def print_errors():
        for line in stderr:
            print(f'tesseract: {line}', file=sys.stderr)

    try:
        worker.wait()
    except Exception:
        print_errors()
        raise
    _filter_boring_stderr(stderr)
    print_errors()


def fix_html(s):
    """
    Work around buggy hOCR output:
    https://groups.google.com/d/topic/tesseract-issues/AdZhdGFkTrA
    """
    regex = re.compile(
        r'''
        ( <[!/]?[a-z]+(?:\s+[^<>]*)?>
        | <!--.*?-->
        | (?<= // ) <!\[CDATA\[
        | (?<= //]] ) >
        | &[a-z]+;
        | &[#][0-9]+;
        | &[#]x[0-9a-f]+;
        | [^<>&]+
        )
        ''', re.IGNORECASE | re.VERBOSE | re.DOTALL
    )
    return ''.join(
        chunk if n & 1 else html.escape(chunk)
        for n, chunk in enumerate(regex.split(s))
    )


class ExtractSettings:

    def __init__(self, rotation=0, page_size=None, **kwargs):
        self.rotation = rotation
        self.page_size = page_size


class Engine(common.Engine):
    name = 'tesseract'
    image_format = image_io.TIFF
    needs_utf8_fix = True

    executable = utils.Property('tesseract')
    extra_args = utils.Property([], shlex.split)
    use_hocr = utils.Property(None, int)
    fix_html = utils.Property(0, int)

    def __init__(self, *args, **kwargs):
        common.Engine.__init__(self, **kwargs)
        try:
            self._directory, self._extension = self.get_filesystem_info()
        except errors.UnknownLanguageListError:
            raise errors.EngineNotFoundError(self.name)
        if self.use_hocr is None:
            self.use_hocr = self._extension == 'traineddata'
        if self.use_hocr:
            # Import hocr late, so that lxml is imported only when needed.
            from ocrodjvu import hocr
            self._hocr = hocr
        else:
            self._hocr = None
        self._user_to_tesseract = None  # To be defined later.
        self._languages = list(self._get_languages())

    def get_filesystem_info(self):
        try:
            with ipc.Subprocess(
                    [self.executable, '', '', '-l', 'nonexistent'],
                    stdin=ipc.DEVNULL,
                    stdout=ipc.DEVNULL,
                    stderr=ipc.PIPE,
            ) as tesseract:
                stderr = codecs.getreader(sys.stdout.encoding or locale.getpreferredencoding())(tesseract.stderr)

                try:
                    stderr = stderr.read()
                    match = _ERROR_PATTERN.search(stderr)
                    if match is None:
                        raise errors.UnknownLanguageListError
                    directory = match.group('dir')
                    extension = match.group('ext')
                    if not os.path.isdir(directory):
                        raise errors.UnknownLanguageListError
                finally:
                    try:
                        tesseract.wait()
                    except ipc.CalledProcessError:
                        pass
                    else:
                        # This should never happen. Recognizing non-existent image
                        # should always fail. But apparently there are Subversion
                        # snapshots of Tesseract in the wild that do it wrongly. Rather
                        # than failing hard, issue a warning:
                        warnings.warn('unexpected exit code from Tesseract', category=RuntimeWarning, stacklevel=2)
        except OSError:
            raise errors.UnknownLanguageListError

        return directory, extension

    def list_languages(self):
        return iter(self._languages)

    def _get_languages(self):
        self._user_to_tesseract = {}
        wildcard = f'*.{self._extension}'
        for filename in glob.iglob(os.path.join(self._directory, wildcard)):
            filename = os.path.basename(filename)
            code = os.path.splitext(filename)[0]
            if code == 'osd':
                continue
            try:
                iso_code = self.user_to_iso639(code)
            except errors.InvalidLanguageIdError:
                continue
            self._user_to_tesseract[iso_code] = code
            yield iso_code

    @classmethod
    def user_to_iso639(cls, language):
        match = _LANGUAGE_PATTERN.match(language)
        if match is None:
            return language
        iso_code = iso639.b_to_t(match.group(1))
        if match.group(2) is not None:
            iso_code += '-' + match.group(2)
        return iso_code

    def user_to_tesseract(self, language):
        result = []
        for sub_lang in language.split('+'):
            iso_code = self.user_to_iso639(sub_lang)
            try:
                tesseract_code = self._user_to_tesseract[iso_code]
            except LookupError:
                raise errors.MissingLanguagePackError(iso_code)
            result += [tesseract_code]
        return str.join('+', result)

    def check_language(self, language):
        self.user_to_tesseract(language)

    def recognize_plain_text(self, image, language, details=None, uax29=None):
        language = self.user_to_tesseract(language)
        with temporary.directory() as output_dir:
            with ipc.Subprocess(
                    [self.executable, image.name, os.path.join(output_dir, 'tmp'), '-l', language] + self.extra_args,
                    stdin=ipc.DEVNULL,
                    stdout=ipc.DEVNULL,
                    stderr=ipc.PIPE,
            ) as worker:
                _wait_for_worker(worker)
            with open(os.path.join(output_dir, 'tmp.txt'), 'rt') as file:
                return common.Output(
                    file.read(),
                    format_='txt',
                )

    def recognize_hocr(self, image, language, details=text_zones.TEXT_DETAILS_WORD, uax29=None):
        language = self.user_to_tesseract(language)
        character_details = details < text_zones.TEXT_DETAILS_WORD or (uax29 and details <= text_zones.TEXT_DETAILS_WORD)
        with temporary.directory() as output_dir:
            tessconf_path = os.path.join(output_dir, 'tessconf')
            with open(tessconf_path, 'wt') as tessconf:
                # Tesseract 3.00 does not come with any config file to enable hOCR
                # output. Let's create our own one.
                print('tessedit_create_hocr T', file=tessconf)
            commandline = [
                self.executable, image.name, os.path.join(output_dir, 'tmp'),
                '-l', language
            ] + self.extra_args + [tessconf_path]
            if character_details:
                commandline += ['makebox']
            with ipc.Subprocess(
                    commandline,
                    stdin=ipc.DEVNULL,
                    stdout=ipc.DEVNULL,
                    stderr=ipc.PIPE,
            ) as worker:
                _wait_for_worker(worker)
            hocr_path = os.path.join(output_dir, 'tmp.hocr')
            if not os.path.exists(hocr_path):
                hocr_path = hocr_path[:-4] + 'html'
            with open(os.path.join(output_dir, hocr_path), 'r') as hocr_file:
                contents = hocr_file.read()
            if character_details:
                assert commandline[-1] == 'makebox'
                assert commandline[-2] == tessconf_path
                box_path = os.path.join(output_dir, 'tmp.box')
                if not os.path.exists(box_path):
                    # Tesseract << 3.04
                    del commandline[-2]
                    with ipc.Subprocess(
                            commandline,
                            stdin=ipc.DEVNULL,
                            stdout=ipc.DEVNULL,
                            stderr=ipc.PIPE,
                    ) as worker:
                        _wait_for_worker(worker)
                with open(box_path, 'r') as box_file:
                    contents = contents.replace(
                        '</body>',
                        _BBOX_EXTRAS_TEMPLATE.format(box_file.read()) + '</body>'
                    )
        if self.fix_html:
            contents = fix_html(contents)
        return common.Output(
            contents,
            format_='html',
        )

    def recognize(self, image, language, details=None, uax29=None):
        if self._hocr is None:
            f = self.recognize_plain_text
        else:
            f = self.recognize_hocr
        return f(image, language, details=details, uax29=uax29)

    def extract_text(self, stream, **kwargs):
        if self._hocr is not None:
            return self._hocr.extract_text(stream, **kwargs)
        settings = ExtractSettings(**kwargs)
        bbox = text_zones.BBox(*((0, 0) + settings.page_size))
        text = stream.read()
        zone = text_zones.Zone(const.TEXT_ZONE_PAGE, bbox, [text])
        zone.rotate(settings.rotation)
        return [zone.sexpr]
