# coding=utf-8
# Copyright 2014 Janusz Skonieczny

from os.path import normcase

CSS = (
    "assets/css/bootstrap4.css",
    "assets/css/font-awesome4.css",
    "assets/css/screen.css",
)

JS = (
    "assets/js/jquery.js",
    "assets/js/bootstrap.js",
    "assets/js/main.js",
)

import sys  # noqa: E402 isort:skip

if sys.platform == 'win32':
    JS = [normcase(f) for f in JS]
    # IE_JS = [normcase(f) for f in IE_JS]
    CSS = [normcase(f) for f in CSS]

from django_assets import Bundle, register  # noqa: E402 isort:skip

register('js', Bundle(*JS, filters='yui_js', output='script.%(version)s.js'))
register('css', Bundle(*CSS, filters='yui_css', output='style.%(version)s.css'))
