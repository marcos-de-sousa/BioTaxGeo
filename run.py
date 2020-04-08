from flask import Flask
from controller.form_controller import form_blueprint
from controller.home_controller import home_blueprint
from controller.markers_controller import markers_blueprint
from controller.taxon_controller import taxon_blueprint

app = Flask(__name__)

# home
app.register_blueprint(home_blueprint)

# Readers
app.register_blueprint(form_blueprint)

# Markers_Validation
app.register_blueprint(markers_blueprint)

# Taxon_Validation
app.register_blueprint(taxon_blueprint)

app.run(debug=True, port=8080)
