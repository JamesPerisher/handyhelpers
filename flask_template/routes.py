from flask import Flask
from flask import render_template, redirect, make_response, request, url_for, flash

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "".join([s.choice([chr(i) for i in range(32,127)]) for j in range(128)]) # gen random secret probs bad idea
print("Secret key: %s" %app.config["SECRET_KEY"])


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def home_redirect():
    return redirect("/", code=302)

@app.route("/favicon.ico")
def favicon():
    return redirect("static/images/favicon.ico")

@app.route("/license")
def license():
    return render_template("license.html")

@app.route("/donate")
def donate():
    return redirect("https://www.paypal.me/pauln07/5USD")



@app.errorhandler(HTTPException)
def error404(error):
    print(error, type(error))
    error = str(error)
    try:
        return render_template("error.html", error_num=error.split(":",1)[0], error_txt=error.split(":",1)[1])
    except IndexError:
        return render_template("error.html", error_num="Infinity", error_txt="This error SHOULD in theory never be seen by the user.")



if __name__ == "__main__":
    app.run(debug = True, use_reloader=True)
