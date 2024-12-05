from flask import Blueprint, redirect, url_for, render_template, request, make_response, session, current_app

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')
