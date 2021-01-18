#!/usr/bin/env python3
"""
Programming Class Queue
"""

__author__ = "Steven Yulong Yan"

##################################
# This application is programmed on macOS High Sierra but later adjusted on windows PC.
# Larger monitors are recommended for better visualisation.
# Minor text alignment issues might occur due to font compatibility if you are using a Mac.
# You might encounter issues with button background colour displays if you are using a Mac.
##################################


# ------ Imported Modules ------ #


import time
import random

try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import simpledialog
except ImportError:
    print("You are not using the latest version of python.")

#  ------ GUI Setup (Setting up the root window) ------ #


root = Tk()
root.geometry("1140x690")
root.resizable(0, 0)  # The window is set to be not resizable.
root.title("Programming Class Queue")


# ------ Global Variables ------ #


WINFO_WIDTH = 1140
WINFO_HEIGHT = 690
REFRESH_PERIOD = 3
TARGET_DIAMETER = 20
left_hit = False
right_hit = False
bottom_hit = False
left_win = False
right_win = False
quick_precise_timing = False
long_precise_timing = False
quick_game_temp = None
quick_game_continue = False
long_game_temp = None
long_game_continue = False
quick_average = StringVar()
quick_average.set("No students in queue.")
long_average = StringVar()
long_average.set("No students in queue.")


# ------ Accessible Functions ------ #


def get_row(frame):
    """
    Return the row number of the given frame.
    :param frame: The frame from which the row information retrieves
    :return (int): The row number of the frame
    """
    return frame.grid_info()["row"]


def frame_quick_configure(event):
    """
    Configure the canvas within which the scrollbar is attached to
    the frame for the quick queue.
    """
    canvas_quick_queue.config(scrollregion=canvas_quick_queue.bbox("all"))


def frame_long_configure(event):
    """
    Configure the canvas within which the scrollbar is attached to
    the frame for the long queue.
    """
    canvas_long_queue.config(scrollregion=canvas_long_queue.bbox("all"))


def time_convert(time_digit):
    """
    Convert the time into a desired format.
    :param time_digit: (int) The original time expression
    :return (str): The converted time expression
    """
    if time_digit < 60:
        time_string = "a few seconds"
    elif 60 <= time_digit < 120:
        time_string = "a minute"
    elif 120 <= time_digit < 3600:
        minutes = time_digit // 60
        time_string = "{} minutes".format(minutes)
    elif 3600 <= time_digit < 7200:
        time_string = "1 hour"
    else:
        hours = time_digit // 3600
        time_string = "{} hours".format(hours)
    return time_string


def quick_toggle():
    """
    Control the button settings between two different modes for the quick queue.
    """
    global quick_precise_timing
    if button_quick_timing.config("text")[-1] == "Precise Timing Off":
        button_quick_timing.config(text="Precise Timing On",
                                   bg="#3c763d", highlightbackground="#3c763d")
        quick_precise_timing = True
        time.sleep(REFRESH_PERIOD)
        quick_redraw_accurate()
    else:
        button_quick_timing.config(text="Precise Timing Off",
                                   bg="#c0c1c4", highlightbackground="#c0c1c4")
        quick_precise_timing = False
        time.sleep(REFRESH_PERIOD)
        quick_redraw_approx()


def long_toggle():
    """
    Control the button settings between two different modes for the long queue.
    """
    global long_precise_timing
    if button_long_timing.config("text")[-1] == "Precise Timing Off":
        button_long_timing.config(text="Precise Timing On",
                                  bg="#31708f", highlightbackground="#31708f")
        long_precise_timing = True
        time.sleep(REFRESH_PERIOD)
        long_redraw_accurate()
    else:
        button_long_timing.config(text="Precise Timing Off",
                                  bg="#c0c1c4", highlightbackground="#c0c1c4")
        long_precise_timing = False
        time.sleep(REFRESH_PERIOD)
        long_redraw_approx()


def target_hit_effects(target):
    """
    Configure the concentric circles in the single player game.
    :param target: An instance of the Target Class
    """
    target.master.itemconfig(target.target, fill="#00840b")
    target.master.itemconfig(target.circle_1st, outline="#00c610")
    target.master.itemconfig(target.circle_2nd, outline="#00ff14")
    target.master.itemconfig(target.circle_3rd, outline="#6dff79")


# Alerts #
def name_limit_alert():
    """
    Display the message indicating the input name is too lone.
    """
    messagebox.showerror("Shorten Your Name",
                         "Sorry, your input name must not contain more than 17 characters.\n"
                         "\nPlease try again")


def unaccepted_char_alert():
    """
    Display the message indicating the input name contains special characters.
    """
    messagebox.showerror("Non-recognisable Characters",
                         "Sorry, your input contains at least one unrecognised character.\n"
                         "\nPlease try again.")


def in_self_queue_alert():
    """
    Display the message indicating the user cannot be added in the queue
    if they are already in the queue.
    """
    messagebox.showerror("Already Queued",
                         "Sorry the request is rejected as you are already in the queue.\n"
                         "\nYou cannot have two identities in one queue")


def in_quick_queue_alert():
    """
    Display the message indicating the user cannot enter the long queue
    if they are already in the quick queue.
    :return:
    """
    messagebox.showerror("Already in Another queue",
                         "Sorry the request is rejected as "
                         "you have already requested help in the quick question queue")


def in_long_queue_alert():
    """
    Display the message indicating the user cannot enter the quick queue
    if they are already in the long queue.
    """
    messagebox.showerror("Already in Another queue",
                         "Sorry the request is rejected as "
                         "you have already requested help in the long question queue")


def invalid_name_alert():
    """
    Display the message indicating the input name is not valid.
    """
    messagebox.showerror("Not a Valid Name", "Please enter a valid name in the given field.")


def quick_game_lose_alert():
    """
    Display the message indicating the user has lost the single player game.
    """
    messagebox.showinfo("Game Over", "You have lost.")


def quick_game_win_alert():
    """
    Display the message indicating the user has won the single player game.
    """
    messagebox.showinfo("Game Over", "You have won.")


def long_game_blue_win():
    """
    Display the message indicating the user on the blue side has won in the double player game.
    """
    messagebox.showinfo("Game Over", "The blue side has won.")


def long_game_red_win():
    """
    Display the message indicating the user on the red side has won in the double player game.
    """
    messagebox.showinfo("Game Over", "The red side has won.")


# ------ The Queue Class ------ #


class Queue:
    """
    A queue list
    """
    
    def __init__(self, starting_queue=None):
        """
        Construct a queue list.
        :param starting_queue: The starting queue
        """
        if starting_queue is None:
            starting_queue = []
        self.starting_queue = starting_queue

    def get_queue(self):
        """
        Return the queue list.
        :return (list): The queue list
        """
        return self.starting_queue


# Instantiation
quick_add_queue = Queue()
long_add_queue = Queue()
quick_delete_queue = Queue()
long_delete_queue = Queue()


# ------ Quick Question Queue ------ #


class QuickRecipient:
    """
    A recipient in the quick question queue
    """

    def __init__(self, name, question, starting_time):
        """
        Construct a recipient in the quick question queue.
        :param name (str): The name of the recipient
        :param question (int): The number of questions answered of the recipient
        :param starting_time (int): The time when the recipient enters the queue
        """
        self.name = name
        self.question = question
        self.starting_time = starting_time
        self.frame = Frame(frame_quick_queue, width=515, height=30)
        self.frame.grid(sticky=W)
        self.label_row = Label(self.frame, text=get_row(self.frame) + 1)
        self.label_row.place(x=0, y=3)
        self.label_name = Label(self.frame, text=self.name)
        self.label_name.place(x=30, y=3)
        self.label_question = Label(self.frame, text=self.question)
        self.label_question.place(x=200, y=3)
        self.label_time = Label(self.frame, text=self.starting_time)
        self.label_time.place(x=305, y=3)
        self.cancel_button = Button(self.frame, bg="red", highlightbackground="red")
        self.cancel_button.config(text="    ", cursor="hand2", command=self.cancel)
        self.cancel_button.place(x=450, y=3)
        self.confirm_button = Button(self.frame, bg="green", highlightbackground="green")
        self.confirm_button.config(text="    ", cursor="hand2", command=self.confirm)
        self.confirm_button.place(x=475, y=3)

    def cancel(self):
        """
        Remove the recipient from the question queue.
        """
        for recipient in quick_add_queue.get_queue():
            if recipient[0] == self.name:
                quick_add_queue.get_queue().remove(recipient)
        self.frame.destroy()

    def confirm(self):
        """
        Remove the recipient from the question queue and store it in a dump queue.
        """
        for recipient in quick_add_queue.get_queue():
            if recipient[0] == self.name:
                quick_add_queue.get_queue().remove(recipient)
                quick_delete_queue.get_queue().append(recipient)
        self.frame.destroy()


def quick_get_name():
    """
    Display a text dialog window and pass on the entry for the quick queue.
    """
    name = simpledialog.askstring(" ", "What is your name?", initialvalue="e.g. Peter O'Shea")
    quick_verify_name(name)


def quick_verify_name(name):
    """
    Verify the entry and pass on the name for the quick queue.
    Display alert messages if it fails verification.
    :param name: The user input name
    """
    try:
        if len(name) > 17:
            name_limit_alert()
            quick_get_name()
        elif (all(char.isalpha() or char == " " or char == "'" for char in name) and
              not all(char.isspace() for char in name)):
            quick_ask(name)
        elif (char == "." for char in name) and not all(char.isspace() for char in name):
            unaccepted_char_alert()
            quick_get_name()
        else:
            invalid_name_alert()
            quick_get_name()
    except TypeError:
        pass


def quick_ask(name):
    """
    1. If the name is found to be already in some queue then raise alerts accordingly.
    2. If the name is found in the dump queue then count the number
       and store it as the number of questions answered.
    3. Record the time when the recipient enters the queue
    4. Instantiate from the queue class and store the corresponding attributes.
    5. Execute the accurate or approximate time mode accordingly for the quick queue.
    :param name: The verified input name
    """
    if any(recipient[0] == name for recipient in quick_add_queue.get_queue()):
        return in_self_queue_alert()
    if any(recipient[0] == name for recipient in long_add_queue.get_queue()):
        return in_long_queue_alert()
    questions_asked = 0
    for recipient in quick_delete_queue.get_queue():
        if recipient[0] == name:
            questions_asked += 1
    start_time = time.time()
    quick_add_queue.get_queue().append((name, questions_asked, round(start_time)))
    if quick_precise_timing:
        quick_redraw_accurate(True)
    else:
        quick_redraw_approx(True)


def quick_redraw_accurate(new_entry=False):
    """
    1. Sort the queue list according to firstly questions answered in ascending order
       and secondly the time elapsed in descending order.
    2. Calculate the average wait time.
    3. Refresh this process for the quick queue and perform the accurate display.
    :param new_entry: Determines if it is a new entry.
    """
    global quick_precise_timing
    queue_list = quick_add_queue.get_queue()
    sorted_queue_list = sorted(sorted(queue_list, key=lambda x: x[2]), key=lambda x: x[1])
    sum_time = 0
    for frame in frame_quick_queue.winfo_children():
        frame.destroy()
    for recipient in sorted_queue_list:
        end_time = time.time()
        elapsed_time = round(end_time) - recipient[2]
        sum_time += elapsed_time
        if elapsed_time == 0:
            QuickRecipient(recipient[0], recipient[1], "{} second ago".format(elapsed_time))
        else:
            QuickRecipient(recipient[0], recipient[1], "{} seconds ago".format(elapsed_time))
    try:
        recipient_number = len(sorted_queue_list)
        average_wait_time = sum_time // recipient_number
        if recipient_number == 1:
            if average_wait_time == 0:
                quick_average.set("An average wait time of {} second for 1 student."
                                  .format(average_wait_time))
            else:
                quick_average.set("An average wait time of {} seconds for 1 student."
                                  .format(average_wait_time))
        elif recipient_number > 1:
            quick_average.set("An average wait time of about {} seconds "
                              "for {} students"
                              .format(average_wait_time, recipient_number))
    except ZeroDivisionError:
        pass
    if not new_entry:
        if quick_precise_timing:
            root.after(REFRESH_PERIOD * 1000, quick_redraw_accurate)


def quick_redraw_approx(new_entry=False):
    """
    1. Sort the queue list according to firstly questions answered in ascending order
       and secondly the time elapsed in descending order.
    2. Calculate the average wait time.
    3. Refresh this process for the quick queue and perform the approximate display.
    :param new_entry: Determines if it is a new entry.
    """
    global quick_precise_timing
    quick_queue_list = quick_add_queue.get_queue()
    quick_sorted_queue_list = sorted(sorted(quick_queue_list, key=lambda x: x[2]), key=lambda x: x[1])
    sum_time = 0
    for frame in frame_quick_queue.winfo_children():
        frame.destroy()
    for recipient in quick_sorted_queue_list:
        end_time = time.time()
        elapsed_time = round(end_time) - recipient[2]
        sum_time += elapsed_time
        QuickRecipient(recipient[0], recipient[1], "{} ago".format(time_convert(elapsed_time)))
    try:
        recipient_number = len(quick_sorted_queue_list)
        average_wait_time = sum_time // recipient_number
        if recipient_number == 1:
            quick_average.set("An average wait time of {} for 1 student."
                              .format(time_convert(average_wait_time)))
        elif recipient_number > 1:
            quick_average.set("An average wait time of about {} "
                              "for {} students"
                              .format(time_convert(average_wait_time), recipient_number))
    except ZeroDivisionError:
        pass
    if not new_entry:
        if not quick_precise_timing:
            root.after(REFRESH_PERIOD * 1000, quick_redraw_approx)


# If precise timing is switched on perform the accurate mode, otherwise perform the approximate mode.
if quick_precise_timing:
    root.after(REFRESH_PERIOD * 1000, quick_redraw_accurate)
else:
    root.after(REFRESH_PERIOD * 1000, quick_redraw_approx)


# ------ Long Question Queue ------ #


class LongRecipient:
    """
    A recipient in the long question queue
    """

    def __init__(self, name, question, starting_time):
        """
        Construct a recipient in the long question queue.
        :param name (str): The name of the recipient
        :param question (int): The number of questions answered of the recipient
        :param starting_time (int): The time when the recipient enters the queue
        """
        self.name = name
        self.question = question
        self.starting_time = starting_time
        self.frame = Frame(frame_long_queue, width=515, height=30)
        self.frame.grid(sticky=W)
        self.label_row = Label(self.frame, text=get_row(self.frame) + 1)
        self.label_row.place(x=0, y=3)
        self.label_name = Label(self.frame, text=self.name)
        self.label_name.place(x=30, y=3)
        self.label_question = Label(self.frame, text=self.question)
        self.label_question.place(x=200, y=3)
        self.label_time = Label(self.frame, text=self.starting_time)
        self.label_time.place(x=305, y=3)
        self.cancel_button = Button(self.frame, bg="red", highlightbackground="red")
        self.cancel_button.config(text="    ", cursor="hand2", command=self.cancel)
        self.cancel_button.place(x=450, y=3)
        self.confirm_button = Button(self.frame, bg="green", highlightbackground="green")
        self.confirm_button.config(text="    ", cursor="hand2", command=self.confirm)
        self.confirm_button.place(x=475, y=3)

    def cancel(self):
        """
        Remove the recipient from the question queue.
        """
        for recipient in long_add_queue.get_queue():
            if recipient[0] == self.name:
                long_add_queue.get_queue().remove(recipient)
        self.frame.destroy()

    def confirm(self):
        """
        Remove the recipient from the question queue and store it in a dump queue.
        """
        for recipient in long_add_queue.get_queue():
            if recipient[0] == self.name:
                long_add_queue.get_queue().remove(recipient)
                long_delete_queue.get_queue().append(recipient)
        self.frame.destroy()


def long_get_name():
    """
    Display a text dialog window and pass on the entry for the long queue.
    """
    name = simpledialog.askstring(" ", "What is your name?", initialvalue="e.g. Peter O'Shea")
    long_verify_name(name)


def long_verify_name(name):
    """
    Verify the entry and pass on the name for the long queue. Display alert messages if it fails verification.
    :param name: The user input name
    """
    try:
        if len(name) > 17:
            name_limit_alert()
            long_get_name()
        elif (all(char.isalpha() or char == " " or char == "'" for char in name) and
              not all(char.isspace() for char in name)):
            long_ask(name)
        elif (char == "." for char in name) and not all(char.isspace() for char in name):
            unaccepted_char_alert()
            long_get_name()
        else:
            invalid_name_alert()
            long_get_name()
    except TypeError:
        pass


def long_ask(name):
    """
    1. If the name is found to be already in some queue then raise alerts accordingly.
    2. If the name is found in the dump queue then count the number
       and store it as the number of questions answered.
    3. Record the time when the recipient enters the queue
    4. Instantiate from the queue class and store the corresponding attributes.
    5. Execute the accurate or approximate time mode accordingly for the long queue.
    :param name: The verified input name
    """
    if any(recipient[0] == name for recipient in long_add_queue.get_queue()):
        return in_self_queue_alert()
    if any(recipient[0] == name for recipient in quick_add_queue.get_queue()):
        return in_quick_queue_alert()
    questions_asked = 0
    for recipient in long_delete_queue.get_queue():
        if recipient[0] == name:
            questions_asked += 1
    start_time = time.time()
    long_add_queue.get_queue().append((name, questions_asked, round(start_time)))
    if long_precise_timing:
        long_redraw_accurate(True)
    else:
        long_redraw_approx(True)


def long_redraw_accurate(new_entry=False):
    """
    1. Sort the queue list according to firstly questions answered in ascending order
       and secondly the time elapsed in descending order.
    2. Calculate the average wait time.
    3. Refresh this process for the long queue and perform the accurate display.
    :param new_entry: Determines if it is a new entry.
    """
    global long_precise_timing
    long_queue_list = long_add_queue.get_queue()
    long_sorted_queue_list = sorted(sorted(long_queue_list, key=lambda x: x[2]), key=lambda x: x[1])
    sum_time = 0
    for frame in frame_long_queue.winfo_children():
        frame.destroy()
    for recipient in long_sorted_queue_list:
        end_time = time.time()
        elapsed_time = round(end_time) - recipient[2]
        sum_time += elapsed_time
        if elapsed_time == 0:
            LongRecipient(recipient[0], recipient[1], "{} second ago".format(elapsed_time))
        else:
            LongRecipient(recipient[0], recipient[1], "{} seconds ago".format(elapsed_time))
    try:
        recipient_number = len(long_sorted_queue_list)
        average_wait_time = sum_time // recipient_number
        if recipient_number == 1:
            if average_wait_time == 0:
                long_average.set("An average wait time of {} second for 1 student."
                                 .format(average_wait_time))
            else:
                long_average.set("An average wait time of {} seconds for 1 student."
                                 .format(average_wait_time))
        elif recipient_number > 1:
            long_average.set("An average wait time of about {} seconds "
                             "for {} students"
                             .format(average_wait_time, recipient_number))
    except ZeroDivisionError:
        pass
    if not new_entry:
        if long_precise_timing:
            root.after(REFRESH_PERIOD * 1000, long_redraw_accurate)


def long_redraw_approx(new_entry=False):
    """
    1. Sort the queue list according to firstly questions answered in ascending order
       and secondly the time elapsed in descending order.
    2. Calculate the average wait time.
    3. Refresh this process for the long queue and perform the accurate display.
    :param new_entry: Determines if it is a new entry.
    """
    global long_precise_timing
    queue_list = long_add_queue.get_queue()
    sorted_queue_list = sorted(sorted(queue_list, key=lambda x: x[2]), key=lambda x: x[1])
    sum_time = 0
    for frame in frame_long_queue.winfo_children():
        frame.destroy()
    for recipient in sorted_queue_list:
        end_time = time.time()
        elapsed_time = round(end_time) - recipient[2]
        sum_time += elapsed_time
        LongRecipient(recipient[0], recipient[1], "{} ago".format(time_convert(elapsed_time)))
    try:
        recipient_number = len(sorted_queue_list)
        average_wait_time = sum_time // recipient_number
        if recipient_number == 1:
            long_average.set("An average wait time of {} for 1 student."
                             .format(time_convert(average_wait_time)))
        elif recipient_number > 1:
            long_average.set("An average wait time of about {} "
                             "for {} students"
                             .format(time_convert(average_wait_time), recipient_number))
    except ZeroDivisionError:
        pass
    if not new_entry:
        if not long_precise_timing:
            root.after(REFRESH_PERIOD * 1000, long_redraw_approx)


# If precise timing is switched on perform the accurate mode, otherwise perform the approximate mode.
if long_precise_timing:
    root.after(REFRESH_PERIOD * 1000, long_redraw_accurate)
else:
    root.after(REFRESH_PERIOD * 1000, long_redraw_approx)


# ------ Quick Question Game (Paddle Ball Game with A Single Player) ------ #


class Sphere:
    """
    A sphere that bounces back when hitting objects with boundaries
    """

    def __init__(self, master, platform, target_left, target_right):
        """
        Construct a sphere that moves.
        :param master: The parent to contain the sphere object
        :param platform: An instance of the Platform Class
        :param target_left: An instance of the Target Class
        :param target_right: An instance of the Target Class
        """
        self.master = master
        self.platform = platform
        self.target_left = target_left
        self.target_right = target_right
        self.sphere = self.master.create_oval(0, 0, 25, 25, fill="#f765b3")
        self.master.move(self.sphere, 565, 300)
        self.direction_x = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        self.direction_y = -4

    def move(self):
        """
        Reverse the direction when hitting boundaries and
        reset relevant variables if a target is hit.
        """
        global left_hit
        global right_hit
        global bottom_hit
        try:
            self.master.move(self.sphere, self.direction_x, self.direction_y)
            sphere_position = self.master.coords(self.sphere)
            # The sphere hits the top edge of the board.
            if sphere_position[1] <= 0:
                self.direction_y = 4
            # The sphere hits the bottom edge of the board.
            if sphere_position[3] >= WINFO_HEIGHT:
                bottom_hit = True
            # The sphere hits the left boundary of the board.
            if sphere_position[0] <= 0:
                self.direction_x = 4
            # The sphere hits the right boundary of the board.
            if sphere_position[2] >= WINFO_WIDTH:
                self.direction_x = -4
            # The sphere collides with the surface of the platform.
            if self.collision(sphere_position):
                self.direction_y = -4
            if self.hit_left_target(sphere_position):
                left_hit = True
            if self.hit_right_target(sphere_position):
                right_hit = True
        except TclError:
            pass

    def collision(self, sphere_position):
        """
        Return True if the sphere is caught by the platform and False otherwise.
        :param sphere_position: The position of the sphere
        :return: True if the sphere is caught by the platform and False otherwise
        """
        platform_position = self.master.coords(self.platform.platform)
        # The right side of the sphere meets the left side of the platform
        if (sphere_position[2] >= platform_position[0] and
                # The left side of the sphere meets the right side of the platform
                sphere_position[0] <= platform_position[2] and
                # The bottom of the sphere hits the surface of the platform but is not below the platform
                platform_position[1] <= sphere_position[3] <= platform_position[3]):
            return True
        else:
            return False

    def hit_left_target(self, sphere_position):
        """
        Return True if the sphere hits the left target and False otherwise.
        :param sphere_position: The position of the sphere
        :return: True if the sphere hits the left target and False otherwise
        """
        left_target_position = self.master.coords(self.target_left.circle_1st)
        # The sphere is inside the target circle
        if (sphere_position[0] >= left_target_position[0] and
                sphere_position[1] >= left_target_position[1] and
                sphere_position[2] <= left_target_position[2] and
                sphere_position[3] <= left_target_position[3]):
            return True
        else:
            return False

    def hit_right_target(self, sphere_position):
        """
        Return True if the sphere hits the right target and False otherwise.
        :param sphere_position: The position of the sphere
        :return: True if the sphere hits the right target and False otherwise
        """
        right_target_position = self.master.coords(self.target_right.circle_1st)
        # The sphere is inside the target circle
        if (sphere_position[0] >= right_target_position[0] and
                sphere_position[1] >= right_target_position[1] and
                sphere_position[2] <= right_target_position[2] and
                sphere_position[3] <= right_target_position[3]):
            return True
        else:
            return False


class Target:
    """
    A target for the moving sphere
    """

    def __init__(self, master, position_x, position_y):
        """
        Construct a target for the moving sphere.
        :param master: The parent to place the target object
        :param position_x: The factor-x of the position of the target
        :param position_y: The factor-y of the position of the target
        """
        self.master = master
        self.position_x = position_x
        self.position_y = position_y
        self.target = self.master.create_oval(0, 0, TARGET_DIAMETER, TARGET_DIAMETER, fill="#ff0000")
        self.circle_1st = self.master.create_oval(0, 0, TARGET_DIAMETER * 3, TARGET_DIAMETER * 3,
                                                  outline="#ff2626", width=6)
        self.circle_2nd = self.master.create_oval(0, 0, TARGET_DIAMETER * 6, TARGET_DIAMETER * 6,
                                                  outline="#ff4747", width=3)
        self.circle_3rd = self.master.create_oval(0, 0, TARGET_DIAMETER * 9, TARGET_DIAMETER * 9,
                                                  outline="#ff4747", width=2)
        self.master.move(self.target, self.position_x, self.position_y)
        self.master.move(self.circle_1st, self.position_x - TARGET_DIAMETER, self.position_y - TARGET_DIAMETER)
        self.master.move(self.circle_2nd,
                         self.position_x - TARGET_DIAMETER * 2.5, self.position_y - TARGET_DIAMETER * 2.5)
        self.master.move(self.circle_3rd,
                         self.position_x - TARGET_DIAMETER * 4, self.position_y - TARGET_DIAMETER * 4)


class Platform:
    """
    A platform to catch the sphere and make it bounce back
    """

    def __init__(self, master):
        """
        Construct of platform to catch the sphere.
        :param master: The parent to place the platform object
        """
        self.master = master
        self.platform = self.master.create_rectangle(0, 0, 150, 10, fill="#0faa01")
        self.master.move(self.platform, 510, 600)
        self.direction_x = 0
        self.master.bind_all("<KeyPress-Left>", self.move_left)
        self.master.bind_all("<KeyPress-Right>", self.move_right)
        self.master.bind_all("<KeyPress-Down>", self.pause)

    def move(self):
        """
        Pause the motion of the platform when it reaches the left or right boundary.
        """
        try:
            self.master.move(self.platform, self.direction_x, 0)
            platform_position = self.master.coords(self.platform)
            # The platform hits the left boundary.
            if platform_position[0] <= 0:
                self.direction_x = 0
            # The platform hits the right boundary.
            if platform_position[2] >= WINFO_WIDTH:
                self.direction_x = 0
        except TclError:
            pass

    def pause(self, event):
        """
        Pause the platform motion.
        """
        self.direction_x = 0

    def move_left(self, event):
        """
        Set the platform direction to left.
        """
        self.direction_x = -4

    def move_right(self, event):
        """
        Set the platform direction to right.
        """
        self.direction_x = 4


def quick_game():
    """
    1. Create a new top-level window.
    2. Initiate a canvas for the game.
    3. Instantiate new widgets on the canvas
    4. Call game_start function upon clicking.
    """
    global quick_game_temp
    quick_game_temp = Toplevel()
    quick_game_temp.geometry("1140x690")
    quick_game_temp.resizable(0, 0)
    quick_game_temp.title("Paddle Ball - Single Player")
    canvas_quick_game = Canvas(quick_game_temp,
                               width=WINFO_WIDTH, height=WINFO_HEIGHT,
                               bd=0, highlightthickness=0)
    canvas_quick_game.place(x=0, y=0)
    canvas_quick_game.create_text(590, 400, text="<Left Arrow>, <Right Arrow> and <Down Arrow> buttons "
                                                 "make the paddle move left, move right and pause.",
                                  font="Arial 18")
    canvas_quick_game.create_text(580, 500, fill="#ea3a09", text="Click to start!",
                                  font="Times 30 bold")
    platform = Platform(canvas_quick_game)
    target_left = Target(canvas_quick_game, 285, 100)
    target_right = Target(canvas_quick_game, 855, 100)
    Sphere(canvas_quick_game, platform, target_left, target_right)
    quick_game_temp.bind("<Button-1>", quick_game_start)


def quick_game_start(event):
    """
    Unveil the game.
    """
    global quick_game_continue
    quick_game_continue = True
    quick_game_temp.destroy()
    quick_game_action()


def quick_game_action():
    """
    1. Re-initiate the canvas and its widgets.
    2. Keep the game in motion until certain conditions are met.
    3. End the game with prompt up windows and reset variables.
    """
    global quick_game_continue
    global left_hit
    global right_hit
    global bottom_hit
    quick_game_single = Toplevel()
    quick_game_single.geometry("1140x690")
    quick_game_single.resizable(0, 0)
    quick_game_single.title("Paddle Ball - Single Player")
    canvas_quick_game = Canvas(quick_game_single,
                               width=WINFO_WIDTH, height=WINFO_HEIGHT,
                               bd=0, highlightthickness=0)
    canvas_quick_game.place(x=0, y=0)
    platform = Platform(canvas_quick_game)
    target_left = Target(canvas_quick_game, 285, 100)
    target_right = Target(canvas_quick_game, 855, 100)
    sphere = Sphere(canvas_quick_game, platform, target_left, target_right)
    while quick_game_continue:
        sphere.move()
        platform.move()
        try:
            if left_hit:
                target_hit_effects(target_left)
        except TclError:
            pass
        try:
            if right_hit:
                target_hit_effects(target_right)
        except TclError:
            pass
        if bottom_hit:
            time.sleep(0.5)
            quick_game_lose_alert()
            quick_game_single.destroy()
            left_hit = False
            right_hit = False
            bottom_hit = False
        if left_hit and right_hit:
            time.sleep(0.5)
            quick_game_win_alert()
            quick_game_single.destroy()
            left_hit = False
            right_hit = False
        try:
            quick_game_single.update_idletasks()
            quick_game_single.update()
        except TclError:
            quick_game_continue = False
        time.sleep(0.01)


# ------ Long Question Game (Paddle Ball Game with Double Players) ------ #


class Ball:
    """
    A ball to keeping bouncing between the two paddles
    """

    def __init__(self, master, left_paddle, right_paddle):
        """
        Construct a ball in motion.
        :param master: The parent to hold the ball object
        :param left_paddle: An instance of the LeftPaddle Class
        :param right_paddle: An instance of the RightPaddle Class
        """
        self.master = master
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
        self.ball = self.master.create_oval(0, 0, 15, 15, fill="#cf11f9")
        self.master.move(self.ball, 563, 330)
        self.direction_x = random.choice([-4, 4])
        self.direction_y = random.choice([-4, 4])

    def move(self):
        """
        Reverse the direction when hitting boundaries and
        reset relevant variables if there is a winning situation.
        """
        global left_win
        global right_win
        try:
            self.master.move(self.ball, self.direction_x, self.direction_y)
            ball_position = self.master.coords(self.ball)
            # The ball hits the top edge of the board.
            if ball_position[1] <= 0:
                self.direction_y = 4
            # The ball hits the bottom edge of the board.
            if ball_position[3] >= WINFO_HEIGHT:
                self.direction_y = -4
            # The ball hits the left boundary of the board.
            if ball_position[0] <= 0:
                right_win = True
            # The ball hits the right boundary of the board.
            if ball_position[2] >= WINFO_WIDTH:
                left_win = True
            if self.hit_left_paddle(ball_position):
                self.direction_x = 4
            if self.hit_right_paddle(ball_position):
                self.direction_x = -4
        except TclError:
            pass

    def hit_left_paddle(self, ball_position):
        """
        Check if the ball is caught by the left paddle.
        :param ball_position: The position of the ball
        :return: True if if the ball is caught by the left paddle and False otherwise.
        """
        left_paddle_position = self.master.coords(self.left_paddle.left_paddle)
        # The bottom of the ball meets the top of the paddle
        if (ball_position[3] >= left_paddle_position[1] and
                # The top of the ball meets the bottom of the paddle
                ball_position[1] <= left_paddle_position[3] and
                # The ball touches the surface of the paddle
                ball_position[0] <= left_paddle_position[2]):
            return True
        return False

    def hit_right_paddle(self, ball_position):
        """
        Check if the ball is caught by the right paddle.
        :param ball_position: The position of the ball
        :return: True if if the ball is caught by the left paddle and False otherwise.
        """
        right_paddle_position = self.master.coords(self.right_paddle.right_paddle)
        # The bottom of the ball meets the top of the paddle
        if (ball_position[3] >= right_paddle_position[1] and
                # The top of the ball meets the bottom of the paddle
                ball_position[1] <= right_paddle_position[3] and
                # The ball touches the surface of the paddle
                ball_position[2] >= right_paddle_position[0]):
            return True
        return False


class LeftPaddle:
    """
    A left paddle featured with a colour of red
    """
    def __init__(self, master):
        """
        Construct a paddle for the player on the red side.
        :param master: The parent to position the paddle
        """
        self.master = master
        self.left_paddle = self.master.create_rectangle(0, 0, 20, 100, fill="#ff2828")
        self.master.move(self.left_paddle, 0, 290)
        self.direction_y = 0
        self.master.bind_all("w", self.move_up)
        self.master.bind_all("s", self.move_down)
        self.master.bind_all("a", self.pause)

    def move(self):
        """
        Reverse the moving direction when the paddle hits the top or bottom boundary.
        """
        try:
            self.master.move(self.left_paddle, 0, self.direction_y)
            left_paddle_position = self.master.coords(self.left_paddle)
            # Pause the paddle if it reaches the top end of the screen
            if left_paddle_position[1] <= 0:
                self.direction_y = 0
            # Pause the paddle if it reaches the bottom end of the screen
            if left_paddle_position[3] >= WINFO_HEIGHT:
                self.direction_y = 0
        except TclError:
            pass

    def pause(self, event):
        """
        Pause the paddle motion.
        """
        self.direction_y = 0

    def move_up(self, event):
        """
        Set the paddle direction to North.
        """
        self.direction_y = -3

    def move_down(self, event):
        """
        Set the paddle direction to South.
        """
        self.direction_y = 3


class RightPaddle:
    """
    A right paddle featured with a colour of blue
    """
    def __init__(self, master):
        """
        Construct a paddle for the player on the blue side.
        :param master: The parent to position the paddle
        """
        self.master = master
        self.right_paddle = self.master.create_rectangle(0, 0, 20, 100, fill="#5e3aff")
        self.master.move(self.right_paddle, 1120, 290)
        self.direction_y = 0
        self.master.bind_all("<KeyPress-Up>", self.move_up)
        self.master.bind_all("<KeyPress-Down>", self.move_down)
        self.master.bind_all("<KeyPress-Right>", self.pause)

    def move(self):
        """
        Reverse the moving direction when the paddle hits the top or bottom boundary.
        """
        try:
            self.master.move(self.right_paddle, 0, self.direction_y)
            right_paddle_position = self.master.coords(self.right_paddle)
            # Pause the paddle if it reaches the top end of the screen
            if right_paddle_position[1] <= 0:
                self.direction_y = 0
            # Pause the paddle if it reaches the bottom end of the screen
            if right_paddle_position[3] >= WINFO_HEIGHT:
                self.direction_y = 0
        except TclError:
            pass

    def pause(self, event):
        """
        Pause the paddle motion.
        """
        self.direction_y = 0

    def move_up(self, event):
        self.direction_y = -3

    def move_down(self, event):
        self.direction_y = 3


def long_game():
    """
    1. Create a new top-level window.
    2. Initiate a canvas for the game.
    3. Instantiate new widgets on the canvas
    4. Call game_start function upon clicking.
    """
    global long_game_temp
    long_game_temp = Toplevel()
    long_game_temp.geometry("1140x690")
    long_game_temp.resizable(0, 0)
    long_game_temp.title("Paddle Ball - Double Player")
    canvas_long_game = Canvas(long_game_temp,
                              width=WINFO_WIDTH, height=WINFO_HEIGHT,
                              bd=0, highlightthickness=0)
    canvas_long_game.place(x=0, y=0)
    canvas_long_game.create_line(570, 0, 570, WINFO_HEIGHT, fill="#000")
    canvas_long_game.create_text(590, 200, text="<W>, <S> and <A> buttons make the "
                                                "red paddle move up, move down and pause.",
                                 font="Arial 18")
    canvas_long_game.create_text(590, 240, text="<Up Arrow>, <Down Arrow> and <Right Arrow> buttons "
                                                "make the blue paddle move up, move down and pause.",
                                 font="Arial 18")
    canvas_long_game.create_text(575, 460, fill="#ea3a09", text="Click to start!",
                                 font="Times 30 bold")
    left_paddle = LeftPaddle(canvas_long_game)
    right_paddle = RightPaddle(canvas_long_game)
    Ball(canvas_long_game, left_paddle, right_paddle)
    long_game_temp.bind("<Button-1>", long_game_start)


def long_game_start(event):
    """
    Unveil the game.
    """
    global long_game_continue
    long_game_continue = True
    long_game_temp.destroy()
    long_game_action()


def long_game_action():
    """
    1. Re-initiate the canvas and its widgets.
    2. Keep the game in motion until certain conditions are met.
    3. End the game with prompt up windows and reset variables.
    """
    global long_game_continue
    global left_win
    global right_win
    long_game_double = Toplevel()
    long_game_double.geometry("1140x690")
    long_game_double.resizable(0, 0)
    long_game_double.title("Paddle Ball - Double Player")
    canvas_long_game = Canvas(long_game_double,
                              width=WINFO_WIDTH, height=WINFO_HEIGHT,
                              bd=0, highlightthickness=0)
    canvas_long_game.place(x=0, y=0)
    canvas_long_game.create_line(570, 0, 570, WINFO_HEIGHT, fill="#000")
    left_paddle = LeftPaddle(canvas_long_game)
    right_paddle = RightPaddle(canvas_long_game)
    ball = Ball(canvas_long_game, left_paddle, right_paddle)
    while long_game_continue:
        ball.move()
        left_paddle.move()
        right_paddle.move()
        if left_win:
            time.sleep(0.5)
            long_game_red_win()
            long_game_double.destroy()
            left_win = False
        if right_win:
            time.sleep(0.5)
            long_game_blue_win()
            long_game_double.destroy()
            right_win = False
        try:
            long_game_double.update_idletasks()
            long_game_double.update()
        except TclError:
            long_game_continue = False
        time.sleep(0.01)


# ------ GUI Interface (Basic universal containers and displays) ------ #


# Important Notice (featured with a yellow background)
frame_important = Frame(root, width=WINFO_WIDTH, height=100, bg="#fefbed")
frame_important.place(x=0, y=0)

label_important_heading = Label(frame_important)
label_important_heading.config(fg="#C09853", bg="#fefbed", font="Helvetica 15 bold")
label_important_heading.config(text="Announcement Board")
label_important_heading.place(x=15, y=10)

label_important_content = Label(frame_important)
label_important_content.config(bg="#fefbed", wraplength=1110, justify=LEFT)
label_important_content.config(text="Yesterday morning the marks and feedback for Assignment 3 were released on "
                                    "Blackboard, but there was a bug which was causing some students to be unable to "
                                    "view their feedback. The bug has been fixed and hopefully all students can now "
                                    "see their feedback.")
label_important_content.place(x=15, y=40)

# Quick Question Heading (featured with a green background)
frame_quick_questions = Frame(root, width=530, height=100, bg="#dff0d8")
frame_quick_questions.place(x=20, y=120)

label_quick_questions = Label(frame_quick_questions)
label_quick_questions.config(fg="#3c763d", bg="#dff0d8", font="Helvetica 25")
label_quick_questions.config(text="Quick Questions")
label_quick_questions.place(x=150, y=10)

# Quick Question Subtitle (featured with a font colour of grey on a green background)
label_quick_subs = Label(frame_quick_questions)
label_quick_subs.config(fg="#666", bg="#dff0d8", font="Arial 14 italic")
label_quick_subs.config(text="< 2 mins with a tutor")
label_quick_subs.place(x=170, y=60)

# Long Question Heading (featured with a blue background)
frame_long_questions = Frame(root, width=530, height=100, bg="#d9edf7")
frame_long_questions.place(x=590, y=120)

label_long_questions = Label(frame_long_questions)
label_long_questions.config(fg="#31708f", bg="#d9edf7", font="Helvetica 25")
label_long_questions.config(text="Long Questions")
label_long_questions.place(x=150, y=10)

# Long Question Subtitle (featured with a font colour of grey on a blue background)
label_long_subs = Label(frame_long_questions)
label_long_subs.config(fg="#666", bg="#d9edf7", font="Arial 14 italic")
label_long_subs.config(text="> 2 mins with a tutor")
label_long_subs.place(x=170, y=60)

# Quick Question Instructions (contains 4 bullet points)
frame_quick_instructions = Frame(root, width=530, height=190)
frame_quick_instructions.place(x=20, y=240)

label_quick_instruction_heading = Label(frame_quick_instructions)
label_quick_instruction_heading.config(text="Some examples of quick questions:")
label_quick_instruction_heading.place(x=0, y=0)

quick_instructions = ["    \u2022 Syntax errors",
                      "    \u2022 Interpreting error output",
                      "    \u2022 Assignment interpretation",
                      "    \u2022 Assignment submission issues"]
for i in range(len(quick_instructions)):
    label_instruction = Label(frame_quick_instructions)
    label_instruction.config(text=quick_instructions[i])
    label_instruction.place(x=0, y=20 * (i + 1))

# Request Quick Help Button (featured with a font colour of white on a green button background)
button_quick = Button(frame_quick_instructions)
button_quick.config(fg="#fff", bg="#5cb85c", highlightbackground="#5cb85c", padx=10, pady=10)
button_quick.config(cursor="hand2", command=quick_get_name)
button_quick.config(text="Request Quick Help")
button_quick.place(x=180, y=135)

# Game Button on the Quick Help Section (featured with a font colour of white on a green button background)
button_quick_game = Button(frame_quick_instructions)
button_quick_game.config(fg="#fff", bg="#f765b3", highlightbackground="#f765b3", padx=10, pady=10)
button_quick_game.config(cursor="hand2", command=quick_game)
button_quick_game.config(text="Play Game")
button_quick_game.place(x=380, y=135)

# Long Question Instructions (contains 4 bullet points)
frame_long_instructions = Frame(root, width=530, height=210)
frame_long_instructions.place(x=590, y=240)

label_long_instruction_heading = Label(frame_long_instructions)
label_long_instruction_heading.config(text="Some examples of long questions:")
label_long_instruction_heading.place(x=0, y=0)

long_instructions = ["    \u2022 Open ended questions:",
                     "    \u2022 How to start a problem",
                     "    \u2022 How to improve code",
                     "    \u2022 Debugging",
                     "    \u2022 Assignment help"]
for i in range(len(long_instructions)):
    label_instruction = Label(frame_long_instructions)
    label_instruction.config(text=long_instructions[i])
    label_instruction.place(x=0, y=20 * (i + 1))

# Request Long Help Button (featured with a font colour of white on a blue button background)
button_long = Button(frame_long_instructions)
button_long.config(fg="#fff", bg="#5bc0de", highlightbackground="#5bc0de", padx=10, pady=10)
button_long.config(cursor="hand2", command=long_get_name)
button_long.config(text="Request Long Help")
button_long.place(x=180, y=155)

# Game Button on the Long Help Section (featured with a font colour of white on a blue button background)
button_long_game = Button(frame_long_instructions)
button_long_game.config(fg="#fff", bg="#ce6aed", highlightbackground="#ce6aed", padx=10, pady=10)
button_long_game.config(cursor="hand2", command=long_game)
button_long_game.config(text="Play Game")
button_long_game.place(x=380, y=155)

# --- Separators and the content within --- #

# First separators for both sections
button_left_separator = Frame(root, width=530, height=2, bg="#dddcd4")
button_left_separator.place(x=20, y=430)

button_right_separator = Frame(root, width=530, height=2, bg="#dddcd4")
button_right_separator.place(x=590, y=450)

frame_quick_average = Frame(root, width=530, height=46)
frame_quick_average.place(x=20, y=432)

label_quick_average = Label(frame_quick_average)
label_quick_average.config(textvariable=quick_average)
label_quick_average.place(x=0, y=10)

frame_long_average = Frame(root, width=530, height=46)
frame_long_average.place(x=590, y=452)

label_long_average = Label(frame_long_average)
label_long_average.config(textvariable=long_average)
label_long_average.place(x=0, y=10)

# Second separators for both sections
average_left_separator = Frame(root, width=530, height=2, bg="#dddcd4")
average_left_separator.place(x=20, y=478)

average_right_separator = Frame(root, width=530, height=2, bg="#dddcd4")
average_right_separator.place(x=590, y=498)

frame_quick_heading = Frame(root, width=530, height=38)
frame_quick_heading.place(x=20, y=480)

label_quick_heading = Label(frame_quick_heading)
label_quick_heading.config(font="Helvetica 12 bold")
label_quick_heading.config(text="#" + " " * 5 + "Name" + " " * 20 + "Questions Asked" + " " * 10 + "Time")
label_quick_heading.place(x=0, y=7)

button_quick_timing = Button(frame_quick_heading, width=14)
button_quick_timing.config(bg="#c0c1c4", highlightbackground="#c0c1c4", padx=10, pady=2)
button_quick_timing.config(cursor="hand2", command=quick_toggle)
button_quick_timing.config(text="Precise Timing Off")
button_quick_timing.place(x=380, y=4)

frame_long_heading = Frame(root, width=530, height=38)
frame_long_heading.place(x=590, y=500)

label_long_heading = Label(frame_long_heading)
label_long_heading.config(font="Helvetica 12 bold")
label_long_heading.config(text="#" + " " * 5 + "Name" + " " * 20 + "Questions Asked" + " " * 10 + "Time")
label_long_heading.place(x=0, y=7)

button_long_timing = Button(frame_long_heading, width=14)
button_long_timing.config(bg="#c0c1c4", highlightbackground="#c0c1c4", padx=10, pady=2)
button_long_timing.config(cursor="hand2", command=long_toggle)
button_long_timing.config(text="Precise Timing Off")
button_long_timing.place(x=380, y=4)

# Third separators for both sections
heading_left_separator = Frame(root, width=530, height=2, bg="#dddcd4")
heading_left_separator.place(x=20, y=518)

heading_right_separator = Frame(root, width=530, height=2, bg="#dddcd4")
heading_right_separator.place(x=590, y=538)

# ---  Quick Question Queue Frame And Scrollbar --- #

canvas_quick_queue = Canvas(root, width=515, height=150, bd=0, highlightthickness=0)
canvas_quick_queue.place(x=20, y=520)

frame_quick_queue = Frame(canvas_quick_queue, width=515, height=150)
frame_quick_queue.place(x=0, y=0)

bar_quick_queue = Scrollbar(root, orient="vertical", command=canvas_quick_queue.yview)
canvas_quick_queue.config(yscrollcommand=bar_quick_queue.set)
bar_quick_queue.place(x=535, y=520, height=150)
canvas_quick_queue.create_window((0, 0), window=frame_quick_queue, anchor=NW)
frame_quick_queue.bind("<Configure>", frame_quick_configure)

# --- Long Question Queue Frame And Scrollbar --- #

canvas_long_queue = Canvas(root, width=515, height=120, bd=0, highlightthickness=0)
canvas_long_queue.place(x=590, y=540)

frame_long_queue = Frame(canvas_long_queue, width=515, height=120)
frame_long_queue.place(x=0, y=0)

bar_long_queue = Scrollbar(root, orient="vertical", command=canvas_long_queue.yview)
canvas_long_queue.config(yscrollcommand=bar_long_queue.set)
bar_long_queue.place(x=1090, y=540, height=120)
canvas_long_queue.create_window((0, 0), window=frame_long_queue, anchor=NW)
frame_long_queue.bind("<Configure>", frame_long_configure)

root.mainloop()
