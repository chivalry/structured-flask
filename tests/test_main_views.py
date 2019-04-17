def test_index(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Login' in str(response.data)


def test_404(client):
    response = client.get('/route_does_not_exist')
    assert response.status_code == 404
