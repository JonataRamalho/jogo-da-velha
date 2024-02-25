import copy
from queue import Queue
from SearchBfs import bfs, node_to_path
# from typing import List, Optional


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.position = ()

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.player
            self.player = 'X' if self.player == 'O' else 'O'
            return True
        return False
    
    def make_move_test(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.player
            
            if(self.player == 'X'):
                self.player == '0'
            
            return True
        return False

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    def get_empty_cells(self):
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    empty_cells.append((i, j))
        return empty_cells

    def goal_test(self, current_state):
        if self.player == "O" and current_state != self:
            return True
        return False

    def successors(self, current_state):
        successors_list = []

        if not self.is_full():
            empty_cells = self.get_empty_cells()
            for i, j in empty_cells:
                new_game = copy.deepcopy(self)
                # new_game.make_move(i, j)
                new_game.position = (i, j)
                successors_list.append(new_game)

        return successors_list
        
def bfs_chat(game):
    queue = Queue()
    queue.put((game, []))

    while not queue.empty():
        node, path = queue.get()
        if node.check_winner() == 'X':
            return path
        elif not node.is_full():
            empty_cells = node.get_empty_cells()
            for i, j in empty_cells:
                new_game = copy.deepcopy(node)
                new_game.make_move(i, j)
                queue.put((new_game, path + [(i, j)]))
        print('path', path)
        print('queue', queue)
    return None


def main():
    game = TicTacToe()
    game.print_board()

    while not game.is_full() and not game.check_winner():
        row = int(input("Enter row (0, 1, 2): "))
        col = int(input("Enter column (0, 1, 2): "))
        
        if not (0 <= row <= 2) or not (0 <= col <= 2):
            print("Invalid input. Please enter numbers between 0 and 2.")
            continue
        
        if not game.make_move(row, col):
            print("Invalid move. Try again.")
            continue
        
        game.print_board()
        
        if game.check_winner():
            print("You won!")
            break
        
        if game.is_full():
            print("It's a draw!")
            break
        
        print("Computer's turn:")

        bfs_path = bfs(game, game.goal_test, game.successors)
        # bfs_path = bfs_chat(game)


        if bfs_path:
            path = node_to_path(bfs_path)
            for move in path:
                if len(move.position) > 0:
                    game.make_move(*move.position)
                    game.print_board()
                    print()
        else:
            print("No winning move found for the computer.")
            break

if __name__ == "__main__":
    main()
