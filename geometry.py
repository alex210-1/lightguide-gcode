# all sizes in mm
# https://math.stackexchange.com/questions/2254655/hexagon-grid-coordinate-system
# (x, y, z) cartesian, (a, b, c) hexagonal cubic
# a + b + c = 0

import matplotlib.pyplot as plt
import numpy as np
from math import floor, cos, radians
from gcode import generate_gcode

hex_size = 80  # distance center to corner
grid_size = 2  # distance between adjacent dots
ratio = cos(radians(30))
min_depth = 0.5
max_depth = 1.5


def axial_hex_to_cartesian(dot):
    (a, b, _) = dot
    return (
        grid_size * (b * ratio + a * 2 * ratio),
        b * grid_size * 1.5,
    )


# distance from center to line through dot orthogonal to grid
def hex_norm(dot):
    return max(max(dot), -min(dot)) * grid_size * 2 * ratio


# generates a list of cubic (a, b, c) tuples in final order, origin is center of hex
def generate_grid():
    n_dots = floor(
        hex_size / (2 * ratio * grid_size)
    )  # number of dots from center to edge
    print("n_dots0", n_dots)

    dots = []
    row = []

    for a in range(-n_dots + 1, n_dots):
        for b in range(-n_dots + 1, n_dots):
            dot = (a, b, -(a + b))

            # iterate over trapezoid and cut off corners to get hexagon
            if max(dot) < n_dots and min(dot) > -n_dots:
                row.append(dot)

        if (a % 2) == 0:
            row.reverse()  # alternating directions reduces travel
        dots.extend(row)
        row = []
    return dots


# return cartesian (x, y, z) tuple where z is the penetration depth
def process_dot(dot):
    dist = hex_norm(dot)

    print(dist)

    # mapping function (linear interpolation)
    z = min_depth + (max_depth - min_depth) * (1 - dist / hex_size)

    (x, y) = axial_hex_to_cartesian(dot)
    return (x, y, z)


def plot_dots(dots):
    [X, Y, Z] = np.asarray(dots).T

    fig, ax = plt.subplots()
    ax.plot(X, Y, c="gray")
    ax.scatter(X, Y, marker="o", s=Z * 30, c="red")

    fig.show()
    plt.waitforbuttonpress()


dots = generate_grid()

processed = list(map(process_dot, dots))
plot_dots(processed)

gcode = generate_gcode(processed)
print(gcode)

with open("test.gcode", "w") as file:
    file.write(gcode)
