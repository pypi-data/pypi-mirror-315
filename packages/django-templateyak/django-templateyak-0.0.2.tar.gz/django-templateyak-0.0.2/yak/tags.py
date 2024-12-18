from copy import copy
from inspect import getfullargspec, unwrap
import os
from uuid import uuid4

from django.template import Node, NodeList
from django.template.library import InclusionNode as DjangoInclusion, SimpleNode as DjangoSimple
from django.utils.functional import cached_property

from django.template.library import parse_bits

from .exceptions import WithNotSupported, AssignmentNotSupported


class AssignmentNodeMixin(Node):
    '''
    Provides uniformity on how subclasses handle context assignment (`as target_var`)
    '''

    def render(self, context):
        rendered = super().render(context)
        if self.template_tag and self.template_tag.target_var:
            context[self.template_tag.target_var] = rendered
            return ''
        return rendered


class InclusionNode(AssignmentNodeMixin, DjangoInclusion):
    '''
    Django InclusionNode subclass with support for:
        - context assignment
        - dynamic template file assignation
    '''

    unresolved = None
    template_base = None

    def sanitize_filename(self):
        if not self.filename.endswith('.html'):
            self.filename = self.filename.replace('.', os.path.sep).replace('-', '_')
            self.filename = f'{self.filename}.html'

    def resolve_filename(self, context):
        if hasattr(self.filename, 'resolve'):
            # filename is a `FilterExpression` and needs to be resolved
            self.unresolved = self.filename

        if not self.unresolved:
            return

        self.filename = copy(self.unresolved).resolve(context)
        self.sanitize_filename()

        if self.template_base:
            self.filename = os.path.join(self.template_base, self.filename)

    def render(self, context):
        '''
        resolves the template filename and adapt the cache mechanism for supporting
        different filenames
        '''

        self.resolve_filename(context)
        context_cache = context.render_context.get(self, dict())
        context.render_context[self] = context_cache.get(self.filename)

        rv = super().render(context)

        context_cache[self.filename] = context.render_context.get(self)
        context.render_context[self] = context_cache

        return rv


class SimpleNode(AssignmentNodeMixin, DjangoSimple):
    '''
    Django SimpleNode subclass that supports context assignment through
    AssignmentNodeMixin
    '''
    pass


class NodeListRenderer(Node):
    '''
    Helper Node to wrap a NodeList with a Node. Its role is to make syntax uniform.

    It is used to make a NodeList renderable as a single Node.
    It also keeps track of the parent tag uuid if available
    '''

    def __init__(self, nodelist, uuid=None):
        self.nodelist = nodelist
        self.parent_uuid = uuid

    def render(self, context):
        # replace _parent_uuid in context and keep track of the previous one
        if '_parent_uuid' in context:
            prev_uuid = context['_parent_uuid']
        else:
            prev_uuid = None
        context['_parent_uuid'] = self.parent_uuid

        rv = self.nodelist.render(context)

        # reset _parent_uuid to its previous value
        if prev_uuid:
            context['_parent_uuid'] = prev_uuid
        else:
            del context['_parent_uuid']

        return rv


class TemplateTag:
    '''
    Base class for class-based templatetags.
    '''

    is_block_node = False
    accepts_with_context = False

    nodelist = None
    template_name = None
    with_context = None
    allow_as = True

    _init_args = tuple()

    @property
    def node_class(self):
        '''
        Automatically deduces whether to use a SimpleNode or InclusionNode.

        You might want to override this with a simple attribute in your subclasses.

        If using a custom node class, it should accept the following:
            - a render method (`self.render`)
            - a takes_context boolean
            - a list (`args`)
            - a dict (`kwargs`)
            - a template name or `None`
        '''
        return SimpleNode if self.template_name is None else InclusionNode

    @property
    def takes_context(self):
        '''
        Whether or not this TemplateTag takes the template context.

        This is deduced by inspecting the `render` method and looking at the name of its first arg.
        '''
        params = self._arg_spec[0]
        if len(params) > 0 and params[0] == 'context':
            return True
        return False

    @cached_property
    def _arg_spec(self):
        '''
        Cached property storing the argspec of the `render` method
        '''
        return self.get_arg_spec(self.render)

    @classmethod
    def get_arg_spec(cls, func, discard_self=True):
        ((_discarded_self, *params), varargs, varkw, defaults, kwonly, kwonly_defaults, _,) \
            = getfullargspec(unwrap(func))
        if not discard_self:
            params = (_discarded_self, *params)
        return params, varargs, varkw, defaults, kwonly, kwonly_defaults

    @cached_property
    def uuid(self):
        return str(uuid4())

    def clean_bits(self, bits):
        '''
        Called during tag parsing to extract the "bits"
        (raw pieces of the template string inside `{%` `%}`)

        This method **modifies** `bits`
        '''
        self.clean_as(bits)
        self.clean_with(bits)

    def clean_as(self, bits):
        '''
        Removes `as` keyword if present and store the `target_var` on the `TemplateTag`
        '''
        if len(bits) >= 2 and bits[-2] == "as":
            if not self.allow_as:
                raise AssignmentNotSupported(f'{self.__class__.__name__} does not support "as"')

            self.target_var = bits[-1]
            del bits[-2:]

    def clean_with(self, bits):
        '''
        Removes `with` keyword if present and store the `with_context`, a list of keyword arguments,
        on the `TemplateTag` for later evaluation.
        '''
        if self.accepts_with_context:
            if 'with' not in bits:
                return
            pos = bits.index('with')

            if pos == len(bits) + 1:
                raise WithNotSupported(f'missing assignements after "with" in {self.__class__.__name__}')

            _, self.with_context = parse_bits(self.parser, bits[pos + 1:],
                                              [], None, 'with_context', None, [], {},  # fake argspec
                                              False, f'{self.__class__.__name__}.render - with_context')
            del bits[pos:]
        elif 'with' in bits:
            raise WithNotSupported(self.__class__.__name__)

    def _get_args_kwargs(self, parser, token):
        '''
        Helper method to map template string bits to args and kwargs
        that will be passes to the `render` method.

        `parse_bits` is imported from Django.
        '''
        bits = token.split_contents()[1:]
        self.target_var = None

        self.clean_bits(bits)

        args, kwargs = parse_bits(parser, bits,
                                  *self._arg_spec,
                                  self.takes_context, f'{self.__class__.__name__}.render')

        return args, kwargs

    def get_with_context(self, context):
        '''
        Evaluates the content of `with_context` before returning it
        '''
        if self.with_context is None:
            return dict()
        return {k: v.resolve(context) for k, v in self.with_context.items()}

    def tag_extract(self, token):
        return token.contents.split(' ', 1)[0]

    def deduce_end_tag(self, token):
        return f'end{self.tag_extract(token)}'

    def parse(self, args, kwargs, nodelist=None, end_token=None):
        '''
        Called at parsing time after collecting the internal nodelist if applicable.

        You might want to override this for eg storing the nodelist in the context
        or a template partial.
        '''
        self.nodelist = nodelist

    def render(self):
        '''
        This is the only method you probably need to override.

        If you require the template contex, accept `context` as first argument
        (eg `def render(self, context):`).

        The arguments of this method will be automatica
        '''
        pass

    def get_node_last_arg(self):
        '''
        Called upon when creating the `Node` (as specified by `node_class`).
        Django's `SimpleNode` and `InclusionNode` have different signature.

        This method returns the `template_name` (therefore `None` if no `template_name` was defined)

        `SimpleNode` accepts `target_var` as last arg
        (we are setting this using `AssignmentNodeMixin` instead)
        while `InclusionNode` a template name.
        '''
        return self.template_name

    def handle_end_token(self, token):
        '''
        Doesn't do anything by default with the end or closing token.

        You might want to override if eg your non-inclusion `TemplateTag`
        wraps its contents in a `<div>`
        '''
        pass

    def get_node_args_kwargs(self, args, kwargs):
        return (
            self.render,
            self.takes_context,
            args,
            kwargs,
            self.get_node_last_arg()
        ), dict()

    def __call__(self, parser, token):
        '''
        - gets (unevaluated) `args` and `kwargs` from the token string
        - collects internal nodes into `nodelist` if this is a block tag
        - passes `args`, `kwargs` and eventual `nodelist` and `end_token` to the `parse` method
        - creates and returns the render `Node`
        '''
        self.parser = parser

        # args and kwargs will respectively be a list and a dict of `FilterExpression`s
        args, kwargs = self._get_args_kwargs(parser, token)

        if self.is_block_node:
            nodelist = NodeList()
            nodelist.must_be_first = False
            end_tag = self.deduce_end_tag(token)

            # Read and tokenize the template until we encounter the corresponding endtag.
            parser.extend_nodelist(
                nodelist,
                NodeListRenderer(parser.parse([end_tag]), self.uuid),
                token
            )
            end_token = parser.next_token()

        else:
            nodelist = None
            end_token = None

        self.parse(args, kwargs, nodelist, end_token)

        node_args, node_kwargs = self.get_node_args_kwargs(args, kwargs)
        # TODO: check this isn't an issue for GC
        self.node = self.node_class(*node_args, **node_kwargs)
        self.node.template_tag = self
        return self.node

    @classmethod
    def as_tag(cls, *args, **kwargs):
        '''
        Class method used to create a templatetag function.
        Similar to `as_view` on class-based views
        '''
        def func(parser, token):
            return cls(*args, **kwargs)(parser, token)
        func.__name__ = cls.__name__.lower()

        return func

    def __init__(self, **kwargs):
        '''
        Do not call directly. Use `as_tag` instead.

        Any `kwarg` passed to this method will be mapped and assigned
        to an attribute or method on the object.
        This is useful if you'd like to avoid subclassing.
        '''
        for attr, val in kwargs.items():
            if not hasattr(self, attr):
                raise AttributeError(f'{self.__class__.__name__} received unknown parameter "{attr}"')

            setattr(self, attr, val)

        # stores initial kwargs, this will be needed for handling nested similar tags
        self._init_kwargs = kwargs


# Specific classes corresponding to current Django `Library` helper methods (and more)


class SimpleTag(TemplateTag):
    node_class = SimpleNode


class InclusionTag(TemplateTag):
    node_class = InclusionNode

    def __call__(self, parser, token):
        assert self.template_name is not None, 'InclusionTag requires a "template_name" attribute'
        return super().__call__(parser, token)


class BlockTag(SimpleTag):
    is_block_node = True


class BlockInclusionTag(BlockTag, InclusionTag):
    pass
