import pytest

EXPECTED_ROUTES = {
    ('/', 'GET'),
    ('/account', 'GET'),
    ('/account', 'POST'),
    ('/api/v1/basket/items', 'POST'),
    ('/api/v1/basket/items/<int:product_id>', 'DELETE'),
    ('/api/v1/products', 'GET'),
    ('/api/v1/products/<int:product_id>/rating', 'DELETE'),
    ('/api/v1/products/<int:product_id>/rating', 'PUT'),
    ('/api/v1/products/<int:product_id>/reviews', 'POST'),
    ('/api/v1/reviews/<int:review_id>', 'DELETE'),
    ('/basket', 'GET'),
    ('/checkout', 'GET'),
    ('/cloth', 'GET'),
    ('/cloth/product_detail/<product_url>', 'GET'),
    ('/create_account', 'GET'),
    ('/create_account', 'POST'),
    ('/login', 'GET'),
    ('/login', 'POST'),
    ('/logout', 'GET'),
    ('/static/<path:filename>', 'GET'),
}


def test_every_url_keeps_its_path_and_methods(test_app):
    routes = {
        (rule.rule, method)
        for rule in test_app.url_map.iter_rules()
        for method in rule.methods - {'HEAD', 'OPTIONS'}
    }

    assert routes == EXPECTED_ROUTES


@pytest.mark.parametrize('path', ['/login', '/create_account'])
def test_logged_in_user_is_sent_home_from_the_sign_in_pages(client, path):
    with client.session_transaction() as flask_session:
        flask_session['user'] = {'id': 1, 'name': 'john'}

    response = client.get(path)

    assert response.status_code == 302
    assert response.headers['Location'] == '/'
