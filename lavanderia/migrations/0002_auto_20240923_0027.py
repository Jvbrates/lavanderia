from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from lavanderia.models import AvaibleSlot, Washer, ReservedSlot


def add_permissions_to_group(apps, schema_editor):
    groupBolsistas, created = Group.objects.get_or_create(name='bolsistas')

    models_to_add = [AvaibleSlot, Washer, ReservedSlot]

    for model in models_to_add:
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        for perm in permissions:
            groupBolsistas.permissions.add(perm)


class Migration(migrations.Migration):
    dependencies = [
        ('lavanderia', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_permissions_to_group),
    ]
