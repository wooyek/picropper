# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
# from celery import shared_task
from django.contrib import messages
from django.views.debug import CLEANSED_SUBSTITUTE, SafeExceptionReporterFilter
from django.views.generic import View


def show_debug_toolbar(request):
    from debug_toolbar.middleware import show_toolbar
    return show_toolbar(request) or "debug" in request.GET or request.user.is_superuser


# @queueable(max_retries=0, queue="errors")
def django_tasker_err():
    raise Exception(u"Django tasker async task error ążśźęćńół")


# @shared_task(bind=True, max_retries=0, queue="counters", trail=False)
# def celery_err(self):
#     raise Exception(u"Celery async task error ążśźęćńół")


class ErrView(View):
    """Raise an error on purpose to test any health monitoring features"""

    def get(self, request):
        messages.warning(request, u"Error was tested ążźśęćńół")
        # celery_err.delay()
        # django_tasker_err.queue()
        raise Exception(u"Błąd ążśźęćńół")


class SaferExceptionReporterFilter(SafeExceptionReporterFilter):
    def get_traceback_frame_variables(self, request, tb_frame):
        """
        Replaces the values of variables marked as sensitive with
        stars (*********).
        """
        # Loop through the frame's callers to see if the sensitive_variables
        # decorator was used.
        current_frame = getattr(tb_frame, 'f_back', None)
        sensitive_variables = None
        while current_frame is not None:
            if (current_frame.f_code.co_name == 'sensitive_variables_wrapper' and
                    'sensitive_variables_wrapper' in current_frame.f_locals):
                # The sensitive_variables decorator was used, so we take note
                # of the sensitive variables' names.
                wrapper = current_frame.f_locals['sensitive_variables_wrapper']
                sensitive_variables = getattr(wrapper, 'sensitive_variables', None)
                break
            current_frame = current_frame.f_back

        cleansed = {}
        if self.is_active(request) and sensitive_variables:
            if sensitive_variables == '__ALL__':
                # Cleanse all variables
                for name, value in tb_frame.f_locals.items():
                    cleansed[name] = CLEANSED_SUBSTITUTE
            else:
                # Cleanse specified variables
                for name, value in tb_frame.f_locals.items():
                    if name in sensitive_variables:
                        value = CLEANSED_SUBSTITUTE
                    else:
                        value = self.cleanse_special_types(request, value)
                    cleansed[name] = value
        else:
            # Potentially cleanse the request and any MultiValueDicts if they
            # are one of the frame variables.
            for name, value in tb_frame.f_locals.items():
                cleansed[name] = self.cleanse_special_types(request, value)

        if (tb_frame.f_code.co_name == 'sensitive_variables_wrapper' and
                'sensitive_variables_wrapper' in tb_frame.f_locals):
            # For good measure, obfuscate the decorated function's arguments in
            # the sensitive_variables decorator's frame, in case the variables
            # associated with those arguments were meant to be obfuscated from
            # the decorated function's frame.
            cleansed['func_args'] = CLEANSED_SUBSTITUTE
            cleansed['func_kwargs'] = CLEANSED_SUBSTITUTE

        return cleansed.items()
