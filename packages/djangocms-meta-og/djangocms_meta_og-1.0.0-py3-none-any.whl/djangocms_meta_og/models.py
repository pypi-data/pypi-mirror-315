from cms.models import Page
from django.conf import settings
from django.db import models
from django_meta_og.models import Content


class PageMetaOg(models.Model):
    meta = models.ManyToManyField(Content)
    language = models.CharField(choices=settings.LANGUAGES, max_length=20)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["language", "page"]]

    def __str__(self):
        if self.page is None:
            title = "Entire website"
            changed_date = ""
            published = f"['{self.language}']"
        else:
            title = str(self.page)
            changed_date = self.page.changed_date
            published = str(self.page.get_published_languages())
        return f'{self.language} "{title}" {published} {changed_date}'.strip()
