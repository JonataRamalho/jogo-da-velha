import copy
from queue import Queue
from SearchBfs import bfs, node_to_path


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.position = ()
    
    def __eq__(self, other):
        return isinstance(other, TicTacToe) and self.board == other.board

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))


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

            for i in range(3):
                row_info = current_state.board[i][:] 
                try:
                    position_with_empty_space = row_info.index(' ')
                except: 
                    position_with_empty_space = None
                
                if row_info.count('X') == 2 and position_with_empty_space: #alterado para >= 0 pois quando o indice for ZERO o python entende como False.
                    if (i, position_with_empty_space) == current_state.position:
                        return True
                    return False
                
                x_counter = 0 
                keep_searching = True

                while keep_searching:
                    for j in range(3):
                        LIMIT = 2
                        position_with_empty_space = None
                        column_info = current_state.board[j][i]

                        if(column_info == 'X'):
                            x_counter += 1
                            position_with_empty_space = None
                        else:
                            position_with_empty_space = j

                        if (x_counter >= 2 and position_with_empty_space):
                            keep_searching = False

                            if (position_with_empty_space, i) == current_state.position:
                                return True
                            
                            return False
                        
                        if(j == LIMIT and x_counter < 2):
                            keep_searching = False

            return True
                    
        return False
    
    
    def successors(self, current_state):
        successors_list = []

        if not self.is_full():
            empty_cells = self.get_empty_cells()
            for i, j in empty_cells:
                new_game = copy.deepcopy(self)
                new_game.make_move(i, j)
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

    total_moves = 0

    while True:
        row = int(input("Insira a linha (0, 1, 2): "))
        col = int(input("Insira a coluna (0, 1, 2): "))
        
        if not (0 <= row <= 2) or not (0 <= col <= 2):
            print("Entrada inválida. Digite números entre 0 e 2.")
            continue
        
        if not game.make_move(row, col):
            print("Movimento inválido. Tente novamente.")
            continue
        
        game.print_board()
        
        winner = game.check_winner()
        if winner:
            print(f"{winner} ganhou!")
            break
        
        total_moves += 1
        # Limite para empate - precisa melhorar
        if total_moves == 3 and not winner:
            print("É um empate!")
            break
        
        print("É a vez do computador:")

        bfs_path = bfs(game, game.goal_test, game.successors)

        if bfs_path:
            path = node_to_path(bfs_path)
            for move in path:
                if len(move.position) > 0:
                    game.make_move(*move.position)
                    game.print_board()
                    print()
        else:
            print("Não foi encontrada nenhuma jogada para o computador.")
            break


if __name__ == "__main__":
    main()
