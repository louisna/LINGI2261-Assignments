from clause import *

"""
For the color grid problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the grid color problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, points=None):
    expression = []
    # your code here
    for i in range(size):
        for j in range(size):
            a = [item for item in points if item[0] == i and item[1] == j]
            for k in range(size):
                if len(a) > 0 and a[0][2] != k:
                    continue
                for runner in range(size):
                    # First: add clauses for the row
                    if runner != i:
                        clause_row = Clause(size)
                        clause_row.add_negative(i, j, k)
                        clause_row.add_negative(runner, j, k)
                        expression.append(clause_row)
                    # Second: add clauses for the column
                    if runner != j:
                        clause_column = Clause(size)
                        clause_column.add_negative(i, j, k)
                        clause_column.add_negative(i, runner, k)
                        expression.append(clause_column)
    for i in range(size):
        for j in range(size):
            a = [item for item in points if item[0] == i and item[1] == j]
            for k in range(size):
                if len(a) > 0 and a[0][2] != k:
                    continue
                # For up
                for runner in range(1, size):
                    if i - runner < 0 or j - runner < 0:
                        break
                    clause_diag_1_up = Clause(size)
                    clause_diag_1_up.add_negative(i, j, k)
                    clause_diag_1_up.add_negative(i-runner, j-runner, k)
                    expression.append(clause_diag_1_up)
                # For down
                for runner in range(1, size):
                    if i + runner >= size or j + runner >= size:
                        break
                    clause_diag_1_up = Clause(size)
                    clause_diag_1_up.add_negative(i, j, k)
                    clause_diag_1_up.add_negative(i + runner, j + runner, k)
                    expression.append(clause_diag_1_up)

                # For up
                for runner in range(1, size):
                    if i - runner < 0 or j + runner >= size:
                        break
                    clause_diag_1_up = Clause(size)
                    clause_diag_1_up.add_negative(i, j, k)
                    clause_diag_1_up.add_negative(i-runner, j+runner, k)
                    expression.append(clause_diag_1_up)
                # For down
                for runner in range(1, size):
                    if i + runner >= size or j - runner < 0:
                        break
                    clause_diag_1_up = Clause(size)
                    clause_diag_1_up.add_negative(i, j, k)
                    clause_diag_1_up.add_negative(i + runner, j - runner, k)
                    expression.append(clause_diag_1_up)
    return expression


if __name__ == '__main__':
    expression = get_expression(3, [(0, 0, 0)])
    for clause in expression:
        print(clause)
