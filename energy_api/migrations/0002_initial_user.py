from django.db import migrations

from energy_api.models import User


def create_initial_user(apps, schema_editor):
    User.objects.create_superuser(
        username='admin',
        email='admin@gmail.com',
        password='123456789',
    )

class Migration(migrations.Migration):
    dependencies = [('energy_api','0001_initial')]
    operations = [
        migrations.RunPython(create_initial_user),
    ]