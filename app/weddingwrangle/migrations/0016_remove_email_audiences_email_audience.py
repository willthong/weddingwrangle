# Generated by Django 4.0.7 on 2023-07-06 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weddingwrangle', '0015_alter_audience_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='audiences',
        ),
        migrations.AddField(
            model_name='email',
            name='audience',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='email', to='weddingwrangle.audience'),
            preserve_default=False,
        ),
    ]