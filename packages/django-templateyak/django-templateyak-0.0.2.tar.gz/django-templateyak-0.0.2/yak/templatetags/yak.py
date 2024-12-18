from django.template import Library, Node, NodeList

from ..component import Komponent, Slot, ContentForSlot


register = Library()

register.tag('component', Komponent.as_tag())
register.tag(Slot.as_tag())
register.tag('slotvalue', ContentForSlot.as_tag())
