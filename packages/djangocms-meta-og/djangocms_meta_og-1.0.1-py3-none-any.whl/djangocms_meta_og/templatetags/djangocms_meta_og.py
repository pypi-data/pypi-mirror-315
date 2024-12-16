from typing import Any

from django import template

from djangocms_meta_og.utils import get_page_meta

register = template.Library()


@register.simple_tag(takes_context=True)
def djangocms_meta_og_prefix(context: dict[str, Any]) -> str:
    request = context["request"]
    current_page = context.get("current_page", getattr(request, "current_page", None))
    if hasattr(current_page, "pk"):
        page_meta = get_page_meta(current_page, request.LANGUAGE_CODE)
        if page_meta is not None:
            return "\n".join(
                {f"{meta.property.namespace.prefix}: {meta.property.namespace.uri}" for meta in page_meta.meta.all()}
            )
    return ""
