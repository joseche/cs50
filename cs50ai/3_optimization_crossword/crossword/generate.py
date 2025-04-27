import sys

# import math

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {var: self.crossword.words.copy() for var in self.crossword.variables}

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [[None for _ in range(self.crossword.width)] for _ in range(self.crossword.height)]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new("RGBA", (self.crossword.width * cell_size, self.crossword.height * cell_size), "black")
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2), rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            for word in self.domains[variable].copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision_made = False
        x_values = self.domains[x].copy()
        y_values = self.domains[y]
        if overlap := self.crossword.overlaps[x, y]:
            xi, yi = overlap
            for x_value in x_values:
                x_has_y = any(x_value[xi] == y_value[yi] for y_value in y_values)
                if not x_has_y:
                    self.domains[x].remove(x_value)
                    revision_made = True
        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        q = []
        if arcs is None:
            q.extend(list(iter(self.crossword.overlaps)))
        else:
            q.extend(arcs)
        while q:
            x, y = q.pop()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                q.extend((n, x) for n in self.crossword.neighbors(x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(var in assignment for var in self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        used_words = []
        for x in assignment:
            x_value = assignment[x]
            if x_value in used_words:
                return False
            used_words.append(x_value)
            x_value_len = len(x_value)
            if x_value_len != x.length:
                return False
            for y in self.crossword.neighbors(x):
                if y in assignment:
                    y_value = assignment[y]
                    if x_value == y_value:
                        return False
                    xi, yi = self.crossword.overlaps[x, y]
                    if x_value[xi] != y_value[yi]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        x_values = self.domains[var]
        ruled_out_values = {var: 0 for var in x_values}
        for y in self.crossword.neighbors(var):
            y_values = self.domains[y].copy()
            for y_value in y_values:
                xi, yi = self.crossword.overlaps[var, y]
                for x_value in x_values:
                    if x_value[xi] != y_value[yi]:
                        ruled_out_values[x_value] += 1
        return sorted(ruled_out_values, key=lambda x: ruled_out_values[x])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_keys = self.domains.keys() - assignment.keys()
        n_values = {k: len(self.domains[k]) for k in unassigned_keys}
        min_values = min(n_values.values())
        tie_keys = [k for k in unassigned_keys if len(self.domains[k]) == min_values]
        if len(tie_keys) <= 1:
            return tie_keys[0]
        # choose key with highest degree
        degree_vals = {k: len(self.crossword.neighbors(k)) for k in unassigned_keys}
        max_degree = max(degree_vals.values())
        max_degree_keys = [k for k in unassigned_keys if len(self.crossword.neighbors(k)) == max_degree]
        return max_degree_keys[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            if self.consistent(assignment):
                if result := self.backtrack(assignment):
                    return result
            del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
