# Generated by Django 4.2.5 on 2023-10-12 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0003_rename_billing_address_line3_customuser_billing_address_line2'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
