# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, CustomGroup, Group ,TicketChat,TicketBD

admin.site.unregister(Group)

def make_published(modeladmin, request, queryset):
    queryset.update(is_visible=True)
make_published.short_description = _("Активировать  группы")

def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_visible=True)
make_unpublished.short_description = _("Деактивировать группы")

@admin.register(CustomGroup)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)
    actions = [make_published,make_unpublished]

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

@admin.register(CustomUser)
class AuthorAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]
        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

@admin.register(TicketChat)
class LocateUserAdmin(admin.ModelAdmin):
    # list_display = ('id', 'char')
    pass

@admin.register(TicketBD)
class LocateUserAdmin(admin.ModelAdmin):
    # list_display = ('id', 'char')
    pass

