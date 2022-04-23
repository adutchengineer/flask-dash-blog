
import dash
import markdown2
from flask import (Flask, redirect, render_template, render_template_string,
                   url_for)
from flask_flatpages import FlatPages
from flask_flatpages.utils import pygmented_markdown
from flask_frozen import Freezer

from main.dash.dashboard import init_dashboard

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"
FLATPAGES_ROOT = "content"
POST_DIR = "posts"


def my_renderer(text):
    body = render_template_string(
        markdown2.markdown(text, extras=["fenced-code-blocks"])
    )
    return pygmented_markdown(body)


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(__name__)
    app.config["FLATPAGES_HTML_RENDERER"] = my_renderer
    register_dashapps(app)
    register_routes(app)
    return app


def register_dashapps(app):
    from .dash.layout import html_layout

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }

    dash_app = dash.Dash(
        server=app,
        routes_pathname_prefix="/projects/dashapp/",
        external_stylesheets=[
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    with app.app_context():
        dash_app.index_string = html_layout
        dash_app.layout = init_dashboard()


def register_routes(app):
    pages = FlatPages(app)
    freezer = Freezer(app)

    @app.route("/")
    def index():
        return render_template("main.html")

    @app.route("/posts/")
    def posts():
        posts = [p for p in pages if p.path.startswith(POST_DIR)]
        posts.sort(key=lambda item: item["date"], reverse=True)
        return render_template("posts.html", posts=posts)

    @app.route("/posts/<name>/")
    def post(name):
        path = "{}/{}".format(POST_DIR, name)
        post = pages.get_or_404(path)
        return render_template("post.html", post=post)

    @app.route("/<title_for_redirect>")
    def project_jupyter_notebook():
        return redirect("https://mybinder.org/<your_binder_url>")

    @freezer.register_generator
    def pagelist():
        for post in posts:
            yield url_for("post", path=post.path)
