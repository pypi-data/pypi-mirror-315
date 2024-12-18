from .tags import TemplateTag, InclusionNode
from .exceptions import UnsetSlot


class Komponent(TemplateTag):
    '''
    Block-type `TemplateTag` similar in every other aspect to
    Django's `{% include %}` tag.
    '''

    is_block_node = True
    node_class = InclusionNode  # Forcing this as the template_name is unknown at first
    accepts_with_context = True

    def clean_bits(self, bits):
        '''
        Stores the `FilterExpression` representing the template name during parsing.
        This expression will have be evaluated by the `Node` at render time.
        '''
        super().clean_bits(bits)
        self.template_name = self.parser.compile_filter(bits.pop(0))

    def render(self, context):
        '''
        Stores the rendered contents of the internal node list in the context as `yield`
        alongside with any evaluted `with_context`.

        A convenience `has_block` variable is also set to represent whether or not
        there is something in `yield`.
        '''

        slot_content = self.nodelist.render(context)

        return {
            **context.flatten(),
            **self.get_with_context(context),
            '_parent_uuid': self.uuid,
            'yield': slot_content,
            'has_block': len(slot_content.strip()) > 0,
        }


class SlotBase(TemplateTag):
    '''
    Base class used by slot classes in this module.

    It provides helper methods to store slots contents in the context
    '''

    def get_component_uuid(self, context):
        return context.get('_parent_uuid', None)

    def set_named_slot(self, context, uuid, name, value):
        if '_slots' not in context:
            context['_slots'] = dict()
        if uuid not in context['_slots']:
            context['_slots'][uuid] = dict()
        context['_slots'][uuid][name] = value

    def get_named_slot(self, context, uuid, name):
        if '_slots' not in context or uuid not in context['_slots'] or name not in context['_slots'][uuid]:
            raise UnsetSlot(f'{uuid} - {name}')
        return context['_slots'][uuid][name]


class Slot(SlotBase):
    '''
    `TemplateTag` representing named overridable chunks of a `Komponent`
    '''

    name = None
    is_block_node = True

    def get_nodelist(self, context):
        '''
        If a node list has been stored in the context under the name of this slot,
        use that, otherwise use the internal nodelist
        '''
        try:
            c_uuid = self.get_component_uuid(context)
            return self.get_named_slot(context, c_uuid, self.name)
        except UnsetSlot:
            return self.nodelist

    def render(self, context, _name):
        '''
        renders the nodelist retuned by `get_nodelist`
        '''
        self.name = _name

        nodelist = self.get_nodelist(context)
        return nodelist.render(context)


class ContentForSlot(SlotBase):
    '''
    `TemplateTag` used to override the default content of a `Slot`
    '''

    is_block_node = True

    def render(self, context, _name):
        '''
        Stores the internal node list inside the context for use by `Slot`
        '''
        c_uuid = self.get_component_uuid(context)
        self.set_named_slot(context, c_uuid, _name, self.nodelist)
        return ''
