from flask import Flask
from dataclasses import db
from routes import routes

import activity

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["database"] = db

app.register_blueprint(routes)
app.errorhandler(Exception)(activity.error)



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run("0.0.0.0", 2000, debug=True)
