import flask

def test_index_should_return_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_404(client):
    response = client.get('/404')
    assert response.status_code == 404
