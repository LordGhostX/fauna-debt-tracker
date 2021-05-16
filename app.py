from flask import *
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/loans/")
def loans():
    return render_template("loans.html")


@app.route("/loans/add/", methods=["POST"])
def add_loan():
    return redirect(url_for("loans"))


@app.route("/loans/edit/", methods=["POST"])
def edit_loan():
    return redirect(url_for("loans"))


if __name__ == "__main__":
    app.run(debug=True)
