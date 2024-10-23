from Board import Board
 
if __name__ == "__main__":
    brd = Board("rnbqkbnr/pppppppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1")
    print(brd)
    def get_moves(x, y): 
        p = brd[x][y]
        mvs = p.get_all_possible_moves()
        print(mvs)
        print(*list(brd.algebraic_notation(p, mv) for mv in mvs))

    get_moves(4, 4)
 