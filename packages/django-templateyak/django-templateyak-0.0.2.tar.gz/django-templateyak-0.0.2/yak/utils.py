def monkey_patch_dj_angles():
    from dj_angles.tags import Tag
    from .djangles import map_component

    if getattr(Tag, '_yak_patched', False):
        return

    Tag.original_get_dtt = Tag.get_django_template_tag

    def new_get_dtt(self, *args, **kwargs):
        '''
        Patched by YAK.

        To see the original dj_angles code, refer to `original_get_dtt`
        '''
        if self.django_template_tag is None:
            # Assume any missing template tag is a component
            self.django_template_tag = map_component

        return self.original_get_dtt(*args, **kwargs)

    Tag.get_django_template_tag = new_get_dtt
    Tag._yak_patched = True


def monkey_patch_django_library_class_based_all_the_things():
    import inspect
    from django.template import Library
    from .tags import TemplateTag, SimpleTag, InclusionTag, BlockTag, BlockInclusionTag

    print('applying compete patch')

    def decorate_func(self, func, name=None, base_class=TemplateTag, **tag_kwargs):

        name = name or getattr(func, '__name__')

        def dec(func):

            def render(self, *args, **kwargs):
                return func(*args, **kwargs)

            # Update the signature of `func` to take a leading `self` parameter and assign it to
            # `render`. This will ensure checks on render's signature work as expected
            signature = [*inspect.signature(func).parameters.values()]
            signature.insert(0, inspect.Parameter('self', inspect.Parameter.POSITIONAL_ONLY))
            render.__signature__ = inspect.Signature(signature)

            self.tag(name, base_class.as_tag(
                render=render,
                **tag_kwargs
            ))
            return func

        if func is None:
            # @register.<helper_func>(...)
            return dec
        elif callable(func):
            # @register.<tag_helper>
            return dec(func)
        else:
            raise ValueError("Invalid arguments provided to tag decorator")

    def simple_tag(self, func=None, takes_context=False, name=None):
        return self.decorate_func(func, name=name, base_class=SimpleTag, takes_context=takes_context)

    def inclusion_tag(self, filename, func=None, takes_context=False, name=None):
        return self.decorate_func(func, name=name, base_class=InclusionTag,
                                  takes_context=takes_context, template_name=filename)

    def simple_block_tag(self, func=None, takes_context=False, name=None):
        return self.decorate_func(func, name=name, base_class=BlockTag, takes_context=takes_context)

    def block_inclusion_tag(self, func=None, takes_context=False, name=None):
        return self.decorate_func(func, name=name, base_class=BlockInclusionTag,
                                  takes_context=takes_context)

    Library.decorate_func = decorate_func
    Library.simple_tag = simple_tag
    Library.inclusion_tag = inclusion_tag
    Library.simple_block_tag = simple_block_tag
    Library.block_inclusion_tag = block_inclusion_tag


def monkey_patch_django_library_simple_refactor():
    from inspect import getfullargspec, unwrap
    from functools import wraps
    from django.template.library import InclusionNode, Library, parse_bits, SimpleNode

    print('applying simple patch')

    def decorate_func(self, func=None, takes_context=False, name=None, node_class=SimpleNode,
                      accepts_as=False, filename=False):

        def dec(func):
            (
                params,
                varargs,
                varkw,
                defaults,
                kwonly,
                kwonly_defaults,
                _,
            ) = getfullargspec(unwrap(func))
            function_name = name or func.__name__

            @wraps(func)
            def compile_func(parser, token):
                bits = token.split_contents()[1:]
                target_var = None
                if len(bits) >= 2 and bits[-2] == "as":
                    if accepts_as:
                        target_var = bits[-1]
                        bits = bits[:-2]
                    else:
                        raise ValueError("Invalid argument 'as' provided to tag")

                args, kwargs = parse_bits(
                    parser,
                    bits,
                    params,
                    varargs,
                    varkw,
                    defaults,
                    kwonly,
                    kwonly_defaults,
                    takes_context,
                    function_name,
                )
                node_args = (func, takes_context, args, kwargs)
                if accepts_as:
                    node_args.append(target_var)
                elif filename is not False:
                    node_args.append(filename)
                return node_class(*node_args)

            self.tag(function_name, compile_func)
            return func

        if func is None:
            # @register.<tag_helper>(...)
            return dec
        elif callable(func):
            # @register.<tag_helper>
            return dec(func)
        else:
            raise ValueError("Invalid arguments provided to simple_tag")

    def simple_tag(self, func=None, takes_context=None, name=None):
        return self.decorate_func(func, takes_context=takes_context, name=name, accepts_as=True)

    def inclusion_tag(self, filename, func=None, takes_context=None, name=None, node_class=InclusionNode):
        return self.decorate_func(func, takes_context=takes_context, name=name, filename=filename)
