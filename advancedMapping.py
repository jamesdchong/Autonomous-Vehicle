import picar_4wd as fc
import numpy as np
import time

# function that prints the map in human-readable format
def printMap(Map):
    Map = np.rot90(Map)
    for row in Map:
        for value in row:
            print("{}".format(value), end="")
        print(end='\n')

def scanMap(start, end, step, prev_angle, prev_x, prev_y):
    Map = np.zeros((100,50), dtype=int) # map of surroundings

    # take reading every 2 degrees
    for angle in range(start, end, step):
        fc.us.servo.set_angle(angle)
        distance = fc.us.get_distance()

        # 49 because to avoid index out of bounds, 2 to avoid close noise
        if distance <= 49 and distance > 2:
            # calculate coordinates using angle, distance
            x_coord = round(distance * np.sin(np.deg2rad(-angle)) + 50)
            y_coord = round(distance * np.cos(np.deg2rad(-angle)))
            Map[x_coord, y_coord] = 1

            # if detected objects within 6 degrees from the previous, connect them
            if np.abs(prev_angle - angle) <= 6:
                # vertical
                if prev_x == x_coord:
                    for y in range(min(prev_y, y_coord), max(prev_y, y_coord)):
                        Map[x_coord, y] = 1
                # diagonal, horizontal
                else:
                    slope = (y_coord - prev_y) / (x_coord - prev_x)
                    for x in range(min(prev_x, x_coord), max(prev_x, x_coord)):
                        y = round(slope * (x - prev_x)) + prev_y
                        Map[x, y] = 1

            # update prev coordinates, angle
            prev_angle = angle
            prev_x = x_coord
            prev_y = y_coord

    printMap(Map)

    return Map, prev_angle, prev_x, prev_y

def buildMap(continuous=True):
    start, end, step = -90, 90, 2 # initially start from right, move left
    prev_angle, prev_x, prev_y = np.inf, np.inf, np.inf # initalize prev variables

    # advanced mapping
    if continuous:
        while True:
            Map, prev_angle, prev_x, prev_y = scanMap(start, end, step, prev_angle, prev_x, prev_y)
            start, end, step = -start, -end, -step # move in other direction
            
    # A* scanning
    else:
        fc.us.servo.set_angle(start)
        time.sleep(0.5)
        Map,_,_,_ = scanMap(start, end, step, prev_angle, prev_x, prev_y)
        return Map

def main():
    buildMap()
        
if __name__ == "__main__":
    main() 