import re

from django.apps import apps
from django.conf import settings

CLASSIFIED = re.compile(r"^(public|private|operational|evidence) \| \S.*$")


def test_every_model_field_has_a_class_and_a_type():
    missing = []
    for model in apps.get_models():
        if model._meta.app_label not in settings.PROJECT_APPS:
            continue
        for field in model._meta.local_concrete_fields:
            if not CLASSIFIED.match(field.db_comment or ""):
                missing.append(f"{model.__name__}.{field.name}")
    assert missing == []
