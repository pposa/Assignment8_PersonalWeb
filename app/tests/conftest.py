import os
import pytest
from pathlib import Path

import app as myapp
import DAL

@pytest.fixture(scope="function")
def tmp_db(tmp_path):
    """Create a temporary projects DB and point DAL.PROJECTS_DB at it for the duration of the test."""
    db_path = str(tmp_path / "projects_test.db")
    # initialize a fresh DB file at the path
    DAL.init_projects_db(db_path=db_path)
    # override in-memory module variable so DAL functions use the test DB
    DAL.PROJECTS_DB = db_path
    yield db_path
    try:
        os.remove(db_path)
    except OSError:
        pass

@pytest.fixture(scope="function")
def client(tmp_db):
    """Flask test client configured for testing."""
    myapp.app.config['TESTING'] = True
    with myapp.app.test_client() as client:
        yield client
