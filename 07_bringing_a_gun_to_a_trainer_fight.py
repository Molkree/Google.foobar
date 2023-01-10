# Bringing a Gun to a Trainer Fight
# =================================

# Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

# Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully).

# Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

# The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

# For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).


import math
from collections import namedtuple

Point = namedtuple("Point", ["x", "y", "is_trainer"])


def get_distance(point_1, point_2):
    # type: (list[int], list[int]) -> float
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    return math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)


def mirror_coordinate(dimension, coordinate, mirror_index):
    # type: (int, int, int) -> int
    return (
        mirror_index * dimension + coordinate
        if mirror_index % 2 == 0
        else (mirror_index + 1) * dimension - coordinate
    )


def mirrors_in_1st_quadrant(dimensions, your_position, trainer_position, distance):
    # type: (list[int], list[int], list[int], int) -> list[Point]
    width, height = dimensions
    your_position_x, your_position_y = your_position
    trainer_position_x, trainer_position_y = trainer_position
    max_x = your_position_x + distance
    max_y = your_position_y + distance
    mirrors_x = max_x // width
    mirrors_y = max_y // height
    mirrored_points = []  # type: list[Point]
    for i in range(mirrors_x + 1):
        mirror_trainer_x = mirror_coordinate(width, trainer_position_x, i)
        mirror_player_x = mirror_coordinate(width, your_position_x, i)
        for j in range(mirrors_y + 1):
            mirror_trainer_y = mirror_coordinate(height, trainer_position_y, j)
            mirrored_points.append(
                Point(mirror_trainer_x, mirror_trainer_y, is_trainer=True)
            )
            # need to include mirrors of your position to not shoot yourself
            mirror_player_y = mirror_coordinate(height, your_position_y, j)
            mirrored_points.append(
                Point(mirror_player_x, mirror_player_y, is_trainer=False)
            )
    return mirrored_points


def solution(dimensions, your_position, trainer_position, distance):
    # type: (list[int], list[int], list[int], int) -> int
    mirrored_points = mirrors_in_1st_quadrant(
        dimensions, your_position, trainer_position, distance
    )
    mirrored_points += (
        # second quadrant
        [Point(-point.x, point.y, point.is_trainer) for point in mirrored_points]
        # third quadrant
        + [Point(-point.x, -point.y, point.is_trainer) for point in mirrored_points]
        # fourth quadrant
        + [Point(point.x, -point.y, point.is_trainer) for point in mirrored_points]
    )
    angles = {}
    for point in mirrored_points:
        dist = get_distance(your_position, [point.x, point.y])
        angle = math.atan2(point.y - your_position[1], point.x - your_position[0])
        if 0 < dist <= distance and (angle not in angles or dist < angles[angle][1]):
            angles[angle] = point.is_trainer, dist
    return sum(value[0] for value in angles.values())


assert solution([3, 2], [1, 1], [2, 1], 4) == 7
assert solution([300, 275], [150, 150], [185, 100], 500) == 9
