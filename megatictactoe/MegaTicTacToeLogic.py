'''
Board class for the game of TicTacToe.
Default board size is 3x3.
Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

'''
# from bkcharts.attributes import color
class Board():

    # list of all 8 directions on the board, as (x,y) offsets

    def __init__(self, n=9):
        "Set up initial board configuration."

        self.n = n
        self.metapieces = [None]*9
        # Create the empty board array.
        self.pieces = [None]*(self.n+1)
        for i in range(self.n):
            self.pieces[i] = [0]*self.n
        self.pieces[-1] = [1]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.

        for i in range(self.n):
            self.metapieces[i] = self.has_won_square(self[i])

        # Get all the empty squares (color==0)
        for square in enumerate(self.pieces[-1]):
            if self.metapieces[square[0]] == 0 and square[1] == 1:
                for x in range(self.n):
                    if self[square[0][x]]==0:
                        newmove = (square[0],x)
                        moves.add(newmove)
        return list(moves)

    def has_legal_moves(self):
        for square in enumerate(self.pieces[-1]):
            if self.metapieces[square[0]] == 0 and square[1] == 1:
                for x in range(self.n):
                    if self[square[0]][x]==0:
                        return True
        return False
    
    def has_won_square(self, square):
        """Check whether a given square list has been won;
        Returns the color of winnner.
        """
        winning_pos = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for i in winning_pos:
            if square[i[0]] == square[i[1]] and square[i[1]] == square[i[2]]:
                return square[i[0]]
        return 0

    def is_win(self, color):
        """Check whether the given player has collected a triplet in any direction; 
        Returns True if color has won.
        """
        for i in range(self.n):
            self.metapieces[i] = self.has_won_square(self[i])
        return color == self.has_won_square(self.metapieces)

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (x,y) = move

        # Add the piece to the empty square.
        assert self[x][y] == 0
        assert x < 9
        assert y < 9
        assert self[-1][x] == 1

        self[-1] = [0]*9
        self[x][y] = color
        for i in range(self.n):
            self.metapieces[i] = abs(self.has_won_square(self[i]))
        if self.metapieces[x] == 0:
            self[-1][x] = 1
        else:
            self[-1] = list(np.array(self.metapieces)*-1+1)

