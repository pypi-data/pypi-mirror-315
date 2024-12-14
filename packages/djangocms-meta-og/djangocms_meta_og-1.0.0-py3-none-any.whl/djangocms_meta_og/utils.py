from typing import Optional

from cms.models import Page

from .models import PageMetaOg


def get_page_meta(current_page: Page, language: str) -> Optional[PageMetaOg]:
    """Get meta OG for current page."""
    try:
        return PageMetaOg.objects.get(page=current_page, language=language)
    except PageMetaOg.DoesNotExist:
        # Load "global" meta without a connected page.
        try:
            return PageMetaOg.objects.get(page__isnull=True, language=language)
        except PageMetaOg.DoesNotExist:
            pass
    return None
