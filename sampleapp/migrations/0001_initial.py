# Generated by Django 4.2.3 on 2023-08-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('can_create_sampleapp_entry', 'Can create sampleapp entries'), ('can_view_sampleapp_entries', 'Can view one or all entries')],
            },
        ),
    ]
