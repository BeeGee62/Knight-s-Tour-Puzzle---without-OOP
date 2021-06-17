# Knight's Tour Puzzle: program to find a path from a given position on a chess board
# with a knight, using only legitimate moves and visiting each square only once


def request_dimensions():
    """ Ask user for board dimensions, first #columns and second #rows
    """

    while True:
        dimensions = input("Enter your board dimensions: ").split()
        if len(dimensions) != 2:
            print("Invalid dimensions!")
        else:
            try:
                column_n, row_n = (int(dimension) for dimension in dimensions)
            except ValueError:
                print("Invalid dimensions!")
            else:
                if column_n <= 0 or row_n <= 0:
                    print("Invalid dimensions!")
                else:
                    return column_n, row_n


def request_start_coordinates(dimensions):
    """ Ask user for the knight's start coordinates, first column and second row

    Keyword arguments:
        dimensions: tuple with 2 integers; #chessboard_columns and #chessboard_rows
    """

    while True:
        coordinates = input("Enter the knight's starting position: ").split()
        if not valid_coordinates(dimensions, coordinates):
            print("Invalid position!")
        else:
            return tuple(int(coordinate) for coordinate in coordinates)


def valid_coordinates(dimensions, coordinates):
    """ Return validity of coordinates

    Keyword arguments:
        dimensions:  tuple with 2 integers; #chessboard_columns and #chessboard_rows
        coordinates: string with possibly tuple of 2 integers, col and row
    """

    if len(coordinates) == 2:
        try:
            col, row = (int(coordinate) for coordinate in coordinates)
        except ValueError:
            return False
        else:
            return (1 <= row <= dimensions[1]) and (1 <= col <= dimensions[0])
    else:
        return False


def request_user_solution():
    """ If user wants to solve puzzle manually returns True
    """

    while True:
        answer = input("Do you want to try the puzzle? (y/n): ").lower()

        if answer == 'y' or answer == 'n':
            return answer == 'y'
        else:
            print('Invalid option')


def draw_board(dimensions, knight_position, visited, possible_moves=None):
    """ Draw chess board and the position of the knight on the board

    Keyword arguments:
        dimensions:      tuple with 2 integers; #chessboard_columns and #chessboard_rows
        knight_position: tuple with 2 integers; 1 <= knight_position[0] <= #rows and
                         1 <= knight_position[1] <= #cols
        visited:         dictionary with coordinate: '*' (user solved) or 'int' (int = order of visited square)
        possible_moves:  dictionary with coordinate: 'int' (int = nr of squares that can be visited from that pos.)
    """
    square_width = len(str(dimensions[0] * dimensions[1]))
    empty_square = " " + "_" * square_width
    king_square = " " * square_width + "X"
    chessboard = [[empty_square] * dimensions[0] for _ in range(dimensions[1])]
    if possible_moves is None:
        possible_moves = {}

    # mark knight's position, possible moves and visited_squares
    knight_col = dimensions[1] - knight_position[1]
    knight_row = knight_position[0] - 1
    chessboard[knight_col][knight_row] = king_square
    for move in possible_moves:
        square_contents = f"{str(possible_moves[move]):>{square_width + 1}s}"
        chessboard[dimensions[1] - move[1]][move[0] - 1] = square_contents
    for visit in visited:
        square_contents = f"{str(visited[visit]):>{square_width + 1}s}"
        chessboard[dimensions[1] - visit[1]][visit[0] - 1] = square_contents

    # print chess board
    border_row = " " * len(str(dimensions[1])) + "-" + "-" * len(empty_square) * dimensions[0] + "--"
    print(border_row)
    for row in range(dimensions[1]):
        print(''.join(['%*d|' % (len(str(dimensions[1])), dimensions[1] - row)] + chessboard[row] + [" |"]))
    print(border_row)
    column_numbers = ['%*d' % (len(empty_square), col + 1) for col in range(dimensions[0])]
    last_row = " " * (len(str(dimensions[1])) + 1) + ''.join(column_numbers)
    print(last_row)


def determine_moves(dimensions, knight_position, visited=None, warnsdorrf_index=-1, user_play=False):
    """ Determine the moves the knight can make from the given position avoiding squares already visited

    Keyword arguments:
        dimensions:  tuple with 2 integers; #chessboard_columns and #chessboard_rows
        knight_position:  tuple with 2 integers; 1 <= knight_position[0] <= #rows and
                          1 <= knight_position[1] <= #cols
        visited:          list of tuples representing all visited squares
        warnsdorrf_index: 1 if number of projected new moves from knight_position needs to be included
        user_play:        boolean
    """
    candidate_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
    possible_moves = {}
    if visited is None:
        visited = {}

    if warnsdorrf_index >= 0:
        for move in candidate_moves:
            horizontal = knight_position[0] + move[0]
            vertical = knight_position[1] + move[1]
            if (1 <= horizontal <= dimensions[0]) and (1 <= vertical <= dimensions[1])\
                    and ((horizontal, vertical) not in visited):
                possible_moves[(horizontal, vertical)] =\
                    len(determine_moves(dimensions, (horizontal, vertical), visited, warnsdorrf_index - 1, user_play))\
                    - int(user_play)

        sorted_posssible_moves = {k: v for k, v in sorted(possible_moves.items(), key=lambda item: item[1])}
        return sorted_posssible_moves
    else:
        return {}


def make_move(dimensions, possible_moves):
    """ Ask user to make the knight's next move; returns coordinates

    Keyword arguments:
        dimensions:      tuple with 2 integers; #chessboard_columns and #chessboard_rows
        possible_moves:  dictionary with keys tuples of 2 integers, marking the possible moves the
                         knight can make from the given position; value can be ignored here
    """
    while True:
        coordinates = input("Enter your next move: ").split()
        to_check = tuple(int(coordinate) for coordinate in coordinates)
        if not valid_coordinates(dimensions, coordinates):
            print("Invalid move!", end=" ")
        elif to_check not in possible_moves:
            print("Invalid move!", end=" ")
        else:
            return tuple(int(coordinate) for coordinate in coordinates)


def user_plays(dimensions, knight_start_point):
    """ Get all moves from user

    Keyword arguments:
        dimensions:         tuple with 2 integers; #chessboard_columns and #chessboard_rows
        knight_start_point: tuple with 2 integers; 1 <= knight_start_point[0] <= #rows and
                            1 <= knight_start_point[1] <= #cols
    """
    visited_points = {}

    # Puzzle iterative solution loop
    knight_old_position = knight_start_point
    legitimate_moves = determine_moves(dimensions, knight_start_point, {}, warnsdorrf_index=1, user_play=True)

    while len(legitimate_moves) > 0:
        knight_new_position = make_move(dimensions, legitimate_moves)
        visited_points[tuple(knight_old_position)] = '*'
        legitimate_moves =\
            determine_moves(dimensions, knight_new_position, visited_points, warnsdorrf_index=1, user_play=True)

        if len(legitimate_moves) == 0:
            if len(visited_points) == (dimensions[0] * dimensions[1] - 1):
                print("What a great tour! Congratulations!")
            else:
                print("No more possible moves!")
                print("Your knight visited", len(visited_points) + 1, "squares!")
            break

        draw_board(dimensions, knight_new_position, visited_points, legitimate_moves)
        knight_old_position = knight_new_position


def computer_plays(dimensions, knight_start_point, print_solution=False):
    """ Computer generates a solution if one exists, using Warnsdorff's heuristic and backtracking

    Keyword arguments:
        dimensions:         tuple with 2 integers; #chessboard_columns and #chessboard_rows
        knight_start_point: tuple with 2 integers; 1 <= knight_start_point[0] <= #cols and
                            1 <= knight_start_point[1] <= #rows
        print_solution:     boolean
    """
    def solve_it(knight_pos, step):
        """ Inside function for depth-first search and backtracking

        Keyword arguments:
            knight_pos: tuple with 2 integers; with current knight position
            step:       integer counter for last move
        """

        legitimate_moves = determine_moves(dimensions, knight_pos, visited_points, warnsdorrf_index=1, user_play=False)
        dead_ends = {k: v for k, v in legitimate_moves.items() if v == 0}
        promising_moves = {k: v for k, v in legitimate_moves.items() if v > 0}

        # only enter dead end if it is the last move => len(dead_ends) == 1:
        if step == (dimensions[0] * dimensions[1] - 1):
            # print("last-but-one move encountered")
            step += 1
            new_knight_pos = list(dead_ends)[0]
            visited_points[new_knight_pos] = step
            return True
        elif len(promising_moves) > 0:
            # presumes ordering by Warnsdorff score, guaranteed by determine_moves() => only works in Python 3.7+
            for new_knight_position in promising_moves.keys():
                step += 1
                visited_points[new_knight_position] = step

                if solve_it(new_knight_position, step):
                    return True

                # not finished than back track
                visited_points.popitem()
                step -= 1
        else:
            return False

    visited_points = {}
    move = 1
    visited_points[knight_start_point] = move
    solved = solve_it(knight_start_point, move)

    if print_solution:
        print("Here's the solution!")
        draw_board(dimensions, knight_start_point, visited_points)

    return solved


def main_control_loop():
    """ Ask to define board, starting position of knight and whether user wants to solve the puzzle
    """
    # User input: define board, starting position knight and if user wants to solve puzzle
    dimensions = tuple(request_dimensions())
    knight_start_point = request_start_coordinates(dimensions)
    user_solves = request_user_solution()
    solution_exists = computer_plays(dimensions, knight_start_point, print_solution=False)
    if not solution_exists:
        print("No solution exists!")
        return

    # proceed if a feasible solution exists
    if user_solves:
        legitimate_moves = determine_moves(dimensions, knight_start_point, {}, warnsdorrf_index=1, user_play=True)
        draw_board(dimensions, knight_start_point, {}, legitimate_moves)
        user_plays(dimensions, knight_start_point)
    else:
        computer_plays(dimensions, knight_start_point, print_solution=True)


main_control_loop()
