from pieces import Piece, Bishop, King, Knight, Pawn, Queen, Rook
from int2 import int2

class Board:
    PieceIcons={'k': King, 'q': Queen, 'r': Rook, 'b': Bishop, 'n': Knight, 'p': Pawn}
    def __init__(self, FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
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
                assert(c.lower() in self.PieceIcons)
                
                white = c.isupper()
                
                piece = self.PieceIcons[c.lower()](white, int2(7-ind, file), self)
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
        self.enpassantTarget = int2(int(FEN[3][1])-1, ord(FEN[3][0])-97) if FEN[3]!='-' else None
        self.fiftyMoveRuleCounter = int(FEN[4])
        self.moveCounter = int(FEN[5])
        self.all_moves = {}
        self.parse_all_moves()
 
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
            case int2():
                return self.pos[index.x][index.y]
            case tuple():
                return self.pos[index[0]][index[1]]
            case int():
                return self.pos[index]
            case _:
                raise TypeError
 
    def __setitem__(self, index, value):
        if value is not None and not isinstance(value, Piece):
            raise ValueError
        match index:
            case int2():
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
 
    def parse_all_moves(self):
        self.all_moves = {}
        for rank in self.pos:
            for piece in rank:
                if piece and piece.white == self.whiteToMove:
                    for mv in piece.get_all_possible_moves():
                        if mv.tuple() not in self.all_moves:
                            self.all_moves[mv.tuple()] = []
                        self.all_moves[mv.tuple()].append(piece)
        
    @staticmethod
    def parse_pos(pos: str):
        assert len(pos)==2 and pos[0] in 'abcdefgh' and pos[1] in '12345678'
        return int2(int(pos[1])-1, ord(pos[0])-97)
    
    def move(self, mv: str):
        assert isinstance(mv, str)
        assert len(mv)>=4

        start = self.parse_pos(mv[:2])
        piece: Piece = self[start]

        assert piece is not None
        assert piece.white == self.whiteToMove

        all_mvs = piece.get_all_possible_moves()
        target = self.parse_pos(mv[2:4])
        assert target in all_mvs

        if isinstance(piece, Pawn) and target.x in [0, 7]:
            assert len(mv)==5
            piece = self.PieceIcons[mv[4].lower()](white = piece.white, pos = target, board = self)
        else:
            assert len(mv)==4
        if isinstance(piece, King) and target-start in (int2(0, 2), int2(0, -2)):
            rk = int2(target.x, 0 if target.y==2 else 7)
            rook = self[rk]
            self[rk] = None
            rk_trgt = int2(target.x, 3 if target.y==2 else 5)
            self[rk_trgt] = rook
            rook.pos = rk_trgt
    
        
        self[target] = piece
        piece.pos = target
        self[start] = None
        piece.castle = False

        self.whiteToMove = not self.whiteToMove
        self.parse_all_moves()
        assert not self.detect_checks()[::-1][int(piece.white)]
    
    def detect_checks(self):
        white = False
        black = False
        for mv, mvs in self.all_moves.items():
            if self[mv] and isinstance(self[mv], King) and mvs:
                if self[mv].white:
                    white = True
                else:
                    black = True
        return white, black