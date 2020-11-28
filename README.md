# Django Data Migration Test

Test utilities for easily testing Django data migrations

## Installation

```
pip install django-test-data-migrations
```

## Usage

Define the following functions in your migration file
1. `data_forward(*args)`
2. `data_backward(*args)` (optional)

```python
from django_test_data_migrations import DataMigrationsTestCaseBase

from app_a.models import Animal

class YourDataMigrationTestCase(DataMigrationsTestCaseBase):
    def test__forward_migration__something_important(self):
        # Prepare some data

        # Run
        self.data_forward(some_arg_0, some_arg_1, ...)

        # Some assertions
    
    def test__backward_migration__something_important(self):
        # Prepare some data

        # Run
        self.data_backward(some_arg_0, some_arg_1, ...)

        # Some assertions
```

## Example
Say you have a simple Django project with following general structure
```bash
test_project/
└── app_a
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_datafix_addsuffixtoname.py
    │   └── __init__.py
    ├── models.py
    └── tests
        ├── __init__.py
        └── test_0002_datafix_addsuffixtoname.py
```
with the following model
```python
from django.db import models


class Animal(models.Model):
    species = models.CharField(blank=False, null=False, max_length=50)
    name = models.CharField(blank=False, null=False, max_length=100)

    def __str__(self):
        return f"Animal [name={self.name}, species={self.species}]"
```
along with the following migration
```python
# app_a/migrations/0002_datafix_addsuffixtoname.py

from django.db import migrations

SUFFIX = " ZZ"


def data_forward(Animal):
    for animal in Animal.objects.all():
        animal.name += SUFFIX
        animal.save()


def data_backward(Animal):
    for animal in Animal.objects.filter(name__endswith=SUFFIX):
        animal.name = animal.name.rstrip(SUFFIX)
        animal.save()


def forward(apps, schema_editor):
    Animal = apps.get_model("app_a", "Animal")
    data_forward(Animal)


def backward(apps, schema_editor):
    Animal = apps.get_model("app_a", "Animal")
    data_backward(Animal)


class Migration(migrations.Migration):

    dependencies = [
        ('app_a', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
```
You can test it as the following
```python
from django_test_data_migrations import DataMigrationsTestCaseBase

from app_a.models import Animal


class DataMigrationsTestCase(DataMigrationsTestCaseBase):
    app_name = "app_a"
    migration_name = "0002_datafix_addsuffixtoname"

    def test__data_forward__append_suffix_to_name(self):
        # Prepare data before migration
        dog = Animal.objects.create(name="Dog", species="dog")
        cat = Animal.objects.create(name="Cat", species="cat")

        # Run `data_forward` aka the entry point to your data migration
        self.data_forward(Animal)

        # Make your assertions
        self.assertEqual(Animal.objects.get(id=dog.id).name, "Dog ZZ")
        self.assertEqual(Animal.objects.get(id=cat.id).name, "Cat ZZ")

    def test__data_backward__append_suffix_to_name(self):
        dog = Animal.objects.create(name="Dog ZZ", species="dog")
        cat = Animal.objects.create(name="Cat zz", species="cat")

        self.data_backward(Animal)

        self.assertEqual(Animal.objects.get(id=dog.id).name, "Dog")
        self.assertEqual(Animal.objects.get(id=cat.id).name, "Cat zz")
```

## Why do I need this library?

1. Runs your data migration test very fast.
2. Encourages developers to write data-related Django migrations separately from model definition related Django migrations
3. Writing tests for data related migrations is extremely important, but is either tricky to do or takes a long time to run. This library intends to testing data migrations easy and fast

## Development

### Setup
Check requirements
```
poetry --version
```
Clone source code repository
```bash
git clone git@github.com:imranariffin/django-test-data-migrations.git
```
Install dev dependencies
```bash
poetry install
```

### Run tests
```bash
make test
```
You should be ready to start development
