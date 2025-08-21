from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company, Address


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Show extra fields in list view
    list_display = ("username", "email", "phone", "user_type", "is_verified", "kyc_verified", "is_active", "date_joined")
    list_filter = ("user_type", "is_verified", "kyc_verified", "is_staff", "is_active")
    search_fields = ("username", "email", "phone")

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "user_type",
                "phone",
                "country_code",
                "alternate_email",
                "is_verified",
                "kyc_verified",
                "signup_ip",
                "last_login_ip",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": (
                "user_type",
                "phone",
                "country_code",
                "alternate_email",
            )
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "gst_number", "pan_number", "website", "created_at")
    search_fields = ("name", "gst_number", "pan_number", "owner__username")
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("address_line1", "city", "state", "country", "postal_code", "address_type", "is_default", "get_owner")
    search_fields = ("address_line1", "city", "state", "country", "postal_code", "user__username", "company__name")
    list_filter = ("address_type", "is_default", "country", "state")
    ordering = ("-created_at",)

    def get_owner(self, obj):
        if obj.user:
            return f"User: {obj.user.username}"
        elif obj.company:
            return f"Company: {obj.company.name}"
        return "N/A"
    get_owner.short_description = "Owner"
