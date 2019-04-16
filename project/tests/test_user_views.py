from flask_login import current_user

admin_email = 'ad@min.com'
admin_password = 'password'


def log_in(client, email=None, password=None):
    email = email or admin_email
    password = password or admin_password
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def test_correct_login(client):
    response = log_in(client)
    assert 'Logout' in str(response.data)
    assert current_user.email == admin_email
    assert current_user.is_active
    assert response.status_code == 200
