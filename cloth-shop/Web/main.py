from flask import Flask, Response, jsonify, redirect, request, session, url_for
from flask.typing import ResponseReturnValue

from blueprints import api, auth, basket, catalogue
from config import get_config
from database import create_database_Session
from exceptions import ProductNotFound, ShopError, UserNotFound
from utils import get_username_by_id_filter

BLUEPRINTS = (auth.bp, catalogue.bp, basket.bp, api.bp)


def handle_missing_record(error: ShopError) -> ResponseReturnValue:
    return jsonify({'message': str(error)}), 404


def nl2br_filter(s: str) -> str:
    return s.replace('\n', '<br>')


def before_request() -> ResponseReturnValue | None:
    if 'user' in session and request.endpoint in ['auth.login']:
        return redirect(url_for('catalogue.home'))
    if 'user' in session and request.endpoint in ['auth.create_account']:
        return redirect(url_for('catalogue.home'))
    ## if you are logged in and you try to go back to login page you will get redirected to home page

    if 'basket' not in session:
        session['basket'] = []
    ## sets empty basket


## User will be unable to go back to a previously visited page and remaining logged in after logging out
def add_header(response: Response) -> Response:
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.cache_control.max_age = 0
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    return response


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    app.extensions['db_Session'] = create_database_Session(
        app.config['DATABASE_URL'], echo=app.config['SQLALCHEMY_ECHO']
    )

    app.jinja_env.filters['get_username_by_id'] = get_username_by_id_filter
    app.add_template_filter(nl2br_filter, 'nl2br')

    app.register_error_handler(ProductNotFound, handle_missing_record)
    app.register_error_handler(UserNotFound, handle_missing_record)

    app.before_request(before_request)
    app.after_request(add_header)

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
