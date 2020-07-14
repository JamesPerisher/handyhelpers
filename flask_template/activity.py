from flask import render_template, jsonify, request, session, redirect
from dataclasses import Test
import forms

from werkzeug.exceptions import HTTPException



def home():
    return render_template("home.html")

def error(e):
    return render_template("error.html", error_num=e.code if isinstance(e, HTTPException) else 500, error_txt=str(e).split(": ", 1)[1])
