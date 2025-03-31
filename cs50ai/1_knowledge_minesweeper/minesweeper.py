import itertools
import random
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        logger.info(f"Creating sentence with cells: {cells}, count: {count}")
        self.cells = set(cells)
        self.count = count
        self.mines = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            logger.info(f"known_safes, cells: {self.cells}, count: {self.count}")
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            logger.info(f"mark_mine, cell: {cell}, cells: {self.cells}, count: {self.count}")
            self.cells.remove(cell)
            self.mines.add(cell)
            if self.count > 0:
                self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            logger.info(f"mark_safe, cell: {cell}, cells: {self.cells}, count: {self.count}")
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        logger.info(f"mark_mine: {cell}")
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        logger.info(f"mark_safe: {cell}")
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
                based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
                if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
                if they can be inferred from existing knowledge
        """
        logger.info(f"adding knowledge: cell:{cell}, count:{count}")
        # 1
        self.moves_made.add(cell)
        # 2
        self.mark_safe(cell)
        # 3
        # to build a new sentence, we need to make the list of cells that are neighbors,
        # and count how many mines are there
        neighbor_mines_count = 0
        neighbor_cells = set()
        col, row = cell
        for i in range(col - 1, col + 2):
            for j in range(row - 1, row + 2):
                if i < 0 or i >= self.height or j < 0 or j >= self.width:
                    continue  # exclude the cells that fall outside of the grid
                if (i, j) == (col, row):
                    continue  # we don't consider the cell because it is what the user clicked and was revealed
                # if count is 0 then all the neighbors are safe
                if count == 0:
                    self.mark_safe((i, j))
                # check if the cell is a mine
                elif (i, j) in self.mines:  # we don't add the cell because its known to be a mine already
                    neighbor_mines_count += 1
                elif (i, j) not in self.safes:
                    neighbor_cells.add((i, j))
        # from what is known at this point, we have the neighbors that are mines,
        # so we take those out from the count
        count_without_known = count - neighbor_mines_count
        if neighbor_cells:  # if there are some unknown cells, add the sentence
            new_sentence = Sentence(neighbor_cells, count_without_known)
            self.knowledge.append(new_sentence)
        # 4
        # mark any additional cell as safe or mine
        # keep a loop unless there are no updates
        updates = True
        while updates:
            updates = False
            new_safes = set()
            new_mines = set()
            # check sentences with 0 mines
            for sentence in self.knowledge:
                if sentence.count == 0:
                    logger.info(f"Found a sentence with 0 mines: {sentence}")
                    updates = True
                    for cell in sentence.cells:
                        new_safes.add(cell)
            # check sentences with same number of mines and cells
            for sentence in self.knowledge:
                if sentence.count == len(sentence.cells):
                    logger.info(f"Found a sentence with ALL mines: {sentence}")
                    for cell in sentence.cells:
                        new_mines.add(cell)
            if len(new_mines) or len(new_safes):
                updates = True
                for new_safe in new_safes:
                    self.mark_safe(new_safe)
                for new_mine in new_mines:
                    self.mark_mine(new_mine)
                # now we have used the info available and probably some sentences are empty
                # so we can remove them from the knowledge
                self.knowledge = [sentence for sentence in self.knowledge if sentence.cells]

        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge
        infering_new_sets = True
        while infering_new_sets:
            infering_new_sets = False
            new_set = set()
            new_count = 0
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 == sentence2:
                        continue
                    if sentence1.cells.issubset(sentence2.cells):
                        new_set = sentence2.cells - sentence1.cells
                        new_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(new_set, new_count)
                        if new_sentence not in self.knowledge:
                            logger.info(f"Found a new set: {new_sentence}")
                            self.knowledge.append(new_sentence)
                            infering_new_sets = True
                            break

        # logging to see the progress
        logger.info(f"safes: {self.safes}")
        logger.info(f"mines: {self.mines}")
        for sentence in self.knowledge:
            logger.info(f"sentence: {sentence}")

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_cells = set(itertools.product(range(self.height), range(self.width)))
        available = all_cells - self.moves_made - self.mines
        if not available:
            # raise ValueError("no options for random moves")
            print("DONE !!!!!")
            return None
        return random.choice(list(available))
