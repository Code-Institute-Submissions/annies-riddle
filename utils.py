import json

def check_username(userscores, username):
    '''
    If username was empty or already stored in the user scores file,
    then it is invalid, otherwise it is fine
    '''
    if username == "" or username in userscores:
        return False
    return True

def check_answer(riddle, answer):
    '''
    Check provided answer against the one passed in from main app which
    comes from riddles JSON file. Convert both to lower case to ignore
    casing differences. Also testing only that the correct answer is part of
    user supplied answer, so that answering "a brain" or "the brain" are
    both correct.
    '''
    if riddle["answer"].lower() in answer.lower():
        return True
    else:
        return False

def get_next_riddle(riddles, progress):
    '''
    Loads the next riddle in the list, using progress as an index.
    On initial load, progress is none, so load the first riddle.
    When progress reaches the last index of the riddles list, return None
    so game knows that the game is over. 
    '''
    if progress == None:
        return riddles[0]
    else:
        if progress >= (len(riddles) - 1):
            return None
        else:
            return riddles[progress+1]