import pytest
from rest_framework import settings
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
