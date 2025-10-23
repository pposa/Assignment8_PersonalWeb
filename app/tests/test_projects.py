def test_projects_empty_seeding(client):
    # Initially DB is empty; requesting /projects should seed and return grouped projects
    resp = client.get('/projects')
    assert resp.status_code == 200
    data = resp.get_data(as_text=True)
    # After seeding, at least one of the known project titles should be present
    assert 'EY Case Competition' in data or 'Patient Transparency Prototype' in data


def test_add_project_form_and_redirect(client):
    # Post a new project via /add_project and ensure redirect and presence on /projects
    resp = client.post('/add_project', data={'title': 'Test Project', 'description': 'desc', 'image_filename': 'test.png'})
    # Should redirect to projects
    assert resp.status_code in (301, 302)

    resp2 = client.get('/projects')
    assert resp2.status_code == 200
    assert 'Test Project' in resp2.get_data(as_text=True)
