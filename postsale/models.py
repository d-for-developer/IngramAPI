from django.db import models
from django.utils.text import gettext_lazy as _


# Create your models here.
class PostSaleModel(models.Model):
    customer_name = models.CharField(verbose_name=_("Customer Name"), max_length=60, null=True, blank=False)
    customer_email = models.CharField(verbose_name=_("Customer Email"), max_length=60, null=True, blank=False)
    customer_mobile_no = models.CharField(verbose_name=_("Mobile Number"), max_length=12, null=True, blank=False)
    product_name = models.CharField(verbose_name=_("Product Name / Code"), max_length=60, null=True, blank=False)
    assetMake = models.CharField(verbose_name=_("Asset Make"), max_length=60, null=False, blank=False)
    assetModel = models.CharField(verbose_name=_("Asset Model"), max_length=60, null=False, blank=False)
    serialNo = models.CharField(verbose_name=_("Serial No"), max_length=60, null=False, blank=False)
    invoiceDate = models.CharField(verbose_name=_("Invoice Date"), max_length=60, null=False, blank=False)
    invoiceValue = models.CharField(verbose_name=_("Invoice Value"), max_length=60, null=False, blank=False)
    customer_address = models.CharField(verbose_name=_("Customer Address"), max_length=60, null=False, blank=False)
    pin_code = models.CharField(verbose_name=_("Customer Pin code"), max_length=6, null=False, blank=False)
    city = models.CharField(verbose_name=_("City"), max_length=20, null=False, blank=False)
    state = models.CharField(verbose_name=_("State"), max_length=15, null=False, blank=False)
    OA_Plan_name = models.CharField(verbose_name=_("One Assist Plan name"), max_length=60, null=False, blank=False)
    OA_plan_price_paid_by_seller = models.CharField(verbose_name=_("One Assist plan price paid by seller"),
                                                    max_length=60, null=False, blank=False)
    OA_plan_price_to_customer = models.CharField(verbose_name=_("One Assist plan price to customer"), max_length=60,
                                                 null=False, blank=False)
    partner_name = models.CharField(verbose_name=_("Partner Name"), max_length=60, null=False, blank=False)
    partner_bu_name = models.CharField(verbose_name=_("Partner bu name"), max_length=60, null=False, blank=False)
    MembershipId = models.CharField(verbose_name=_("MembershipId"), max_length=60, null=False, blank=False)
    primary_customerID = models.CharField(verbose_name=_("Primary Customer ID"), max_length=60, null=False, blank=False)
    start_date = models.DateField(verbose_name=_("Start date"))
    end_date = models.DateField(verbose_name=_("End date"))

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name = _('Post Sale Data')
        verbose_name_plural = _('Post Sales Data')
