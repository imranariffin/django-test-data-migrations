from django_test_data_migrations import DataMigrationsTestCaseBase

from app_a.models import Animal


class DataMigrationsTestCase(DataMigrationsTestCaseBase):
    app_name = "app_a"
    migration_name = "0002_datafix_addsuffixtoname"

    def test__data_forward__append_suffix_to_name(self):
        dog = Animal.objects.create(name="Dog", species="dog")
        cat = Animal.objects.create(name="Cat", species="cat")

        self.data_forward(Animal)

        self.assertEqual(Animal.objects.get(id=dog.id).name, "Dog ZZ")
        self.assertEqual(Animal.objects.get(id=cat.id).name, "Cat ZZ")

    def test__data_backward__append_suffix_to_name(self):
        dog = Animal.objects.create(name="Dog ZZ", species="dog")
        cat = Animal.objects.create(name="Cat zz", species="cat")

        self.data_backward(Animal)

        self.assertEqual(Animal.objects.get(id=dog.id).name, "Dog")
        self.assertEqual(Animal.objects.get(id=cat.id).name, "Cat zz")
