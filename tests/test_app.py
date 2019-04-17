def test_app(app):
    assert app.config['TESTING']
    assert app.config['DEBUG']
