from cms.utils import get_current_site
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import PageMetaOg


class PageField(ModelChoiceField):
    def label_from_instance(self, page) -> str:
        title = str(page)
        if not title and hasattr(settings, "CMS_CONFIRM_VERSION4") and settings.CMS_CONFIRM_VERSION4:
            title = str(page.pagecontent_set(manager="admin_manager").last().title)
        return title


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
    ordering = ["page", "language"]
    list_display = ["view_page", "language"]

    def view_page(self, obj):
        return str(obj)

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
            page = form.base_fields["page"]
            if hasattr(settings, "CMS_CONFIRM_VERSION4") and settings.CMS_CONFIRM_VERSION4:
                queryset = page.queryset.filter(node__site=self.get_site(request))
            else:
                queryset = page.queryset.filter(node__site=self.get_site(request), publisher_is_draft=True)
            form.base_fields["page"] = PageField(queryset=queryset, help_text=page.help_text)
        return form
