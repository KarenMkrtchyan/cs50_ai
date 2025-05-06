import itertools
import random


class Minesweeper():
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


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    # Ex: {A, B, C} = 3 
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def __sub__(self, other):
        if isinstance(other, Sentence):
            return Sentence(self.cells.difference(other.cells), self.count-other.count)
        else:
            raise TypeError("Unsupported operand type for -")
        
    def issubset(self, other):
        return self.cells.issubset(other.cells)

    def copy(self):
        return Sentence(self.cells.copy(), self.count)
    
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return None
        
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return None
        
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        try:
            self.cells.remove(cell)
            self.count -=1
        except:
            return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        try:
            print("sentence mark_safe call")
            self.cells.remove(cell)
        except:
            return


class MinesweeperAI():
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

    def near_cells(self, cell):
        list_of_cells = []

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    list_of_cells.append((i,j))
        
        return list_of_cells


    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            print("minesweeperAI mark_safe call")
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
        self.moves_made.add(cell)
        self.mark_safe(cell)
        new_knowledge = Sentence(self.near_cells(cell), count)
        self.knowledge.append(new_knowledge)
        madeInfference = True

        while madeInfference:
            madeInfference = False
            for sentence in self.knowledge: # O(n^2), TODO: optimize, but how? 
                # when a sentence becomes trivial
                self.extract_sentence(sentence)
                # when a subset emerges
                for second_sentence in self.knowledge:
                    if second_sentence == sentence:
                        continue
                    if second_sentence.issubset(sentence):
                        new_knowledge = sentence - second_sentence
                        self.extract_sentence(new_knowledge)
                        madeInfference = True
                    elif sentence.issubset(second_sentence):
                        new_knowledge = second_sentence - sentence
                        self.extract_sentence(new_knowledge)
                        madeInfference = True
            if madeInfference:
                if len(new_knowledge.cells) != 0:
                    for sentence in self.knowledge: # O(n^2), TODO: optimize, but how? 
                        if sentence == new_knowledge:
                            madeInfference = False
                            break
            if madeInfference:     
                self.knowledge.append(new_knowledge)


    def extract_sentence(self, sentence):
        working_sentence = sentence.copy()
        if working_sentence.known_safes() != None:
            for known_save in working_sentence.known_safes():
                print("found a save cell", known_save)
                self.mark_safe(known_save)
        if working_sentence.known_mines() != None:
            for known_mine in working_sentence.known_mines():
                print("found a mine", known_mine)
                self.mark_mine(known_mine)   

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        try:
            print("big brain move")
            print(self.safes - self.moves_made)
            chosen_move = (self.safes - self.moves_made).pop()
            self.moves_made.add(chosen_move)
            return chosen_move
        except:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # heuristic: pick a random cell from the sentence with the highest cell#/mine# ratio
        try:   
            chosen_sentence = None
            chosen_ratio = 0
            for sentence in self.knowledge:
                if len(sentence.cells)/sentence.count > chosen_ratio:
                    chosen_ratio = len(sentence.cells)/sentence.count
                    chosen_sentence = sentence
                move = random.choice(chosen_sentence.cells)
                self.moves_made.add(move)
                return move
        except:
            return (random.randint(0,self.height-1),  random.randint(0,self.width-1))