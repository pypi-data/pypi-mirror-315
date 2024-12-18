from dj_angles.settings import get_setting


class KomponentMapper:
    '''
    Mapper class for component tags.
    '''

    open_tags = []

    map_to = 'component'
    default_tag = 'component'

    def __init__(self, **kwargs):
        for attr, val in kwargs.items():
            if not hasattr(self, attr):
                raise AttributeError(f'{self.__class__.__name__} received unknown parameter "{attr}"')

            setattr(self, attr, val)

    @property
    def default_prefix(self):
        return get_setting('prefix', 'dj-')

    def get_opening_tag(self, tag):
        return self.map_to

    def get_closing_tag(self, tag):
        return f'end{self.map_to}'

    def get_og_tag(self, tag):
        '''use the component's name as html tag if tag_name is the generic component tag'''
        if tag.tag_name == self.default_tag:
            return tag.attributes[0]
        return tag.tag_name

    def get_tag_attributes(self, tag):
        '''strip the first attribute if tag_name is the generic component tag'''
        if tag.tag_name == self.default_tag:
            return tag.attributes[1:]
        return tag.attributes

    def get_tag(self, og_tag):
        '''returns a string or {{}} expression that will evaluate to the tag'''
        return self.adapt_tag_attr_value(og_tag)

    def get_closing_lst(self, tag):
        return ['</', tag, '>']

    def __call__(self, tag):
        angles_tag = tag
        wrap_tag = get_setting('wrap_tags', False)

        if angles_tag.is_end:
            # Closing tag
            # we first close the component call
            # we know what the closing tag should be because we stored it we we opened the tag
            tag = self.__class__.open_tags.pop()
            rv_lst = ['{% ', self.get_closing_tag(angles_tag), ' %}']

            if wrap_tag:
                # then add the closing html tag if necessary
                rv_lst.extend(self.get_closing_lst(tag))

            rv = ''.join(rv_lst)
            return rv

        # get the short name of the file to be included
        og_tag = self.get_og_tag(angles_tag)

        if angles_tag.tag_name == self.default_tag:
            # we are dealing with <prefix-component template>
            tag = self.get_tag(og_tag)
        else:
            # we are dealing with <prefix-template>
            tag = og_tag

        args, attrs, updated_tag = self.split_args_attrs(self.get_tag_attributes(angles_tag))
        if updated_tag is None:
            updated_tag = tag
            prefix = True
        else:
            prefix = False

        prefixed_tag = f'{prefix and self.default_prefix or ""}{updated_tag}'
        if not angles_tag.is_self_closing:
            # store the prefixed tag so that we remember it when encountering the closing tag
            self.__class__.open_tags.append(prefixed_tag)

        rv_args = []
        if wrap_tag:
            rv_args.extend([f'<{prefixed_tag}', ' '.join(attrs), '>'])
        rv_args.extend(['{% ', self.get_opening_tag(angles_tag), ' '])

        if angles_tag.tag_name == self.default_tag:
            rv_args.append(self.get_og_tag(angles_tag))
        else:
            rv_args.append(f'"{self.get_og_tag(angles_tag)}"')

        rv_args.extend([' '.join(args), '%}'])

        if angles_tag.is_self_closing:
            rv_args.extend(['{% ', self.get_closing_tag(angles_tag), ' %}'])
            if wrap_tag:
                rv_args.extend(self.get_closing_lst(prefixed_tag))

        rv = ''.join([f'{arg}' for arg in rv_args])
        return rv

    def split_args_attrs(self, attributes):
        '''splits the attributes meant for the wrapping html tag from the templatetag's arguments'''
        html_attrs = ['']
        ttag_args = ['']
        html_tag = None

        for attr in attributes:
            if attr.key.startswith('wrap:'):
                html_attr = attr.key.split(':', 1)[-1]

                if html_attr == 'tag' and attr.has_value:
                    html_tag = self.adapt_tag_attr_value(attr.value)
                    continue

                if not attr.has_value:
                    html_attrs.append(html_attr)
                else:
                    html_attrs.append(''.join([
                        html_attr,
                        '=',
                        self.adapt_tag_attr_value(attr.value, wrap=True)])
                    )
            else:
                ttag_args.append(f'{attr}')

        return ttag_args, html_attrs, html_tag

    def adapt_tag_attr_value(self, value, wrap=False):
        '''
        Use strings as-is but un-quoted.
        Wrap filter expressions in mustaches
        '''
        value = f'{value}'
        if value[0] in ["'", '"'] and value[0] == value[-1]:
            rv = value[1:-1]
        else:
            rv = ''.join(['{{', value, '}}'])

        return f'"{rv}"' if wrap else rv


map_component = KomponentMapper()


mapper = {
    **{tag: tag for tag in ('slot', 'slotvalue')},
    'component': map_component,
}
