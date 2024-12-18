import warnings

from django.conf import settings
from django.template import Library, defaulttags
from django.template.exceptions import TemplateSyntaxError
from django.utils.html import escape, format_html
from django.utils.lorem_ipsum import paragraphs, words
from django.utils.safestring import mark_safe

from ..tags import TemplateTag


register = Library()


class NoArgsNodeTag(TemplateTag):
    def get_node_args_kwargs(self, args, kwargs):
        return tuple(), dict()

    def render(self):
        pass


class AutoEscape(TemplateTag):
    is_block_node = True
    is_on = None

    def clean_bits(self, bits):
        super().clean_bits(bits)
        self.clean_on_off_bit(bits)

    def clean_on_off_bit(self, bits):
        if len(bits) != 1:
            raise TemplateSyntaxError("'autoescape' tag requires exactly one argument.")
        bit = bits.pop(0)
        if bit not in ('on', 'off'):
            raise TemplateSyntaxError("'autoescape' argument should be 'on' or 'off'")
        self.is_on = (bit == 'on')

    def render(self, context):
        inside = self.nodelist.render(context)
        if self.is_on:
            inside = escape(inside)
        return inside


class CsrfToken(TemplateTag):
    def render(self, context):
        csrf_token = context.get("csrf_token")
        if csrf_token:
            if csrf_token == "NOTPROVIDED":
                return ""
            else:
                return format_html(
                    '<input type="hidden" name="csrfmiddlewaretoken" value="{}">',
                    csrf_token,
                )
        else:
            # It's very probable that the token is missing because of
            # misconfiguration, so we raise a warning
            if settings.DEBUG:
                warnings.warn(
                    "A {% csrf_token %} was used in a template, but the context "
                    "did not provide the value.  This is usually caused by not "
                    "using RequestContext."
                )
            return ""


class Debug(NoArgsNodeTag):
    node_class = defaulttags.DebugNode


class FirstOf(TemplateTag):
    def render(self, *args):
        for var in args:
            if var:
                return var


class OriginalLorem(TemplateTag):

    common = True
    method = 'b'

    def clean_bits(self, bits):
        super().clean_bits(bits)
        self.clean_random_bit(bits)
        self.clean_method_bit(bits)

    def clean_random_bit(self, bits):
        if bits[-1] == "random":
            self.common = False
            bits.pop()

    def clean_method_bit(self, bits):
        if bits[-1] in ("w", "p", "b"):
            self.method = bits.pop()

    def render(self, count):
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = 1
        if self.method == "w":
            return words(count, common=self.common)
        else:
            paras = paragraphs(count, common=self.common)
        if self.method == "p":
            paras = ["<p>%s</p>" % p for p in paras]
        return mark_safe("\n\n".join(paras))


class YakLorem(TemplateTag):

    def render(self, count, method='b', random=False):
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = 1
        if method == "w":
            return words(count, common=not random)
        else:
            paras = paragraphs(count, common=not random)
        if method == "p":
            paras = ["<p>%s</p>" % p for p in paras]
        return mark_safe("\n\n".join(paras))


# Usage: {% autoescape on %}...{% endautoescape %}
register.tag(AutoEscape.as_tag())

# Usage: {% csrf_token %}
register.tag('csrf_token', CsrfToken.as_tag())

# Usage: {% debug %}
register.tag(Debug.as_tag())

# Usage: {% firstof var1 var2 ... varn %}
register.tag(FirstOf.as_tag())

# Usage: {% lorem int_or_var %}{% lorem 4 w %}{% lorem 5 p random %}
register.tag('lorem', OriginalLorem.as_tag())

# Usage: {% lorem_var_enabled int_or_var %}{% lorem_var_enabled 4 string_or_var %}
#   {% lorem_var_enabled 5 'p' random=boolean_or_var %}
register.tag('lorem_var_enabled', YakLorem.as_tag())
