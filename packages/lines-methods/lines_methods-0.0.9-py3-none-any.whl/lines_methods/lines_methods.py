import math
from typing import List, Tuple, Union


def get_intersection(line_a: List[int], line_b: List[int]) -> Union[Tuple[None, None], Tuple[int, int]]:
    x1, y1, x2, y2 = line_a
    x3, y3, x4, y4 = line_b

    a1 = y2 - y1
    b1 = x1 - x2
    c1 = a1 * x1 + b1 * y1

    a2 = y4 - y3
    b2 = x3 - x4
    c2 = a2 * x3 + b2 * y3

    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        return None, None  # The lines are parallel.

    # Calculate intersection point
    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant

    return int(x), int(y)


def get_length(coordinates: List[int]) -> int:
    x1, y1, x2, y2 = coordinates
    return int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def get_angle_between_lines(line_a: List[int], line_b: List[int]) -> int:
    vector_a = [line_a[2] - line_a[0], line_a[3] - line_a[1]]
    vector_b = [line_b[2] - line_b[0], line_b[3] - line_b[1]]

    dot_product = vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]

    magnitude_a = math.sqrt(vector_a[0] ** 2 + vector_a[1] ** 2)
    magnitude_b = math.sqrt(vector_b[0] ** 2 + vector_b[1] ** 2)

    cos_theta = dot_product / (magnitude_a * magnitude_b)

    angle_radians = math.acos(cos_theta)

    angle_degrees = math.degrees(angle_radians)
    return int(angle_degrees)


def extend_line(line: List[int] | None, extend_length: int) -> List[int]:
    if line is None:
        return [0, 0, 1, 1]
    else:
        x1, y1, x2, y2 = line
        dx = x2 - x1
        dy = y2 - y1

        length = math.sqrt(dx ** 2 + dy ** 2)

        if length > 0:
            dx /= length
            dy /= length

        new_x1 = x1 - dx * extend_length
        new_y1 = y1 - dy * extend_length
        new_x2 = x2 + dx * extend_length
        new_y2 = y2 + dy * extend_length
        return [int(new_x1), int(new_y1), int(new_x2), int(new_y2)]


def get_medium_point_from_line(line: List[int]) -> Tuple[int, int]:
    x1, y1, x2, y2 = line
    mid_x = int((x1 + x1) / 2)
    mid_y = int((y1 + y2) / 2)
    return mid_x, mid_y


def angle_between_vector_and_horizontal(line: List[int]) -> int:
    x1, y1, x2, y2 = line
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx ** 2 + dy ** 2)
    cos_theta = dx / length
    theta_rad = math.acos(cos_theta)
    theta_deg = math.degrees(theta_rad)
    if dy < 0:
        theta_deg = 360 - theta_deg
    if theta_deg > 180:
        theta_deg = theta_deg - 360
    return int(theta_deg)


def create_vector_from_point_with_angle_to_vector(v: List[int], point: List[int], alpha: int = 0) -> List[int]:
    x1, y1, x2, y2 = v
    x3, y3 = point
    delta_x1 = x2 - x1
    delta_y1 = y2 - y1
    theta1 = math.atan2(delta_y1, delta_x1)
    theta2 = theta1 + math.radians(alpha)
    L = math.sqrt(delta_x1 ** 2 + delta_y1 ** 2)
    x4 = x3 + L * math.cos(theta2)
    y4 = y3 + L * math.sin(theta2)
    return [int(x3), int(y3), int(x4), int(y4)]
