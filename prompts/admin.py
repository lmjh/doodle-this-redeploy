from django.contrib import admin
from .models import Activity, Adjective, Creature, Location


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "activity",
    )

    list_editable = ("activity",)


@admin.register(Adjective)
class AdjectiveAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "determiner",
        "adjective",
    )
    list_editable = (
        "determiner",
        "adjective",
    )


@admin.register(Creature)
class CreatureAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "determiner",
        "creature",
        "plural",
    )
    list_editable = (
        "determiner",
        "creature",
        "plural",
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "location",
    )
    list_editable = ("location",)
