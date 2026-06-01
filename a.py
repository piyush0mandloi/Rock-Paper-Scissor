import random
from flask import Flask, render_template, request

app = Flask(__name__)

choices = ["rock", "paper", "scissors"]

rules = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    user_input = ""
    comp_choice = ""
    banner_class = ""

    if request.method == "POST":
        user_input = request.form["guess"]
        comp_choice = random.choice(choices)

        if user_input == comp_choice:
            message = "It's a Draw!"
            banner_class = "draw"

        elif rules[user_input] == comp_choice:
            message = "You Win!"
            banner_class = "win"

        else:
            message = "Computer Wins!"
            banner_class = "lose"


    return render_template(
        "index.html",
        message=message,
        user_choice=user_input,
        comp_choice=comp_choice,
            banner_class=banner_class
    )


if __name__ == "__main__":
    app.run(debug=True)