from flask import Blueprint, redirect, render_template, request, redirect, session, url_for

lab6 = Blueprint('lab6', __name__)

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')