from typing import Dict

from django.contrib import admin
from django.http.request import HttpRequest

from apps.channels.models import ExperimentChannel


@admin.register(ExperimentChannel)
class ExperimentChannelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "team",
        "platform",
        "active",
    )
    search_fields = ("name",)
    list_filter = (
        "platform",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    @admin.display(description="Team")
    def team(self, obj):
        return obj.experiment.team.name

    def get_changeform_initial_data(self, request: HttpRequest) -> Dict[str, str]:
        return {"extra_data": {"bot_token": "your token here"}}
