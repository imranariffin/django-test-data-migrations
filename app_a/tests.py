from importlib import import_module

from django.test import TestCase

from app_a.models import Animal


class DataFixTestCaseBase(TestCase):
    app_name = None
    migration_name = None
    data_forward = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.app_name is None:
            raise Exception("`app_name` is not defined")
        if cls.migration_name is None:
            raise Exception("`migration_name` is not defined")

        migration_path = f"{cls.app_name}.migrations.{cls.migration_name}"
        migration_module = import_module(migration_path)

        if not hasattr(migration_module, "data_forward"):
            raise Exception("`data_forward` function is not defined in migration")

        def _f(self, *args):
            migration_module.data_forward(*args)
        cls.data_forward = _f


class DataFixTestCase(DataFixTestCaseBase):
    app_name = "app_a"
    migration_name = "0002_appa_datafix_addsuffixtoname"

    def test_data_fix(self):
        dog = Animal.objects.create(name="Dog", species="dog")
        cat = Animal.objects.create(name="Cat", species="cat")


        self.data_forward(Animal)

        self.assertEqual(
            Animal.objects.get(id=dog.id).name,
            "Dog ZZ",
        )
        self.assertEqual(
            Animal.objects.get(id=cat.id).name,
            "Cat ZZ",
        )

