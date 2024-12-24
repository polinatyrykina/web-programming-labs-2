from flask import Blueprint, render_template, request, jsonify, abort, session, current_app

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')