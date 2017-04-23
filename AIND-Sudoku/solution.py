assignments = []

rows = 'ABCDEFGHI'
columns = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


def diagonal_units():
    """
    Construct the diagonal units - First we construct the diagonal from A1 to I9 and then from A9 to I1
    together these 2 lists are the diagonal units
    """
    diagonal = []
    for index, element in enumerate(rows):
        diagonal.append(rows[index] + columns[index])
    n = len(rows) - 1
    other_diagonal = []
    for index, element in enumerate(rows):
        other_diagonal.append(rows[index] + columns[n - index])
    return [diagonal, other_diagonal]


boxes = cross(rows, columns)
row_units = [cross(r, columns) for r in rows]
column_units = [cross(rows, c) for c in columns]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = diagonal_units()
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def remove_value_from_peers(value, list_of_peers, values):
    """
    Removes the value from the list of peers.
    :param value: value of the box - eg. '12' 
    :param list_of_peers: intersection of the peers list of both elements of naked twins
    :param values: value dict representing the sudoku
    :return: values
    """
    for peer in list_of_peers:
        for individual_value in value:
            values = assign_value(values, peer, values[peer].replace(individual_value, ''))
    return values


def find_naked_twin(values, box):
    """
    Find the naked Twin for the box
    :param values: value dict representing the sudoku
    :param box: denotes the key for which peers are being traversed. Eg A3
    :return: naked Twin of the element if found or else returns False.
    """
    for element in peers[box]:
        if set(values[box]) == set(values[element]):
            return element
    return False


def find_common_peers(twin_one, twin_two):
    """
    Find the Common Peers for 2 Naked Twins
    :param twin_one: Box corresponding to naked Twin one. Eg A1
    :param twin_two: Box corresponding to naked Twin two. Eg A2
    :return: list of common peers
    """
    return set(peers[twin_one]) & set(peers[twin_two])


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    display(values)
    for key in values.keys():
        if len(values[key]) == 2:
            expected_naked_twin = find_naked_twin(values, key)
            if expected_naked_twin == False:
                continue
            common_peers = find_common_peers(key, expected_naked_twin)
            values = remove_value_from_peers(values[key], common_peers, values)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_dict = {}
    grid_index = 0
    cells = cross(rows, columns)
    for x in range(81):
        grid_dict[cells[x]] = grid[grid_index] if grid[grid_index] != '.' else '123456789'
        grid_index = grid_index + 1
    return grid_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    :param values: A sudoku in dictionary form
    :return: The resulting sudoku in dictionary form
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate(), only_choice() and naked_Twins(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    :param values:   A sudoku in dictionary form.
    :return:  A sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def is_sudoku_solved(values):
    """
    Validates if the sudoku is solved by asserting if all length of value in all boxes == 1.
    :param values: 
    :return: True if sudoku is solved else False
    """
    return all(len(values[s]) == 1 for s in boxes)


def find_element_with_min_branches(values):
    """
    Find the Element which will spawn minimum branches
    :param values: value dict representing the sudoku grid
    :return: element with least branching
    """
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    return s


def solve_sudoku(values):
    """
    The method to recursively solve the sudoku
    :param values: value dict representing the sudoku grid
    :return: solution of the sudoku - value dict representing the sudoku grid
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if is_sudoku_solved(values):
        return values
    least_branching_cell = find_element_with_min_branches(values)
    for rValue in values[least_branching_cell]:
        new_sudoku = values.copy()
        new_sudoku[least_branching_cell] = rValue
        solution = solve_sudoku(new_sudoku)
        if solution:
            return solution


def search(values):
    """
    search the sudoku to solve it - It is basically used to invoke solve_sudoku
    :param values: value dict representing the sudoku grid
    :return: solved sudoku 
    """
    return solve_sudoku(values)


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


print(peers['A1'])
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    sudoku = solve(diag_sudoku_grid)
    display(sudoku)
    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
