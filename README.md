# Class Question Queue

This is a queueing application for students to raise questions in class.

## Overview

* When a user presses either the "Request Quick Help" button or "Request Long Help" button,
the application will display a dialog box which asks the user for their name. Once they have entered their name,
the application will join the user to the queue, display their name on the screen, and regularly update the amount of time they have been waiting on the queue.
* The queue keeps track of how many times a question has been asked by the same student since opening the application.
This number is tracked separately for quick & long help and is not updated if they are removed by clicking the red button.
* When a student is added to the queue, they will be added in such a way that no student who has asked a greater number of questions
is placed ahead of them.
* The queue prevents the same student from joining multiple times.
A student may be removed from the queue by either pressing the red button - voluntarily cancelling their request,
or by pressing the green button - marking the request as accepted.
* The queue keeps track of the approximate time a student has been waiting on the queue according to the following table.
Where **x** is used in the display, the value is rounded down - i.e. a wait time of 13:37 should be displayed as "13 minutes ago".

| Wait Time   | Display           |
| :---------: | :---------------: |
| < 1 minute  | a few seconds ago |
| < 2 minutes | a minute ago      |
| < 1 hour    | **x** minutes ago |
| < 2 hours   | 1 hour ago        |
| >= 2 hours  | **x** hours ago   |

* The queue displays the average wait time for the queue, e.g. An average wait of about 12 minutes for 2 students.
* The queue is ordered first by "Questions Asked" in descending order, then by "Time" in ascending order. In other words,
students who have asked fewer questions should be placed to the top. If two students have asked the same number of questions,
the one who has waited longer should be placed to the top.
* The app includes provision of a game which the user can play while they are waiting to have their questions answered.
* Scrollbars are added to so that there is no upper bound for the number of recipients.
* Toggle buttons are added to allow the user to have the option to view the exact time they have been waiting on the queue.
The refreshing interval is set to three seconds by default. Once the button is pressed, it might require a few seconds for the program to finish execution,
which is dependent on the running platform.

## Game Manuals

### Paddle Ball – Single Player
In this game the user is to move the paddle near the bottom of the screen and catch the bouncing ball.
The ball is initially situated in the center and given a random direction to move upwards.
The goal is to make the ball hit the red target in the center of concentric circles. The game is won if the ball hits both targets and
lost if the ball touches the floor.
* **Arrow Left**: Move the paddle left
* **Arrow Right**: Move the paddle right
* **Arrow Down**: Stop the paddle

### Paddle Ball – Double Player
This game allows two users to play simultaneously. The users are to move the paddles positioned on opposite sides of the screen separately
and catch the bouncing ball. The ball is initially situated in the center and given a random direction to move.
The goal is to make the ball hit the opposite side wall of your opponent and whoever succeeds wins the game.
* **W**: Move the red paddle up
* **S**: Move the red paddle down
* **A**: Stop the red paddle
* **Arrow Up**: Move the blue paddle up
* **Arrow Down**: Move the blue paddle down
* **Arrow Right**: Stop the blue paddle
