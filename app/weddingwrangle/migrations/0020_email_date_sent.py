# Generated by Django 4.0.7 on 2023-07-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weddingwrangle', '0019_remove_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='date_sent',
            field=models.DateTimeField(null=True),
        ),
    ]
