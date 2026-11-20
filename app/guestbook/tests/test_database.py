import pytest
from django.db import connection


@pytest.mark.django_db
def test_tests_run_on_postgresql_18_or_later():
    assert connection.vendor == "postgresql"
    assert connection.pg_version >= 180000
