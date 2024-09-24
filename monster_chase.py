# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 00:48:51 2024

@author: Dominick Moran
"""
# Monster Chase
#
# A monster is chasing the player. Each turn, the player must solve a math problem within 10 seconds
# in order to keep moving forward. The problems gradually increase in difficulty.
#
# If they move forward 10 times, they will escape and win the game. But if they fail 3 times,
# the monster will gobble them up!
#
# Idea: Consider using nltk and sentiment score ranges instead; correctness is based on whether the player
# can find a word to match a given sentiment score range


# import the necessary packages:
# random to get random numbers for the math problems (and to choose randomly between addition and
# subtraction)
import random
# tkinter for the user interface
import tkinter as tk
# math for rounding numbers up for the timer
import math

# first window explaining the game
intro_window_1 = tk.Tk()
intro_window_1.title('Monster Chase')
intro_window_1.geometry('500x200+500+250')
window_text = tk.Label(intro_window_1, text='A monster is chasing you! In each turn, you must\nsolve '+
                       'a math problem to keep running forward\nand escape him.', font=('Arial', 15))
window_text.place(x=30, y=30)
ok_button = tk.Button(intro_window_1, text='OK', width=20, command=intro_window_1.destroy)
ok_button.place(x=175, y=150)
intro_window_1.mainloop()

# second window explaining the game
intro_window_2 = tk.Tk()
intro_window_2.title('Monster Chase')
intro_window_2.geometry('500x250+500+250')
window_text = tk.Label(intro_window_2, text='10 correct answers will free you from the monster.\n'+
                       'But if you fail 3 times, he\'ll catch up to you and\ngobble you up!\n\n'+
                       'Are you ready?', font=('Arial', 15))
window_text.place(x=30, y=30)
yes_button = tk.Button(intro_window_2, text='Yes', width=20, command=intro_window_2.destroy)
yes_button.place(x=175, y=200)
intro_window_2.mainloop()

# create a list of problems used already so we don't get repeats
probs = []

# structure of the problems to be used when num_successes <= 4
# simple addition or subtraction (least difficult)
def prob_1_thru_4(min_num, max_num_not_incl):
    num_1 = str(random.randrange(min_num, max_num_not_incl))
    plus_minus = '+' if random.random() < 0.5 else '-'
    num_2 = str(random.randrange(min_num, max_num_not_incl))
    return num_1 + plus_minus + num_2

# structure of the problems to be used when 5 <= num_successes <= 7
# multiplication (moderately difficult)
def prob_5_thru_7(min_num, max_num_not_incl):
    num_1 = str(random.randrange(min_num, max_num_not_incl))
    times = '*'
    num_2 = str(random.randrange(min_num, max_num_not_incl))
    return num_1 + times + num_2

# structure of the problems to be used when num_successes >= 8
# multiplication then either addition or subtraction (most difficult)
def prob_8_thru_10(min_num, max_num_not_incl):
    num_1 = str(random.randrange(min_num, max_num_not_incl))
    times = '*'
    num_2 = str(random.randrange(min_num, max_num_not_incl))
    plus_minus = '+' if random.random() < 0.5 else '-'
    num_3 = str(random.randrange(min_num, max_num_not_incl))
    return num_1 + times + num_2 + plus_minus + num_3

# function to run through each math problem
def math_prob(num_successes):
    # define a success (correct player answer) variable that can be used outside this function
    global is_success
    is_success = False
    
    # initialize the problem window
    problem_window = tk.Tk()
    # set the window title, size, and location
    problem_window.title('Problem '+str(num_successes + 1))
    problem_window.geometry('500x270+500+250')
    
    # create text box to contain the problem
    prob_text_box = tk.Text(problem_window, height=1, width=10)
    
    # for the first 2 problems (where num_successes is either 0 or 1 at the time this window appears),
    # use numbers in range 1 through 10 for addition or subtraction
    if num_successes <= 1:
        prob = prob_1_thru_4(1, 11)
        # if current problem was already used, re-roll until we get a brand new problem
        while prob in probs:
            prob = prob_1_thru_4(1, 11)
        probs.append(prob) # add current problem to probs
        prob_text_box.insert('end', prob) # insert problem into text box
    
    # for the next 2 problems (where num_successes is either 2 or 3 at the time this window appears),
    # use numbers in range 1 through 20 for addition or subtraction
    elif num_successes <= 3:
        prob = prob_1_thru_4(1, 21)
        while prob in probs:
            prob = prob_1_thru_4(1, 21)
        probs.append(prob)
        prob_text_box.insert('end', prob)
    
    # for the next 3 problems (where num_successes is between 4 and 6 at the time this window appears),
    # use numbers in range 1 through 10 for multiplication
    elif num_successes <= 6:
        prob = prob_5_thru_7(1, 11)
        while prob in probs:
            prob = prob_5_thru_7(1, 11)
        probs.append(prob)
        prob_text_box.insert('end', prob)
    
    # for the last 3 problems (where num_successes is greater than 6 at the time this window appears),
    # use numbers in range 1 through 10 for multiplication and addition/subtraction
    else:
        prob = prob_8_thru_10(1, 11)
        while prob in probs:
            prob = prob_8_thru_10(1, 11)
        probs.append(prob)
        prob_text_box.insert('end', prob)
    
    # position the text box and make its text read-only
    prob_text_box.place(x=210, y=40)
    prob_text_box.config(state='disabled')
    
    # insert "Answer:" text label
    answer_label = tk.Label(problem_window, text='Answer:', font=('Arial', 15))
    answer_label.place(x=100, y=100)
    
    # define ans_str as a string variable whose value can be changed by the player
    ans_str = tk.StringVar()
    # define a function get_answer to save the current value of ans_str as answer
    def get_answer():
        global answer
        answer = ans_str.get()
    
    # create text box for entering the answer and set its location
    answer_entry_box = tk.Entry(problem_window, textvariable=ans_str, width=13)
    answer_entry_box.place(x=210, y=105)
    
    # create OK button, which when clicked causes the current text in the answer box to be saved
    # and the window to be closed
    ok_button = tk.Button(problem_window, text='OK', width=20, 
                          command=lambda: [get_answer(), problem_window.destroy()])
    ok_button.place(x=175, y=235)
    
    # place the timer label
    timer_label = tk.Label(problem_window, text='Time:', font=('Arial', 15))
    timer_label.place(x=100, y=170)
    
    # Timer logic:
    # We want the timer to count down from 10 to 0, with each value in this range being displayed for
    # about a second. We could count down by actual seconds, in which case the while loop would use the
    # code timer.after(1000) and timer_var -= 1. However, this would cause every user input not to have
    # its effect displayed until after the current timer.after command finishes running. Therefore, we
    # should count down in smaller increments.
    #
    # If the increments are too small, though, the timer may run too slowly. 50-millisecond increments
    # seem to work well.
    
    # initialize timer countdown variable and timer text
    timer_var = 10
    timer = tk.Label(problem_window, text=str(math.ceil(timer_var)), font=('Arial', 15))
    timer.place(x=235, y=170)
    problem_window.update()
    
    # timer countdown
    while timer_var-0.05 > -1: # repeat until timer_var-0.05 rounded up is no longer between 0 and 10
        try:
            timer.after(50)
            timer_var -= 0.05
            timer.config(text=str(math.ceil(timer_var))) # displayed time = actual time left rounded up
            problem_window.update()
        except tk.TclError: # exit loop if the player clicks the OK button and closes the window
            break
    
    # if the player runs out of time, use the string (if there is one) in the answer text box
    # as the answer and close the window
    #
    # problem_window.destroy() will throw a TclError if the OK button is clicked because the window will
    # close before this line can be executed, so just pass in that case
    try:
        get_answer()
        problem_window.destroy()
    except tk.TclError:
        pass
    
    # to make sure the problem window appears and runs as it's supposed to
    problem_window.mainloop()
    
    # windows for a correct answer
    def correct_window(num_correct_answers):
        correct_window = tk.Tk()
        correct_window.geometry('350x150+550+300')
        if num_correct_answers < 9: # while the game is still going
            correct_window.title('Correct!')
            window_text = tk.Label(correct_window, text="Correct! You're one step closer to\n"+
                                   'escaping the monster!', font=('Arial', 15))
            window_text.place(x=25, y=30)
        else: # upon winning the game
            correct_window.title('Congratulations!')
            window_text = tk.Label(correct_window, text="Correct! Now you've escaped\nthe "+
                                   'monster. Congratulations!!', font=('Arial', 15))
            window_text.place(x=35, y=30)
        ok_button = tk.Button(correct_window, text='OK', width=10, command=correct_window.destroy)
        ok_button.place(x=140, y=110)
        correct_window.mainloop()
        
    # windows for an incorrect answer
    def incorrect_window(num_incorrect_answers):
        incorrect_window = tk.Tk()
        if num_incorrect_answers < 2: # while the game is still going
            incorrect_window.title('Incorrect')
            incorrect_window.geometry('350x150+550+300')
            window_text = tk.Label(incorrect_window, text='Sorry, the correct answer was '+
                                   str(eval(prob))+".\nThe monster's catching up to you!", font=
                                   ('Arial', 15))
            window_text.place(x=25, y=30)
            ok_button = tk.Button(incorrect_window, text='OK', width=10, command=incorrect_window.destroy)
            ok_button.place(x=140, y=110)
        else: # upon losing the game
            incorrect_window.title('Game Over')
            incorrect_window.geometry('330x160+550+300')
            window_text = tk.Label(incorrect_window, text='The monster caught up to you\nand '+
                                   'gobbled you up.\nBetter luck next time!', font=('Arial', 15))
            window_text.place(x=35, y=20)
            ok_button = tk.Button(incorrect_window, text='OK', width=10, command=incorrect_window.destroy)
            ok_button.place(x=130, y=120)
        incorrect_window.mainloop()
    
    # evaluate whether player's answer was correct
    try:
        if eval(prob) == int(answer):
            correct_window(num_successes)
            is_success = True
        else:
            incorrect_window(num_failures)
    except: # e.g. if a ValueError is thrown because the player's answer cannot be converted to an int
        incorrect_window(num_failures)

# initialize success and failure counters
num_successes = 0
num_failures = 0

# run through each problem until there have been 10 successes or 3 failures
while num_successes < 10 and num_failures < 3:
    math_prob(num_successes)
    if is_success == True:
        num_successes += 1
    else:
        num_failures += 1
    