from django.contrib import admin
from .models import ApiToken
from drfaddons.admin import CreateUpdateAdmin


class ApiTokenAdmin(CreateUpdateAdmin):
    list_display = ('title', 'token', 'create_date', 'is_active')
    search_fields = ('token',)

    ownership_info = {
        'label': 'Ownership Info',
        'fields': {
            'token': {'readonly': True},
            'created_by': {'readonly': True},
            'create_date': {'readonly': True},
            'update_date': {'readonly': True}
        }
    }

    def save_model(self, request, obj, form, change):
        from api_token.utils import generate_token

        if not obj.token:
            obj.token = generate_token()
        super().save_model(request, obj, form, change)


admin.site.register(ApiToken, ApiTokenAdmin)
