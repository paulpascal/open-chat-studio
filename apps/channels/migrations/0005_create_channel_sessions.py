# Generated by Django 4.2 on 2023-07-26 11:42

from django.db import migrations

def create_channel_session(apps, schema_editor):
    ChannelSession = apps.get_model("channels", "ChannelSession")
    ExperimentSession = apps.get_model("experiments", "ExperimentSession")

    experiment_sessions = ExperimentSession.objects.exclude(chat__external_chat_id=None).all()
    for experiment_session in experiment_sessions:
        external_chat_id = experiment_session.chat.external_chat_id
        channel_session = ChannelSession.objects.create(
            experiment_session=experiment_session,
            external_chat_id=external_chat_id
        )
        channel_session.save()

def drop_channel_sessions(apps, schema_editor):
    ChannelSession = apps.get_model("channels", "ChannelSession")
    ChannelSession.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_chat_external_chat_id"),
        ("channels", "0004_experimentchannel_platform_channelsession"),
    ]

    operations = [migrations.RunPython(create_channel_session, drop_channel_sessions)]