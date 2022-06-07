import random


class Board:
    def __init__(self, board_dim, num_bombs):
        self.board_dim = board_dim
        self.num_bombs = num_bombs

        self.board = self.make_board()

       # print(self.board)

        # for i in range(self.board_dim):
        #     for j in range(self.board_dim):
        #         print(self.board[i][j], end=" ")
        #     print(" ")

        self.already_dug = set()  # we declare it as a set as this would avoid any duplications

        self.assign_number_to_squares()

    def make_board(self):  # we define the board and plant the bombs here

        board = [[None for _ in range(self.board_dim)]
                 for _ in range(self.board_dim)]

        # this will make the board like :
        # [None , None , .... None]
        # [None , None , .... None]
        # .
        # .
        # [None , None , .... None]

        # print(board)

        # now let us plant the bombs at random locations
        num_of_bombs_planted = 0
        while(num_of_bombs_planted < self.num_bombs):
            loc = random.randint(0, self.board_dim**2 - 1)
            row = loc // self.board_dim
            col = loc % self.board_dim

            # bomb is already planted in location if the condition is true
            if board[row][col] == '*':
                continue  # continue statements start executing the next iteration of the loop

            else:
                board[row][col] = '*'
                num_of_bombs_planted += 1
        return board

    # Over here we are going to assign values to each square which tells us the number of bombs next to the square
    def assign_number_to_squares(self):

        for i in range(self.board_dim):
            for j in range(self.board_dim):
                if self.board[i][j] == '*':
                    continue
                self.board[i][j] = self.calculate_number_of_bombs(i, j)
        print(" ")
        # # print(self.board)
        # for i in range(self.board_dim):
        #     for j in range(self.board_dim):
        #         print(self.board[i][j], end=" ")
        #     print(" ")

    # Function to calculate the number of bombs adjacent to a given square
    def calculate_number_of_bombs(self, row, col):

        num_of_bombs_nearby = 0
        # we add a plus one as range(row-1,row+1) will stop at row and not row+1
        for i in range(max(0, row-1), min(self.board_dim, (row+1) + 1)):
            for j in range(max(0, col-1), min(self.board_dim, (col+1)+1)):
                if i == row and j == col:  # this is element for which we are calculating the number of bombs nearby, can skip
                    continue
                if(self.board[i][j] == '*'):
                    num_of_bombs_nearby += 1
        return num_of_bombs_nearby

    def dig(self, row, col):
        # we use this recursive function to keep digging until we hit a square that has a bomb next to it.
        # if the number of bombs next to a square is 0, then we dig all of the adjacent squares

        # to keep a track of where we have dug
        self.already_dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # if self.board[row][col] == 0 ,
        for i in range(max(0, row-1), min(self.board_dim, (row+1) + 1)):
            for j in range(max(0, col-1), min(self.board_dim, (col+1)+1)):
                if (i, j) in self.already_dug:
                    continue  # we have aready dug this spot

                self.dig(i, j)

        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(
            self.board_dim)] for _ in range(self.board_dim)]
        for row in range(self.board_dim):
            for col in range(self.board_dim):
                if (row, col) in self.already_dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.board_dim):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.board_dim)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.board_dim)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dimensions, number_of_bombs):

    board = Board(dimensions, number_of_bombs)
    safe = True
    while(len(board.already_dug) < board.board_dim**2 - number_of_bombs):
        print(board)
        row = int(input("Enter the row to dig (0-9): "))
        col = int(input("Enter the col to dig (0-9): "))

        if(row < 0 or row > dimensions-1 or col < 0 or col > dimensions):
            print("Invalid row or column, enter again : ")
            continue

        safe = board.dig(row, col)

        if not safe:
            break

    if safe:
        print("Congratulations, you have one the game : ")
    else:
        print("You dug up a bomb, game over :( ")

    for i in range(board.board_dim):
        for j in range(board.board_dim):
            print(board.board[i][j], end=" ")
        print(" ")


if __name__ == '__main__':
    print(" ")
    play(10, 10)
