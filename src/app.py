from flask import Flask
import connexion
import os

# Create the application instance
app = connexion.FlaskApp(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

app.run(port=5000)

# from flask import Flask, redirect, url_for
# from flask_dance.contrib.authentiq import make_authentiq_blueprint
