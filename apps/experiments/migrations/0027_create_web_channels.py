# Generated by Django 4.2 on 2023-08-14 19:07

from django.db import migrations

def populate_web_channel_and_channel_sessions(apps, schema_editor):
    """Creates web channel records with channel sessions for existing chats"""
    ChannelSession = apps.get_model("channels", "ChannelSession")
    ExperimentChannel = apps.get_model("channels", "ExperimentChannel")
    ExperimentSession = apps.get_model("experiments", "ExperimentSession")
    
    sessions = ExperimentSession.objects.filter(channel_session=None).select_related("chat").all()
    for session in sessions:
        experiment = session.experiment
        channel_name = f"{experiment.id}-web"
        experiment_channel, _created = ExperimentChannel.objects.get_or_create(
            name=channel_name,
            experiment=experiment,
            platform="web"
        )
        ChannelSession.objects.get_or_create(
            experiment_channel=experiment_channel,
            external_chat_id=session.chat.id,
            experiment_session=session
        )


class Migration(migrations.Migration):
    dependencies = [
        ("experiments", "0026_noactivitymessageconfig_and_more"),
    ]

    operations = [migrations.RunPython(populate_web_channel_and_channel_sessions, migrations.RunPython.noop)]