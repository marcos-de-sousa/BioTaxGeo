from argparse import ArgumentParser, Namespace
import pyzenodo3.upload as zup
from pyzenodo3.base import BASE_URL
from flask import render_template, request, Blueprint, redirect, url_for, make_response

# def cmdparse() -> Namespace:
#     p = ArgumentParser(description="Upload data to Zenodo staging")
#     p.add_argument("apikey", help="Zenodo API key", nargs="?")
#     p.add_argument("inifn", help="mymeta.ini file with author, title, etc.")
#     p.add_argument("path", help="directory or file to upload to Zenodo", nargs="?")
#     p.add_argument("--use-sandbox", help="Use sandbox.zenodo.org instead of the real site.", action='store_true')
#     return p.parse_args()
zenodo_blueprint = Blueprint('zenodo', __name__, template_folder='templates')


@zenodo_blueprint("/zenodo", methods=["GET", "POST"])
def zenodo():
    # p = cmdparse()
    if request.method == 'POST':
        form = request.form.to_dict()
        metafn = zup.meta(form["inifn"])

        if form["use_sandbox"]:
            base_url = "https://sandbox.zenodo.org/api"
        else:
            base_url = BASE_URL

        zup.upload(metafn, form["path"], form["apikey"], base_url=base_url)
