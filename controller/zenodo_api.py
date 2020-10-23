import pyzenodo3.upload as zup
from pyzenodo3.base import BASE_URL
from flask import request, Blueprint

zenodo_blueprint = Blueprint('zenodo', __name__, template_folder='templates')

@zenodo_blueprint("/zenodo", methods=["GET", "POST"])
def zenodo():
    if request.method == 'POST':
        form = request.form.to_dict()
        metafn = zup.meta(form["inifn"])

        if form["use_sandbox"]:
            base_url = "https://sandbox.zenodo.org/api"
        else:
            base_url = BASE_URL

        zup.upload(metafn, form["path"], form["apikey"], base_url=base_url)
