from django.db import models
from drfaddons.models import CreateUpdateModel
from django.utils.text import gettext_lazy as _


class ApiToken(CreateUpdateModel):
    title = models.CharField(verbose_name=_("Title"), max_length=60, null=True, blank=True)
    token = models.CharField(verbose_name=_("API Token"), max_length=30, unique=True)
    is_active = models.BooleanField(verbose_name=_("Is Active?"), default=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = _('API Token')
        verbose_name_plural = _('API Tokens')
