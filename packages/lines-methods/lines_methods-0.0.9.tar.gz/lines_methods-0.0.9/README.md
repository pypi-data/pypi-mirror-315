# Lines Methods Library #

## What is this? ##
The module allows you to work with vectors in 2D coordinates like [x1, y1, x2, y2]. 

## Quick Guide ##
The module is based on the following structure:

    
    vector = [1, 1, 5, 2]
    length = get_length(coordinates=vector)


----------


### Using ###


Using the library is as simple and convenient as possible:

Let's import it first:
First, import everything from the library (use the `from `...` import ` construct).

Examples of some operations:

Finding the intersection point of two vectors using the `get_intersection()` function:

    intersection = get_intersection(line_a, line_b)


Finding the length of the vector using the `get_length()` function:

    length = get_length(coordinates)


Finding the angle between two vectors using the `get_angle_between_lines()` function:

    angle = get_angle_between_lines(line_a, line_b)


Stretch the line in both directions using the `extend_line()` function:

    new_coordinates = extend_line(line, extend_length)    

Finding the midpoint using the `get_medium_point_from_line()` function:

    medium_point = get_medium_point_from_line(line)

----------


## Developer ##
My github: [Ugryumov_AV](https://github.com/UgryumovAV) 