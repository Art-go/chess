from Board import Board
 
if __name__ == "__main__":
    brd = Board()
    print(brd)
    p = brd[7][1]
    mvs = p.get_all_possible_moves()
    print(mvs)
    print(*list(brd.algebraic_notation(p, mv) for mv in mvs))
    p = brd[0][4]
    mvs = p.get_all_possible_moves()
    print(mvs)
    print(*list(brd.algebraic_notation(p, mv) for mv in mvs))
 