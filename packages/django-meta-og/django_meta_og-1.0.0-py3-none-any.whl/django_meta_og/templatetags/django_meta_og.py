from django import template

from django_meta_og.models import Content

register = template.Library()


@register.simple_tag()
def django_meta_og_prefix():
    return "\n".join(
        {f"{meta.property.namespace.prefix}: {meta.property.namespace.uri}" for meta in Content.objects.all()}
    )
