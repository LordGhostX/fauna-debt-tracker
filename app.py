from datetime import datetime
from dateutil import tz
from flask import *
from flask_bootstrap import Bootstrap
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "SECRET_KEY"
client = FaunaClient(secret="FAUNA_SECRET_KEY")


def faunatimefilter(faunatime):
    return faunatime.to_datetime().strftime("%A, %B %e, %Y")


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
    name = request.form.get("name")
    amount = request.form.get("amount")
    date = request.form.get("date")

    loan_data = client.query(
        q.create(
            q.collection("loans"), {
                "data": {
                    "name": name,
                    "amount": float(amount),
                    "pending": True,
                    "date_created": datetime.strptime(date, "%Y-%m-%d").astimezone(tz=tz.tzlocal())
                }
            }
        )
    )

    flash("You have successfully added loan information!", "success")
    return redirect(url_for("loans"))


@app.route("/loans/edit/", methods=["POST"])
def edit_loan():
    action = request.form.get("action")
    amount = request.form.get("amount")
    loan_id = request.form.get("loanID")

    loan_data = client.query(
        q.get(
            q.ref(q.collection("loans"), int(loan_id))
        )
    )

    old_amount = loan_data["data"]["amount"]
    if action == "Borrow More":
        new_amount = old_amount + float(amount)
    elif action == "Repay Loan":
        new_amount = old_amount - float(amount)

    client.query(
        q.update(
            q.ref(q.collection("loans"), int(loan_id)), {
                "data": {
                    "amount": new_amount
                }
            }
        )
    )

    flash("You have successfully updated loan information!", "success")
    return redirect(url_for("loans"))


if __name__ == "__main__":
    app.run(debug=True)
