# Generated by Django 3.0.8 on 2020-07-28 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.Player'),
        ),
    ]