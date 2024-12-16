from cms.models import Page
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_meta_og.models import Content


class PageMetaOg(models.Model):
    meta = models.ManyToManyField(Content)
    language = models.CharField(choices=settings.LANGUAGES, max_length=20)
    page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text=_("A Meta without a page will be used for the entire site."),
    )

    class Meta:
        unique_together = [["language", "page"]]

    def __str__(self):
        return str(_("Entire website") if self.page is None else self.page)
