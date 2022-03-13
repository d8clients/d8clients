# Generated by Django 4.0.2 on 2022-03-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_alter_organization_description'),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='subscribes',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to='organization.Organization'),
        ),
    ]
