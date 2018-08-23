# Hello World!
Welcome to my little "Riddle-Me" Guessing Game.

Visit my live game here:
https://annies-riddle.herokuapp.com/


## How this game works:
At the start of the game, the player is asked to provide a username.

If the username is already taken, the user will receive an error to inform him. 
If the username is available, the username will be visible on the top right hand corner
and the score is set to 0 (zero).

The game begins!

The player is presented with a riddle-me question.

#### Riddle-Me Quiz Question Example:


**"I am circular. I go up and down.**
**You can throw me. You can catch me.**
**Be careful with me near windows. What am I?"**

**Correct answer: a ball**

In my Riddle-Me game it doesn't matter if your answer is:

- ball,
- a ball,
- a Ball,
- A BALL

I will convert your answer into lower-case characters and check if your provided answer
contains the word 'ball'.

Great, isn't it?


Thank you for visiting my site!
**Enjoy the game!**

Best wishes,

Annie



# Hello Developers / Coders / Techies!
Welcome to my little "Riddle-Me" Guessing Game.

Visit my live game [here](https://annies-riddle.herokuapp.com/)


### Pseudo Code on how my game works:

First Load:
- Ask user to enter username
- Check username is not in use
  - if username is in use:
        - ask for different name
  - else: proceed to quiz/riddle
- Leader Board called "High Cores" is visible at all times

Quiz/Riddle Start:
- using file i/o to read json file containing list of Q&A's
- ask first question
- check answer
    - if incorrect:
        - inform user "wrong" and that they have 1 more attempt
        - display wrong answer above quiz question
        - write to json file: 0
        - button: "next question"
    - if correct:
        - inform user "correct!" and "one point added to your score"
        - write to json file: 1
        -  "next question"

Quiz/Riddle End:
- if no more "next question"
    - infrom user that the game is over 
    - load "gameover.html"
    - confetti effect
- Leader Board called "High Cores" is visible at all times and at the end of the game it will diplay the user's score


## Technologies Used
- Python 
- Flask 
- Bootstrap 4.1.2 (with dependecies jQuery 3.3.1 and popper 1.14.3)
- own CSS, using @keyframes for Fade Out effects
- Flask Jinja templates mixed with HTML5
- Used https://github.com/Agezao/confetti-js


## Testing
- Created a series of unit tests in `tests.py` which initially failed. 
- These tests made a range of assertions which can be seen in the comments of each test in that file.
- Once a full range of tests were created, I then created `utils.py` with utility functions that related to each test.
- These functions are explained in the comments within `utils.py`
- When the functions were complete, all tests were then correctly passing, and I ensured they continued to pass while developing further code.


## Manual Testing

- Ensure initial page load is correct, with list of hiscores shown
- Try entering an empty username, see that an error is shown
- Try entering a taken username from hiscore list, see that an error is shown
- Try entering a valid username, see that the game progresses to the first riddle and that username is shown in page header with 0 score
- Answer first riddle with blank answer, see error message and 1 retry
- Answer first riddle with incorrect answer, see error message and no retry, and that game moves to next riddle
- Answer second riddle with correct answer, see success message, next riddle loaded, and score in page header is incremented by 1
- Try loading homepage again at this point, see that you are redirected back to the start of the riddle game with same username, score reset to 0
- Complete game, see that all riddles in json file are asked, answering questions with variations on casing (upper case, lower case, etc.), 
- Checked if score increments successfully with each correct answer,
- Checked if game successfully redirects to '/gameover' after last riddle
- On gameover, see that success message is displayed, that score and username are added to hiscores list
- After gameover, try to load /riddles, see that session has been cleared and new username input is required, redirected to homepage


## Known Limitations/Issues

- Player can hit refresh after getting correct answer and get awarded more points - could be solved by tracking whether user has already played this riddle or not.
- Method of writing hiscores to a file is vulnerable to problems where two users write to that file at the same time, and one of their changes are lost. 
- No way of re-using your old username to play another game
- Players can go directly to gameover at any point by adding '/gameover' to the URL, which clears their session and stores their score
- Using CSS3 animations not displayed on older browsers (although they aren't important to the functionality of the game)



Thank you for visiting my site!

**Enjoy the game!**

Best wishes,

Annie
