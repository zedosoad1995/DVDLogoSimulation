from random import randrange
import numpy as np

import matplotlib.pyplot as plt

def getCornerPts(size):
    ret = []
    for x in [0, size[0]]:
        for y in [0, size[1]]:
            ret.append([x, y])
            
    return np.array(ret)

def estimateLineParams(pos, direction):
    m = direction[1]/direction[0]
    b = pos[1] - m*pos[0]
    return (m, b)

def nextBounce(pos, direction, dims_screen, dims_rect):
    x_touched_first = False
    corner_touched = False
    
    (m, b) = estimateLineParams(pos, direction)

    new_direction_x = -direction[0]
    new_direction_y = direction[1]

    if direction[0] > 0:
        x_border = dims_screen[0] - dims_rect[0]
        y_border = m*x_border + b
        if y_border <= dims_screen[1] - dims_rect[1] and y_border >= 0:
            x_touched_first = True
            if np.linalg.norm(y_border - (dims_screen[1] - dims_rect[1])) < 0.5 or np.linalg.norm(y_border) < 0.5:
                corner_touched = True
                new_direction_y = -direction[1]
    else:
        x_border = 0
        y_border = b
        if y_border <= dims_screen[1] - dims_rect[1] and y_border >= 0:
            x_touched_first = True
            if np.linalg.norm(y_border - (dims_screen[1] - dims_rect[1])) < 0.5 or np.linalg.norm(y_border) < 0.5:
                corner_touched = True
                new_direction_y = -direction[1]

    if not x_touched_first:
        new_direction_x = direction[0]
        new_direction_y = -direction[1]
        if direction[1] > 0:
            y_border = dims_screen[1] - dims_rect[1]
            x_border = (y_border - b)/m
        else:
            y_border = 0
            x_border = -b/m

    return (x_border, y_border, new_direction_x, new_direction_y, corner_touched)

    

screen_size = (800., 600.)

corner_pts = getCornerPts(screen_size)

dvd_size = (40., 30.)

for _ in range(1000):
    corner_found = False
        
    speed = np.array([1., 2.])

    initial_pos = np.array([randrange(0, screen_size[0] - dvd_size[0]), randrange(0, screen_size[1] - dvd_size[1])])*1.0
    #initial_pos = np.array([359, 0])
    pos = np.copy(initial_pos)
    #print(pos)
    cnt = 0
            
    corner_was_touched = False

    first_bounce = False
    corner_touched = False
    
    while True:

        prev_pos = np.copy(pos)
        
        (pos[0], pos[1], speed[0], speed[1], corner_touched) = nextBounce(pos, speed, screen_size, dvd_size)

        plt.plot([prev_pos[0], pos[0]], [prev_pos[1], pos[1]], 'ro-')

        if corner_touched:
            print("Corner!", pos, cnt)
            corner_was_touched = True

            #plt.show()
            #break

        cnt += 1
        
        if not first_bounce:
            first_bounce_border = np.copy(pos)
            first_bounce_speed = np.copy(speed)
            first_bounce = True
        else:
            if np.linalg.norm(first_bounce_border - pos) < 0.1 and np.all(first_bounce_speed == speed):
                #print(cnt)
                if corner_was_touched:
                    plt.show()
                else:
                    plt.clf()
                break
