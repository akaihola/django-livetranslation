from django.templatetags.i18n import *
import new

from livetranslation.markup import TRANSLATION_ITEM_HTML, get_next_counter_value


def wrap_node(node, get_msgid):
    def new_render(self, context):
        singular, plural = get_msgid(context)
        rendered = TRANSLATION_ITEM_HTML % {
            'id': 'livetranslate-%d' % get_next_counter_value(),
            'msgstr': old_render(context),
            'msgid': singular,
            'msgid_plural': plural}
        return rendered

    old_render = node.render
    node.render = new.instancemethod(new_render, node, node.__class__)
    return node


django_do_translate = do_translate

def do_translate(parser, token):
    from django.conf import settings
    node = django_do_translate(parser, token)
    if not getattr(settings, 'LIVETRANSLATION', False):
        return node

    def get_msgid(context):
        return node.filter_expression.resolve(context), u''

    return wrap_node(node, get_msgid)


django_do_block_translate = do_block_translate

def do_block_translate(parser, token):
    from django.conf import settings
    node = django_do_block_translate(parser, token)
    if not getattr(settings, 'LIVETRANSLATION', False):
        return node

    def get_msgid(context):
        return (node.render_token_list(node.singular)[0],
                node.render_token_list(node.plural)[0])

    return wrap_node(node, get_msgid)


register.tag('trans', do_translate)
register.tag('blocktrans', do_block_translate)
