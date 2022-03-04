from django.db import models
from django.utils.text import gettext_lazy as _


class Product(models.Model):
    serial_no = models.CharField(verbose_name=_("Serial Number"), max_length=30, unique=True)
    part_no = models.CharField(verbose_name=_("Part Number"), max_length=30)
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    model = models.CharField(verbose_name=_("Model"), max_length=40)
    screen_size = models.CharField(verbose_name=_("Screen Size"), max_length=50)
    color = models.CharField(verbose_name=_("Color"), max_length=50)
    is_emi = models.BooleanField(verbose_name=_("Is EMI?"), default=False)
    is_blocked = models.BooleanField(verbose_name=_("Is Blocked?"), default=False)
    create_date = models.DateTimeField(_('Create Date/Time'), auto_now_add=True)
    update_date = models.DateTimeField(_('Date/Time Modified'), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        unique_together = ('serial_no', 'part_no')
