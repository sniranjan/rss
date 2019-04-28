from flask import Flask, request
"""
This program exposes a API and responds to the questions asked in query parameters "q" and "d"
"""


app = Flask(__name__)

@app.route('/')
def respond():
    # Captures the URL parameter "q"
    q = request.args.get('q', default = '', type = str)

    if q=='Ping':
        return 'OK'
    elif q=='Name':
        return "Niranjan Sonachalam"
    elif q== 'Puzzle':
        # Captures the puzzle as a string
        d = request.args.get('d', default='', type=str).split('\n')
        # Removes unnecessary strings from puzzle
        puzzle = d[2:]
        del puzzle[-1]
        return solve_puzzle(puzzle)
    elif q=='Resume':
        return "https://drive.google.com/open?id=1Ig7EpWj_SVONjwn1cfj8M7ZCxrfkiRWx"
    elif q=='Referrer':
        return "Angel.co"
    elif q=='Position':
        return "Senior Software Engineer/Technical Architect"
    elif q=='Phone':
        return "8478487750"
    elif q=="Email Address":
        return "niranjansonachalam@gmail.com"
    elif q=="Degree":
        return "Post Graduate Program in Business Analytics / Bachelor of Engineering(Electronics and Communication Engineering)"
    elif q=="Status":
        return "Yes, currently on H1B with approved i140"
    elif q=="Source":
        return "https://github.com/sniranjan/rss.git"
    elif q=="Years":
        return "8"
    else:
        return "Unexpected Input, Not OK"

def solve_puzzle(puzzle):
    print(puzzle)
    """This funciton solves the puzzle"""

    # Create a empty matrix
    puzzle_matrix = [[None] * len(puzzle) for i in range(len(puzzle))]

    # List to hold rules and nodes
    rules = []
    nodes = []

    # For each row in puzzle
    for row_index, row in enumerate(puzzle):
        # Add the identified nodes to a list [A,B,C,D]
        nodes.append(list(row)[0])
        # Split string and convert to lists
        for column_index, item in enumerate(list(row)[1:]):
            # The puzzle row contains the element too like A-->- removing the first character and converting the remaining to a list
            if column_index == row_index:
                #if A==A,then, set the value to "="
                puzzle_matrix[row_index][column_index] = '='
            else:
                # If not, then, populate the value
                current_node = list(row)[0]
                comparing_node = puzzle[column_index][0:1]
                # If there is no value in the puzzle,
                # calculate the translative property with the given rules,
                # if there is a match found, update the matrix
                if item == '-':
                    if len(rules) > 0:
                        for rule in transitive_closure(rules):
                            if rule[0] in nodes and rule[1] in nodes:
                                #if there is already a condition( > or < ) given, then the reverse is also true - populate that too
                                puzzle_matrix[nodes.index(rule[0])][nodes.index(rule[1])] = ">"
                                puzzle_matrix[nodes.index(rule[1])][nodes.index(rule[0])] = "<"
                else:
                    if item == '>':
                        rules.append((current_node, comparing_node))
                    else: ## Reordering to support calling the transitive function
                        rules.append((comparing_node, current_node))
                    # if there is already a condition( > or < ) given, then the reverse is also true - populate that too
                    puzzle_matrix[row_index][column_index] = item
                    puzzle_matrix[column_index][row_index] = item

    # Formatting results
    result = " " + "".join(nodes) + "\n"
    for index, row in enumerate(puzzle_matrix):
        result = result + nodes[index] + "".join(row) + "\n"
    return result


def transitive_closure(a):
    """
    Function to calculative transitive property between two elements
    If A>B and B>C , then A>C
    """
    closure = set(a)
    while True:
        new_relations = set((x,w) for x,y in closure for q,w in closure if q == y)
        closure_until_now = closure | new_relations

        if closure_until_now == closure:
            break
        closure = closure_until_now
    return closure

if __name__== "__main__":
    app_host = '0.0.0.0'
    app_port= 8081
    app.run(host=app_host,port=app_port,debug=True,threaded=True)