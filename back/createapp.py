from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='../website/static',
                static_url_path='/static', template_folder='../website/templates')
    app.config['SECRET_KEY'] = 'test_key'  # Change the key to be something secret later for security

    from back.views import views, display_dataframe

    app.register_blueprint(views, url_prefix='/')

    return app
