from dataclasses import dataclass
 
@dataclass
class Vector2Int:
    x: int = 0
    y: int = 0
 
    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError
 
        return Vector2Int(self.x + other.x, self.y + other.y)
 
    def __sub__(self, other):
        if type(self) != type(other):
            raise TypeError
 
        return Vector2Int(self.x - other.x, self.y - other.y)
 
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.x==other.x and self.y==other.y
 
 
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
 
class Knight(Piece):
    icon = 'n'
    pattern = [Vector2Int(1, 2),Vector2Int(-1, 2),Vector2Int(1, -2),Vector2Int(-1, -2),
               Vector2Int(2, 1),Vector2Int(-2, 1),Vector2Int(2, -1),Vector2Int(-2, -1)]
 
    def get_all_possible_moves(self):
        return self.trim_moves([i+self.pos for i in self.pattern])
 
class Rook(Piece):
    icon = "r"
    pattern = [Vector2Int(0, 1),Vector2Int(1,0),Vector2Int(0,-1),Vector2Int(-1,0)]
 
    def get_all_possible_moves(self):
        ...
 
class Bishop(Piece):
    icon = "b"
 
class Queen(Piece):
    icon = "q"
 
class King(Piece):
    icon = "k"
    pattern = [Vector2Int(0, 1),Vector2Int(1,0),Vector2Int(0,-1),Vector2Int(-1,0),
               Vector2Int(1, 1),Vector2Int(1,-1),Vector2Int(-1,1),Vector2Int(-1,-1)]
    
    def get_all_possible_moves(self):
        moves = self.trim_moves([i+self.pos for i in self.pattern])
        
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
 
class Board:
    FEN_notation={'k': King, 'q': Queen, 'r': Rook, 'b': Bishop, 'n': Knight, 'p': Pawn}
    def __init__(self, FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1") -> None:
        FEN = FEN.split()
        assert(len(FEN)==6)
 
        castling = [False, False, False, False]
        if FEN[2]!='-':
            if 'K' in FEN[2]:
                castling[0] = True
            if 'Q' in FEN[2]:
                castling[1] = True
            if 'k' in FEN[2]:
                castling[2] = True
            if 'q' in FEN[2]:
                castling[3] = True
 
        FEN_pos = FEN[0].split('/')
        assert(len(FEN_pos)==8)
 
        self.pos = [[None for _ in range(8)] for _ in range(8)]
        for ind, rank in enumerate(FEN_pos):
            file = 0
            for c in rank:
                if c.isdigit():
                    file+=int(c)
                    continue
                assert(c.lower() in self.FEN_notation)
                
                white = c.isupper()
                
                piece = self.FEN_notation[c.lower()](white, Vector2Int(7-ind, file), self)
                pos = (7-ind, file)
                self.pos[7-ind][file] = piece
                file+=1
                
                if c.lower()=='k' and ((white and (castling[0] or castling[1])) or (not white and (castling[2] or castling[3]))):
                    piece.castle = True
                
                if c.lower()!='r':
                    continue
                
                if white:
                    if pos == (0, 0):
                        if castling[1]:
                            castling[1]=False
                            piece.castle=True
                    if pos == (0, 7):
                        if castling[0]:
                            castling[0]=False
                            piece.castle=True
                else:
                    if pos == (7, 0):
                        if castling[3]:
                            castling[3]=False
                            piece.castle=True
                            
                    if pos == (7, 7):
                        if castling[2]:
                            castling[2]=False
                            piece.castle=True

            assert(file==8)
        assert(not any(castling))
        
        self.whiteToMove = FEN[1] == 'w'
        self.enpassantTarget = Vector2Int(ord(FEN[3][0])-97, int(FEN[3][1])) if FEN[3]!='-' else None
        self.fiftyMoveRuleCounter = int(FEN[4])
        self.moveCounter = int(FEN[5])
 
    def __str__(self):
        template = "##A=B=C=D=E=F=G=H=##\n" \
                   "8|{56} {57}#{58} {59}#{60} {61}#{62} {63}#|8\n" \
                   "7|{48}#{49} {50}#{51} {52}#{53} {54}#{55} |7\n" \
                   "6|{40} {41}#{42} {43}#{44} {45}#{46} {47}#|6\n" \
                   "5|{32}#{33} {34}#{35} {36}#{37} {38}#{39} |5\n" \
                   "4|{24} {25}#{26} {27}#{28} {29}#{30} {31}#|4\n" \
                   "3|{16}#{17} {18}#{19} {20}#{21} {22}#{23} |3\n" \
                   "2|{8} {9}#{10} {11}#{12} {13}#{14} {15}#|2\n" \
                   "1|{0}#{1} {2}#{3} {4}#{5} {6}#{7} |1\n" \
                   "##A=B=C=D=E=F=G=H=##"
        formatReadyPos = []
        for i, rank in enumerate(self.pos):
            for j, square in enumerate(rank):
                formatReadyPos.append(square.icon if square is not None else '# '[(i+j)%2])
 
        return template.format(*formatReadyPos)

    def __getitem__(self, index):
        match index:
            case Vector2Int():
                return self.pos[index.x][index.y]
            case int():
                return self.pos[index]
            case _:
                raise TypeError
 
    def __setitem__(self, index, value):
        if value is not None and not isinstance(value, Piece):
            raise ValueError
        match index:
            case Vector2Int():
                self.pos[index.x][index.y]=value
                if value:
                    value.pos=index
            case _:
                raise TypeError
 
    def algebraic_notation(self, piece, target, ambRank = False, ambFile = False, check = False, mate = False):
        move = ""
 
        if not isinstance(piece, Pawn):
            move+=piece.icon.upper()
 
        start = piece.pos
 
        if ambFile:
            move+='abcdefgh'[start.y]
        if ambRank:
            move+='12345678'[start.x]
 
        if self[target]:
            move+='x'
 
        move+='abcdefgh'[target.y]
        move+='12345678'[target.x]
 
        if mate:
            move+='#'
        elif check:
            move+='+'
 
        return move
 
    def get_all_moves(self):
        for rank in self.pos:
            for piece in rank:
                if piece and piece.white == self.whiteToMove:
                    ...
 
if __name__ == "__main__":
    brd = Board("rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")
    print(brd)
    p = brd[0][1]
    mvs = p.get_all_possible_moves()
    print(mvs)
    print(*list(brd.algebraic_notation(p, mv) for mv in mvs))
    p = brd[0][4]
    mvs = p.get_all_possible_moves()
    print(mvs)
    print(*list(brd.algebraic_notation(p, mv) for mv in mvs))
 