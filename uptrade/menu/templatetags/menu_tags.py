from django import template
from menu.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    all_items = MenuItem.objects.select_related('parent').prefetch_related('children').all()
    items = {item.id: item for item in all_items}

    # Отрисовка меню
    def render(item, is_active):
        sub_menu = ''.join(render(child, request.path == child.get_absolute_url()) for child in item.children.all())
        return f'<li class="{"active" if is_active else ""}">{item.name}{sub_menu}</li>'

    root_items = [item for item in all_items if item.parent is None]
    menu = ''.join(render(item, request.path == item.get_absolute_url()) for item in root_items)
    return f'<ul>{menu}</ul>'

