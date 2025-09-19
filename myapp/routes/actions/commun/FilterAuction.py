from flask import Blueprint, redirect, session, url_for


filter = Blueprint("filter", __name__)

@filter.route("/filter")
def Filter():
    return