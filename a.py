import random
from flask import Flask, render_template, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = "your_secret_key"

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

        user_score = session.get("user_score", 0)
        comp_score = session.get("comp_score", 0)
        draw_score = session.get("draw_score", 0)

        user_input = request.form["guess"]
        comp_choice = random.choice(choices)

        if user_input == comp_choice:
            message = "It's a Draw!"
            banner_class = "draw"
            draw_score+=1

        elif rules[user_input] == comp_choice:
            message = "You Win!"
            banner_class = "win"
            user_score+=1

        else:
            message = "Computer Wins!"
            banner_class = "lose"
            comp_score+=1

        
        session["user_score"] = user_score
        session["comp_score"] = comp_score
        session["draw_score"] = draw_score


    return render_template(
        "index.html",
        message=message,
        user_choice=user_input,
        comp_choice=comp_choice,
        banner_class=banner_class,
        user_score = session.get("user_score", 0),
        comp_score = session.get("comp_score", 0),
        draw_score = session.get("draw_score", 0),
    )

@app.route("/reset", methods=["GET"])
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)