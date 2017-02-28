from flask import Blueprint, render_template

student= Blueprint('student',__name__)

@student.route('/<user_url_slug>')
def timeline(user_url_slug):
    return render_template('student/timeline.html')

@student.route('/<user_url_slug>/photos')
def photos(user_url_slug):
    return render_template('student/photos.html')

@student.route('/<user_url_slug>/about')
def about(user_url_slug):
    return render_template('student/about.html')