# Generated by Django 4.2 on 2023-10-12 11:12

import django.db.models.deletion
from django.db import migrations, models

from apps.utils.teams_migration import assign_model_to_team_migration


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0003_flag"),
        ("chat", "0005_delete_futuremessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="team",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="teams.team", verbose_name="Team"
            ),
            preserve_default=False,
        ),
        migrations.RunPython(assign_model_to_team_migration("chat.Chat"), migrations.RunPython.noop),
        migrations.AlterField(
            model_name="chat",
            name="team",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="teams.team", verbose_name="Team"),
        ),
    ]
