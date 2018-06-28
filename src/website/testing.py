# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

# This file mainly exists to allow python setup.py test to work.
import logging
import os
import sys

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.info('Loading %s', __name__)

DJANGO_SETTINGS_MODULE = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings.testing")
logging.info("DJANGO_SETTINGS_MODULE=%s", DJANGO_SETTINGS_MODULE)


def run_tests():
    import django
    django.setup()

    from django.conf import settings
    from django.test.utils import get_runner
    test_runner = get_runner(settings)
    logging.debug("test_runner: %s", test_runner)
    logging.debug("os.getcwd(): %s", os.getcwd())

    # test_dir = os.path.dirname(os.path.dirname(__file__))
    # sys.path.insert(0, test_dir)
    # logging.debug("test_dir: %s" % test_dir)

    # failures = test_runner([], verbosity=1, interactive=True).run_tests(test_labels=test_dir)
    for path in sys.path:
        logging.debug("sys.path: %s", path)
    failures = test_runner().run_tests(['src'])
    logging.debug("failures: %s", failures)
    sys.exit(failures)


if __name__ == '__main__':
    run_tests()
