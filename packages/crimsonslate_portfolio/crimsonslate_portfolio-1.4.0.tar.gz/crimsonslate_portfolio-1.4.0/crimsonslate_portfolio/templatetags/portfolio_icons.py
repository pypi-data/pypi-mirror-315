from django.template import Library


register = Library()


@register.inclusion_tag("portfolio/icon.html")
def icon_social_media(name: str, size: int = 6) -> dict[str, str]:
    return {
        "file": f"portfolio/icons/{name.lower()}.svg",
        "size": str(size),
    }
