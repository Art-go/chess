from int2 import int2
 
class Piece:
    icon = ' '
    def __init__(self, white: bool, pos: int2, board, castle = False) -> None:
        self.white = white
        self.pos = pos
        self.icon = self.icon.upper() if white else self.icon
        self.board = board
        self.castle = castle
 
    def get_all_possible_moves(self) -> list[int2]:
        raise NotImplementedError
 
    def trim_moves(self, moves: list[int2]) -> list[int2]:
        return [i for i in moves if (0 <= i.x <= 7) and (0 <= i.y <= 7) and (not self.board[i] or self.board[i].white!=self.white)]
    
    def __repr__(self):
        return f"{self.icon}@{self.pos.tuple()}"
 
class StandardPiece(Piece):
    pattern = ()
    inf = True
    def get_all_possible_moves(self) -> list[int2]:
        if not self.inf:
            return self.trim_moves([i+self.pos for i in self.pattern]) 
        moves = []
        temp_moves = self.trim_patterned_moves([(i, i+self.pos) for i in self.pattern])
        while temp_moves:
            moves+=[i[1] for i in temp_moves]

            temp_moves = self.captures_trim(temp_moves)
            temp_moves = [(dp, dp+pos) for dp, pos in temp_moves]

            temp_moves = self.trim_patterned_moves(temp_moves)
            
        return moves
    
    def trim_patterned_moves(self, moves: list[tuple[int2, int2]]) -> list[tuple[int2, int2]]:
        return [i for i in moves if (0 <= i[1].x <= 7) and (0 <= i[1].y <= 7) and (not self.board[i[1]] or self.board[i[1]].white!=self.white)]
    
    def captures_trim(self, moves: list[tuple[int2, int2]]) -> list[tuple[int2, int2]]:
        return [i for i in moves if not self.board[i[1]]]


class Knight(StandardPiece):
    icon = 'n'
    pattern = [int2(1, 2),int2(-1, 2),int2(1, -2),int2(-1, -2),
               int2(2, 1),int2(-2, 1),int2(2, -1),int2(-2, -1)]
    inf = False
 
class Rook(StandardPiece):
    icon = "r"
    pattern = [int2(0, 1),int2(1,0),int2(0,-1),int2(-1,0)]
 
class Bishop(StandardPiece):
    icon = "b"
    pattern = [int2(1, 1),int2(1,-1),int2(-1,-1),int2(-1,1)]
 
class Queen(StandardPiece):
    icon = "q"
    pattern = [int2(0, 1),int2(1,0),int2(0,-1),int2(-1,0),
               int2(1, 1),int2(1,-1),int2(-1,1),int2(-1,-1)]
 
class King(StandardPiece):
    icon = "k"
    pattern = [int2(0, 1),int2(1,0),int2(0,-1),int2(-1,0),
               int2(1, 1),int2(1,-1),int2(-1,1),int2(-1,-1)]
    inf = False
    
    def get_all_possible_moves(self):
        moves = super().get_all_possible_moves()
        
        if self.castle:
            assert(self.pos == (int2(7, 4), int2(0, 4))[int(self.white)])
            if self.white:
                if self.board[0][0].castle and self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None:
                    moves.append(int2(0, 2))
                if self.board[0][7].castle and self.board[0][6] is None and self.board[0][5] is None:
                    moves.append(int2(0, 6))
            else:
                if self.board[7][0].castle and self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None:
                    moves.append(int2(7, 2))
                if self.board[7][7].castle and self.board[7][6] is None and self.board[7][5] is None:
                    moves.append(int2(7, 6))
        
        return moves
 
class Pawn(Piece):
    icon = "p"

    def __init__(self, white, pos, board, castle=False):
        super().__init__(white, pos, board, castle)
        self.pattern = (int2(1, 0), int2(2, 0), int2(1,-1), int2(1, 1))
        self.start = 1
        self.promotion = 7
        if not self.white:
            self.pattern = (i*-1 for i in self.pattern)
            self.start = 6
            self.promotion = 0

    def get_all_possible_moves(self):
        moves=[]
        
        if not self.board[self.pos + self.pattern[0]]:
            moves.append(self.pos + self.pattern[0])
            if self.pos.x==self.start and not self.board[self.pos + self.pattern[1]]:
                moves.append(self.pos + self.pattern[1])
        
        mv = self.pos + self.pattern[2]
        print(self.board.enpassantTarget)
        if (0 <= mv.x <= 7) and (0 <= mv.y <= 7) and (self.board[mv] and self.board[mv].white!=self.white) or self.board.enpassantTarget and mv==self.board.enpassantTarget:
            moves.append(mv)
        
        mv = self.pos + self.pattern[3]
        if (0 <= mv.x <= 7) and (0 <= mv.y <= 7) and (self.board[mv] and self.board[mv].white!=self.white) or self.board.enpassantTarget and mv==self.board.enpassantTarget:
            moves.append(mv)
        
        return moves