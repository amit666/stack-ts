import time
import sys

EDGE = 6
LAYER = EDGE**2
TOTAL_PIECES = EDGE**3/4

solutions = []
elapsed_times = []
last_solution_time = int(time.time())

# Shortcut functions for adjacent coordinates
def right(x, offset=1):
    return x+offset

def left(x, offset=1):
    return x-offset

def up(x, offset=1):
    return x+EDGE*offset

def down(x, offset=1):
    return x-EDGE*offset

def next_plane(x, offset=1):
    return x+LAYER*offset

# Possible ways to orient a t-piece
patterns = [
    lambda x,y,z, i: [i, right(i),  right(i,2),  right(up(i)) ] if x < EDGE-2 and y < EDGE-1 else None,
    lambda x,y,z, i: [i, right(i),  right(i,2),  right(next_plane(i))] if x < EDGE-2 and z < EDGE-1 else None,
    lambda x,y,z, i: [i, up(i),  up(i,2), right(up(i)) ] if y < EDGE-2 and x < EDGE-1 else None,
    lambda x,y,z, i: [i, up(i),  up(i,2), next_plane(up(i))] if y < EDGE-2 and z < EDGE-1 else None,
    lambda x,y,z, i: [i, up(i),  up(i,2), left(up(i)) ] if y < EDGE-2 and x > 0 else None,
    lambda x,y,z, i: [i, left(up(i)),  up(i),  right(up(i)) ] if y < EDGE-1 and x > 0 and x < EDGE-1 else None,
    lambda x,y,z, i: [i, next_plane(i), next_plane(i,2), right(next_plane(i))] if z < EDGE-2 and x < EDGE-1 else None,
    lambda x,y,z, i: [i, next_plane(i), next_plane(i,2), up(next_plane(i))] if z < EDGE-2 and y < EDGE-1 else None,
    lambda x,y,z, i: [i, next_plane(i), next_plane(i,2), left(next_plane(i))] if z < EDGE-2 and x > 0 else None,
    lambda x,y,z, i: [i, next_plane(i), next_plane(i,2), down(next_plane(i))] if z < EDGE-2 and y > 0 else None,
    lambda x,y,z, i: [i, left(next_plane(i)), next_plane(i), right(next_plane(i))] if z < EDGE-1 and x > 0 and x < EDGE-1 else None,
    lambda x,y,z, i: [i, down(next_plane(i)), next_plane(i), up(next_plane(i))] if z < EDGE-1 and y > 0 and y < EDGE-1 else None
]

# Show data in a friendly way
def pretty_print(cube):
    result = ""
    newline = "\n"
    for row in range(EDGE):
        for layer in range(EDGE):
            # Only print a layer if not empty
            print_layer = True
            for x in cube[LAYER*layer:LAYER*layer + LAYER]:
                if x is not None:
                    break
            else:
                print_layer = False

            if print_layer:
                slice = list(cube[LAYER*layer + EDGE*row:LAYER*layer + EDGE*row + EDGE])
                slice = [f"{g:<2}" if g is not None else "  " for g in slice]
                result = f"{result} {slice}"
        result = f"{result}{newline}"
    result = f"{result}{newline}"
    result = result.replace("'", "")
    result = result.replace(",", "")
    print(result)

# Main algorithm
def fill(cube, index, piece_index):
    """
    cube is an array of integers of length EDGE^3 (216), each with a value 0..(EDGE^3/4) (54)
    index is an integer 0..(EDGE^3-1), representing the current position within cube being evaluated.
    piece_index is an integer 0..(EDGE^3/4), representing the current piece
    """

    global last_solution_time

    if piece_index >= TOTAL_PIECES:
        now = int(time.time())
        elapsed = now - last_solution_time
        elapsed_times.append(elapsed)
        average = round(sum(elapsed_times)/len(elapsed_times))
        last_solution_time = now
        solutions.append(list(cube))
        print(f"Finished Solution #{len(solutions)} in {elapsed} seconds average:{average}")
        result = {
                "solutions":f"{solutions}",
                "cube":f"{cube}",
                "index":f"{index}",
                "piece_index":f"{piece_index}"
                }
        pretty_print(cube)
        return None

    # If current index is occupied, move to the next one
    try:
        if cube[index] is not None:
            result = fill(cube, index+1, piece_index)
            return result
    except Exception as e:
        print(f"index:{index} piece_index:{piece_index}")
        sys.exit()

    x = index % EDGE
    y = int(index % LAYER / EDGE)
    z = int(index / LAYER)

    # Try one of 12 possible configurations in order
    for f in range(12):
        temp_cube = list(cube)
        next_coordinates = patterns[f](x,y,z, index)
        if not next_coordinates:
            continue

        empty_spots = [temp_cube[f] is None for f in next_coordinates]
        if all(empty_spots):
            for f in next_coordinates:
                temp_cube[f] = piece_index
            fill(temp_cube, index+1, piece_index+1)
    else:
        return None

# start with an empty cube
fill([None for x in range(216)], 0, 0)
