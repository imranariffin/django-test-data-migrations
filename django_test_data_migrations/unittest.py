from importlib import import_module

from django.test import TestCase


class DataMigrationsTestCaseBase(TestCase):
    app_name = None
    migration_name = None
    data_forward = None
    data_backward = None

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

        if hasattr(migration_module, "data_backward"):
            def _b(self, *args):
                migration_module.data_backward(*args)
            cls.data_backward = _b
