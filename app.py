import os
import json
from datetime import datetime
from flask import Flask, redirect, render_template, request, session
from utils import check_username, check_answer, get_next_riddle
from constants import *

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "'^Ps[5b2?4!:$;6w}?|/DP4x^j[A")

with open("data/riddles.json") as riddle_file:
    RIDDLES = json.load(riddle_file)["riddles"]

'''
Homepage view which handles initial load as well as processes POST 
requests sent back when someone enters their username to play
'''
@app.route('/', methods=["GET", "POST"])
def index():
    # Use session cookie to store username for entire game duration
    if "username" in session:
        # User already picked a name, redirect them to the game
        return redirect("/riddles")
    with open("data/scores.json") as scores_file:
        # Load scores file to check username against and to render hiscores
        userscores = json.load(scores_file)
    if request.method == "GET":
        return render_template("index.html", hiscores=userscores)
    if request.method == "POST":
        # Homepage shows user form which sends POST request back to itself here
        username = request.form["username"]
        if not check_username(userscores, username):
            # Username was invalid
            return render_template(
                    "index.html", 
                    username=username, 
                    error=True, 
                    hiscores=userscores)
        else:
            '''
            Username was valid, add it to the json and then write file so
            nobody else can use it
            '''
            userscores[username] = 0
            with open("data/scores.json", "w") as write_file:
                json.dump(userscores, write_file)
            # Also store username in session cookie
            session["username"] = username
            return redirect("/riddles")
    # If neither GET or POST requests brought us here, I'll use this as fallback
    return render_template("index.html", hiscores=userscores)

'''
Game view which handles both the initial game screen load as a GET request,
and the subsequent attempts to answer riddles as POST requests.
'''
@app.route('/riddles', methods=["GET", "POST"])
def riddles():
    '''
    If someone tries to load page without a username in session cookie
    send them to the homepage to pick one
    '''
    if "username" not in session:
        return redirect("/")
    username = session["username"]
    if "score" not in session:
        # On first load, score won't be in cookie yet, so add it now
        session["score"] = 0
    score = session["score"]
    with open("data/scores.json") as scores_file:
        scores = json.load(scores_file)
    if request.method == "GET":
        '''
        GET will occur only on initial load, so set some initial game
        progress variables in session cookie, and then render first
        riddle
        '''
        session["score"] = 0
        # Attempts tracks how many times user has tried to answer riddle
        session["attempts"] = 0
        next_riddle = get_next_riddle(RIDDLES, None)
        return render_template(
                "game.html", 
                username=username, 
                riddle=next_riddle, 
                progress=0, 
                score=session["score"], 
                hiscores=scores)
    if request.method == "POST":
        '''
        After initial load, user enters their answer in a form and submits
        which is sent back to this view via POST request. Check whether
        the answer was correct and then render the relevant data.
        '''
        answer = request.form["answer"]
        progress = int(request.form["progress"])
        current_riddle = RIDDLES[progress]
        if not check_answer(current_riddle, answer):
            '''
            Answer was incorrect, user has ATTEMPTS_PER_RIDDLE attempts to 
            answer, and then they are sent onto the next riddle. 
            '''
            session["attempts"] += 1
            message = """Sorry, your answer '%s' was incorrect. 
                        You have %s attempt left.""" % (
                            answer, 
                            (ATTEMPTS_PER_RIDDLE - session["attempts"]))
            if session["attempts"] >= ATTEMPTS_PER_RIDDLE:
                next_riddle = get_next_riddle(RIDDLES, progress)
                if next_riddle == None:
                    # No more riddles, so the game is over
                    return redirect("/gameover")
                progress += 1
                current_riddle = next_riddle
                session["attempts"] = 0
                message = """Sorry, your answer '%s' was incorrect and 
                            you ran out of attempts. Try the next 
                            riddle below.""" % answer
            return render_template(
                    "game.html", 
                    username=username, 
                    riddle=current_riddle, 
                    progress=progress, 
                    incorrect=True, 
                    message=message, 
                    answer=answer, 
                    score=score, 
                    hiscores=scores)
        else:
            '''
            Answer was correct, increment score by POINTS_PER_RIDDLE and
            then load next riddle.
            '''
            session["score"] = score + POINTS_PER_RIDDLE
            next_riddle = get_next_riddle(RIDDLES, progress)
            if next_riddle == None:
                # No more riddles, so the game is over
                return redirect("/gameover")
            progress += 1
            current_riddle = next_riddle
            # Reset number of attempts for next riddle
            session["attempts"] = 0
            message = "Correct! You have added %s %s to your score" % (
                        POINTS_PER_RIDDLE, 
                        "point" if POINTS_PER_RIDDLE == 1 else "points")
            return render_template(
                    "game.html", 
                    username=username, 
                    riddle=current_riddle, 
                    progress=progress, 
                    last_correct=True, 
                    message=message,
                    score=session["score"], 
                    hiscores=scores)
    # If neither GET or POST requests brought us here, use this as fallback
    return redirect("/")

'''
Gameover view which handles when there are no more riddles to answer
Once a player reaches this page, update the score for them in the scores JSON
and then write back to file. Also clear their session cookie.
'''
@app.route('/gameover')
def gameover():
    # User didn't have a username in cookie, so they weren't playing game yet
    if "username" not in session:
        return redirect("/")
    username = session["username"]
    if "score" not in session:
        session["score"] = 0
    score = session["score"]
    with open("data/scores.json") as scores_file:
        scores = json.load(scores_file)
    scores[username] = score
    with open("data/scores.json", "w") as write_file:
        json.dump(scores, write_file)
    session.clear() 
    return render_template(
            "gameover.html", 
            username=username, 
            score=score, 
            hiscores=scores)

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)