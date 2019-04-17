from flask import current_app


def test_test_app(app):
    assert app.config['TESTING']
    assert app.config['DEBUG']
    assert app.config['BCRYPT_LOG_ROUNDS'] == 4


def test_dev_config(blank_app):
    blank_app.config.from_object('app.DevConfig')
    assert not blank_app.config['TESTING']
    assert not blank_app.config['WTF_CSRF_ENABLED']
    assert blank_app.config['DEBUG_TB_ENABLED']
    assert current_app is not None
    assert blank_app.config['BCRYPT_LOG_ROUNDS'] == 4


def test_prod_config(blank_app):
    blank_app.config.from_object('app.ProdConfig')
    assert not blank_app.config['TESTING']
    assert not blank_app.config['DEBUG_TB_ENABLED']
    assert blank_app.config['WTF_CSRF_ENABLED']
    assert blank_app.config['BCRYPT_LOG_ROUNDS'] == 13
