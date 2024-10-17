from flask import Blueprint, redirect, url_for, request, make_response, render_template
lab3 = Blueprint('lab3', __name__)

@lab3.route("/lab3/")
def lab():
    return render_template('lab3/lab3.html')