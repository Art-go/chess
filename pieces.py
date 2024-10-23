from Vector2Int import Vector2Int
 
class Piece:
    icon = ' '
    def __init__(self, white: bool, pos: Vector2Int, board, castle = False) -> None:
        self.white = white
        self.pos = pos
        self.icon = self.icon.upper() if white else self.icon
        self.board = board
        self.castle = castle
 
    def get_all_possible_moves(self) -> list[Vector2Int]:
        raise NotImplementedError
 
    def trim_moves(self, moves: list[Vector2Int]) -> list[Vector2Int]:
        return [i for i in moves if (0 <= i.x <= 7) and (0 <= i.y <= 7) and (not self.board[i] or self.board[i].white!=self.white)]
 
class StandardPiece(Piece):
    pattern = ()
    inf = True
    def get_all_possible_moves(self) -> list[Vector2Int]:
        moves = self.trim_moves([i+self.pos for i in self.pattern]) 
        if not self.inf:
            return moves
        raise NotImplemented

class Knight(StandardPiece):
    icon = 'n'
    pattern = [Vector2Int(1, 2),Vector2Int(-1, 2),Vector2Int(1, -2),Vector2Int(-1, -2),
               Vector2Int(2, 1),Vector2Int(-2, 1),Vector2Int(2, -1),Vector2Int(-2, -1)]
    inf = False
 
class Rook(StandardPiece):
    icon = "r"
    pattern = [Vector2Int(0, 1),Vector2Int(1,0),Vector2Int(0,-1),Vector2Int(-1,0)]
 
class Bishop(StandardPiece):
    icon = "b"
    pattern = [Vector2Int(1, 1),Vector2Int(1,-1),Vector2Int(-1,-1),Vector2Int(-1,1)]
 
class Queen(StandardPiece):
    icon = "q"
    pattern = [Vector2Int(0, 1),Vector2Int(1,0),Vector2Int(0,-1),Vector2Int(-1,0),
               Vector2Int(1, 1),Vector2Int(1,-1),Vector2Int(-1,1),Vector2Int(-1,-1)]
 
class King(StandardPiece):
    icon = "k"
    pattern = [Vector2Int(0, 1),Vector2Int(1,0),Vector2Int(0,-1),Vector2Int(-1,0),
               Vector2Int(1, 1),Vector2Int(1,-1),Vector2Int(-1,1),Vector2Int(-1,-1)]
    inf = False
    
    def get_all_possible_moves(self):
        moves = super().get_all_possible_moves()
        
        if self.castle:
            assert(self.pos == (Vector2Int(7, 4), Vector2Int(0, 4))[int(self.white)])
            if self.white:
                if self.board[0][0].castle and self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None:
                    moves.append(Vector2Int(0, 2))
                if self.board[0][7].castle and self.board[0][6] is None and self.board[0][5] is None:
                    moves.append(Vector2Int(0, 6))
            else:
                if self.board[7][0].castle and self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None:
                    moves.append(Vector2Int(7, 2))
                if self.board[7][7].castle and self.board[7][6] is None and self.board[7][5] is None:
                    moves.append(Vector2Int(7, 6))
        
        return moves
 
class Pawn(Piece):
    icon = "p"