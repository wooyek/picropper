# coding=utf-8
# Created 2014 by Janusz Skonieczny


def trace_disabled_loggers():  # pragma: no cover
    # http://stackoverflow.com/a/28694704/260480
    import logging
    import sys

    def get_disabled(self):
        return self._disabled

    def set_disabled(self, disabled):
        # noinspection PyProtectedMember
        frame = sys._getframe(1)
        if disabled:
            print('{}:{} disabled the {} logger'.format(
                frame.f_code.co_filename, frame.f_lineno, self.name))
        self._disabled = disabled

    logging.Logger.disabled = property(get_disabled, set_disabled)
