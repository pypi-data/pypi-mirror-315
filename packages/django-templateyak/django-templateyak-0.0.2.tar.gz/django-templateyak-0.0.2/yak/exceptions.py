from django.template.exceptions import TemplateSyntaxError


class UnsetSlot(Exception):
    pass


class WithNotSupported(TemplateSyntaxError):
    pass


class AssignmentNotSupported(TemplateSyntaxError):
    pass
