import unittest

from django.db import migrations, models
from django_test_data_migrations.utils import validate


class ValidateTestCase(unittest.TestCase):
    def test_do_not_raise_when_migration_is_python(self):
        class Migration(migrations.Migration):

            dependencies = [
                ('app_a', '0001_initial'),
            ]

            operations = [
                migrations.RunPython(
                    migrations.RunPython.noop,
                    migrations.RunPython.noop,
                ),
            ]
        
        validate(Migration)

    def test_raise_when_migration_is_not_python(self):
        migration_methods = [
            # migrations.AddModel,
            (
                migrations.CreateModel,
                dict(
                    name='SomeNewModel',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True)),
                        ('species', models.CharField(max_length=50)),
                        ('name', models.CharField(max_length=100)),
                    ],
                ),
            )
        ]

        for migration_method, kwargs in migration_methods:
            class Migration(migrations.Migration):

                dependencies = [
                    ('app_a', '0001_initial'),
                ]

                operations = [
                    migration_method(**kwargs),
                ]

            with self.assertRaises(Exception):
                validate(Migration)
