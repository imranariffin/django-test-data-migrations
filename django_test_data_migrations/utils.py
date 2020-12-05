from django.db.migrations import RunPython


def validate(migration_class: "Migration") -> None:
    operations = migration_class.operations

    for operation in operations:
        if not isinstance(operation, RunPython):
            raise Exception("Non-Python migration is not supported")
