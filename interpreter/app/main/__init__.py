from flask import Flask, redirect, send_file
import os
from .tools.tools import JsonResp
from .classify.trashd import Trash

# Import Routes
from .userdb.routes import user_blueprint
from .annotator.routes import anno_blueprint
from .tfmodels.routes import tfmodels_blueprint
from .classify.routes import classify_blueprint
from .static.routes import static_blueprint
from .datadb.routes import files_blueprint
from .report.routes import reports_blueprint


def create_app():

    # Flask Config
    app = Flask(__name__)

    app.config.from_pyfile("config/config.cfg")

    # set template & static paths:
    app.template_folder = "../../demos/"
    app.static_folder = "../../demos/"

    # upload --> classify config
    app.config['UPLOAD_EXTENSIONS'] = ['.mp3', '.wav', '.WAV', '.wave', '.WAVE']
    app.config['UPLOAD_PATH'] = 'uploads'

    # misc Config
    os.environ["TZ"] = app.config["TIMEZONE"]

    # Register Blueprints
    app.register_blueprint(files_blueprint, url_prefix="/files")
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(anno_blueprint, url_prefix="/annotator")
    app.register_blueprint(tfmodels_blueprint, url_prefix="/models")
    app.register_blueprint(classify_blueprint, url_prefix="/classify")
    app.register_blueprint(static_blueprint, url_prefix="/annotator/static")
    app.register_blueprint(reports_blueprint, url_prefix="/reports")

    # start garbage collection daemon:
    Trash.truck()

    # fetch static:
    @app.route("/favicon.ico", methods=["GET", "POST"])
    def appclcfavicon_ico():
        return app.send_static_file("icons/tmpUI.MerlinAI-favicon-dark/favicon.ico")

    @app.route("/site.webmanifest", methods=["GET", "POST"])
    def appclcwebmanifest():
        return app.send_static_file("icons/tmpUI.MerlinAI-favicon-dark/site.webmanifest")

    @app.route("/favicon-16x16.png", methods=["GET", "POST"])
    def appclcfavicon_ico16():
        return app.send_static_file("icons/tmpUI.MerlinAI-favicon-dark/favicon-16x16.png")

    @app.route("/favicon-32x32.png", methods=["GET", "POST"])
    def appclcfavicon_ico32():
        return app.send_static_file("icons/tmpUI.MerlinAI-favicon-dark/favicon-32x32.png")

    @app.route("/apple-touch-icon.png", methods=["GET", "POST"])
    def appclcapple_touch():
        return app.send_static_file("icons/tmpUI.MerlinAI-favicon-dark/apple-touch-icon.png")

    @app.route("/android-chrome-192x192.png", methods=["GET", "POST"])
    def appclcdroid192():
        return app.send_static_file("icons/tmpUI.MerlinAI-favicon-dark/android-chrome-192x192.png")

    @app.route("/android-chrome-512x512.png", methods=["GET", "POST"])
    def appclcdroid512():
        return app.send_static_file("icons/tmpUI.MerlinAI-favicon-dark/android-chrome-512x512.png")

    # fetch static:
    @app.route("/<f>/", methods=["GET", "POST"])
    def appclcfx(f):
        print(f)
        return app.send_static_file(f)

    # Index Routes:
    @app.route("/")
    def index():
        return redirect("/classify/server", code=302)

    return app
