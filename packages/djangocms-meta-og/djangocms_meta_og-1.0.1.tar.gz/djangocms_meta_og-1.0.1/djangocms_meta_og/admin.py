from cms.utils import get_current_site
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import PageMetaOg


class PageMetaOgForm(ModelForm):
    class Meta:
        model = PageMetaOg
        exclude = []

    def clean_page(self):
        page = self.cleaned_data["page"]
        if page is None:
            query = PageMetaOg.objects.filter(page__isnull=True)
            if self.instance.pk is not None:
                query &= query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError(_("Page meta OG for entire site with this language already exists."))
        return page


@admin.register(PageMetaOg)
class PageMetaOgAdmin(admin.ModelAdmin):
    form = PageMetaOgForm
    ordering = ["page", "page__changed_date", "language"]
    list_display = ["page", "language"]

    def get_site(self, request):
        site_id = request.session.get("cms_admin_site")
        if not site_id:
            return get_current_site()
        try:
            site = Site.objects._get_site_by_id(site_id)
        except Site.DoesNotExist:
            site = get_current_site()
        return site

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if "page" in form.base_fields:
            queryset = form.base_fields["page"].queryset
            form.base_fields["page"].queryset = queryset.filter(
                node__site=self.get_site(request), publisher_is_draft=True
            )
        return form
