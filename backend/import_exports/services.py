from .models import ImportExport
from utils.custom_exceptions import *


def get_import_export_by(raise_exception=True, **kwargs):
    import_export = ImportExport.objects.filter(**kwargs).all()
    if not import_export and raise_exception: 
        raise ObjectNotFound
    return import_export

def add_import_export(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = value
    import_export = get_import_export_by(raise_exception=False,  year=data['year'], month = data['month']).first()
    if import_export:
        raise DuplicateEntry(entry=str(import_export.year) + str(import_export.month), key='year and month')
    import_export = ImportExport.objects.create(**dict(data))
    return import_export

def update_import_export(import_export, data):
    if not any(data.values()):
        raise ValidationError
    import_export._import = data.get('_import') or import_export._import
    import_export.export = data.get('export') or import_export.export
    import_export.save(update_fields=['_import', 'export'])
    return import_export

def delete_import_export(import_export):
    import_export.delete()
    return import_export
