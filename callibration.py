from ultrasonic import callibration_ultra
from time import sleep
from first_bot_movement import forward, backward, turn_left, turn_right
from bot_globals import bot
from math import asin, degrees

def linear_callibrate(reading, distance):
    center = 3
    error = 2

    distance = distance + center
    
    if reading > distance + error:
        forward(reading - distance)
    elif reading < distance - error:
        backward(distance - reading)
    else:
        print "no need for ultrasonic callibration, good work encoders"

def angle_callibrate(reading_left, reading_back, distance):
    ultra_diff = 10 # HAVE TO PUT CORRECT
    #center more than linear to incorporate the tires and ultra position
    center = 5
    distance_error = 4
    angle_error = 1

    distance = distance + center

    average_reading = (reading_left + reading_back)/2

    difference = reading_back - reading_left
    degree = asin(difference/ultra_diff)
    degree = degrees(degree)

    #correcting the distance from left
    if average_reading < distance - error:
        # can add the below commented if angle correction wanted before
        """if reading_left > reading_back + angle_error:
            turn_left(degree)
        elif reading_left < reading_back - angle_error:
            turn_right(degree)"""
        turn_right()
        forward(distance - average_reading)
        turn_left()
            
    elif average_reading > distance + error:
        # can add the below commented if angle correction wanted before
        """if reading_left > reading_back + angle_error:
            turn_left(degree)
        elif reading_left < reading_back - angle_error:
            turn_right(degree)"""
        turn_left()
        forward(average_reading - distance)
        turn_right()

    #now correcting the angle
    if reading_left > reading_back + angle_error:
        turn_left(degree)
        
    elif reading_left < reading_back - angle_error:
        turn_right(degree)

def callibrate(rows, columns, cx, cy, mapp):
    # [0] = forward, [1] = left, [2] = back
    readings = callibration_ultra()

    #for linear callibration
    if bot.direction == 'n':
        if cx == 0:
            distance = 0
        else:
            for i in range(1, cx):
                if mapp[i][cy] == 1:
                    distance = (cx - i - 1) * 25
            distance = cx * 25
        
    elif bot.direction == 's':
        if cx == rows:
            distance = 0
        else:
            for i in range(cx, rows):
                if mapp[i][cy] == 1:
                    distance = (i - cx - 1) * 25
            distance = (rows - cx - 1) * 25
        
    elif bot.direction == 'w':
        if cy == 0:
            distance = 0
        else:
            for i in range(1, cy):
                if mapp[cx][i] == 1:
                    distance = (cy - i - 1) * 25
            distance = cy * 25

    elif bot.direction == 'e':
        if cy == columns:
            distance = 0
        else:
            for i in range(cy, columns):
                if mapp[cx][i] == 1:
                    distance = (i - cy - 1) * 25
            distance = (columns - cy - 1) * 25
    
    linear_callibrate(readings[0], distance)

    # for angle callibration
    if bot.direction == 'n':
        if cy == 0:
            distance = 0
        else:
            for i in range(1, cy):
                if mapp[cx][i] == 1:
                    distance = (cy - i - 1) * 25
            distance = cy * 25
        
    elif bot.direction == 's':
        if cy == columns:
            distance = 0
        else:
            for i in range(cy, columns):
                if mapp[cx][i] == 1:
                    distance = (i - cy - 1) * 25
            distance = (columns - cy - 1) * 25
        
    elif bot.direction == 'w':
        if cx == rows:
            distance = 0
        else:
            for i in range(cx, rows):
                if mapp[i][cy] == 1:
                    distance = (i - cx - 1) * 25
            distance = (rows - cx - 1) * 25

    elif bot.direction == 'e':
        if cx == 0:
            distance = 0
        else:
            for i in range(1, cx):
                if mapp[i][cy] == 1:
                    distance = (cx - i - 1) * 25
            distance = cx * 25

    angle_callibrate(readings[1], readings[2], distance)
