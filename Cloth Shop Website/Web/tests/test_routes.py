import pytest

EXPECTED_ROUTES = {
    ('/', 'GET'),
    ('/account', 'GET'),
    ('/account', 'POST'),
    ('/add-to-basket', 'POST'),
    ('/basket', 'GET'),
    ('/basket/<int:product_id>', 'DELETE'),
    ('/checkout', 'GET'),
    ('/cloth', 'GET'),
    ('/cloth/product_detail/<product_url>', 'GET'),
    ('/create_account', 'GET'),
    ('/create_account', 'POST'),
    ('/delete_review', 'POST'),
    ('/filtered-products', 'POST'),
    ('/login', 'GET'),
    ('/login', 'POST'),
    ('/logout', 'GET'),
    ('/reset_rating', 'POST'),
    ('/save_rating', 'POST'),
    ('/save_review', 'POST'),
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
