# Generated by Django 4.2.5 on 2023-10-12 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentications', '0002_remove_customuser_billing_address_line2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='billing_address_line3',
            new_name='billing_address_line2',
        ),
    ]