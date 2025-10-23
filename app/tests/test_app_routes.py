import app as myapp


def test_home_and_about_routes():
    myapp.app.config['TESTING'] = True
    with myapp.app.test_client() as client:
        res = client.get('/')
        assert res.status_code == 200

        res2 = client.get('/about')
        assert res2.status_code == 200


def test_resume_and_contact_routes():
    myapp.app.config['TESTING'] = True
    with myapp.app.test_client() as client:
        res = client.get('/resume')
        assert res.status_code == 200

        res2 = client.get('/contact')
        assert res2.status_code == 200
