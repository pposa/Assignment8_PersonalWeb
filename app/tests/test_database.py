import DAL


def test_database_connection(tmp_path):
    db_path = str(tmp_path / "projects_test.db")
    # initialize a fresh DB file at the path
    DAL.init_projects_db(db_path=db_path)
    conn = DAL.get_connection(db_path=db_path)
    assert conn is not None
    conn.close()


def test_insert_and_get_projects(tmp_path):
    db_path = str(tmp_path / "projects_test2.db")
    DAL.init_projects_db(db_path=db_path)
    # insert a test project
    rowid = DAL.insert_project({'Title': 'T', 'Description': 'D', 'ImageFileName': 'i.png'}, db_path=db_path)
    assert isinstance(rowid, int) and rowid > 0
    rows = DAL.get_projects(db_path=db_path)
    assert len(rows) == 1
    assert rows[0]['Title'] == 'T'
