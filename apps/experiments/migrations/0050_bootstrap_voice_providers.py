# Generated by Django 4.2 on 2023-10-24 12:01
import logging

from django.db import migrations


def bootstrap_voice_providers(apps, schema_editor):
    Team = apps.get_model("teams", "Team")
    VoiceProvider = apps.get_model("service_providers", "VoiceProvider")
    Experiment = apps.get_model("experiments", "Experiment")

    for team in Team.objects.all():
        if not VoiceProvider.objects.filter(team=team).exists():
            continue

        providers = {
            "aws": list(VoiceProvider.objects.filter(team=team, type="aws")),
            "azure": list(VoiceProvider.objects.filter(team=team, type="azure")),
        }

        experiments = Experiment.objects.filter(
            team=team, synthetic_voice__isnull=False, voice_provider__isnull=True
        )
        for experiment in experiments:
            type_ = experiment.synthetic_voice.service.lower()
            if type_ not in providers or not providers[type_]:
                logging.warning("No voice provider for %s", type_)
                continue

            provider = providers[type_][0]
            experiment.voice_provider = provider
            experiment.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("experiments", "0049_experiment_voice_provider"),
    ]

    operations = [
        migrations.RunPython(bootstrap_voice_providers)
    ]