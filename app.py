from datetime import datetime
from flask import *
from flask_bootstrap import Bootstrap
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

app = Flask(__name__)
Bootstrap(app)
client = FaunaClient(secret="FAUNA_SECRET_KEY")


def faunatimefilter(faunatime):
    return faunatime.to_datetime().strftime("%c")


app.jinja_env.filters["faunatimefilter"] = faunatimefilter


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/loans/")
def loans():
    loans = client.query(
        q.paginate(
            q.match(q.index("loans_by_pending"), True),
            size=100_000
        )
    )
    loans_data = [
        q.get(
            q.ref(q.collection("loans"), loan.id())
        ) for loan in loans["data"]
    ]
    return render_template("loans.html", loans_data=client.query(loans_data))


@app.route("/loans/add/", methods=["POST"])
def add_loan():
    return redirect(url_for("loans"))


@app.route("/loans/edit/", methods=["POST"])
def edit_loan():
    return redirect(url_for("loans"))


if __name__ == "__main__":
    app.run(debug=True)
