from Board import Board
 
if __name__ == "__main__":
    brd = Board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    while True:
        print(brd)
        brd.move(input())