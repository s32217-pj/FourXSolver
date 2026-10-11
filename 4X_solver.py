from easyAI import AI_Player, Human_Player, Negamax, TwoPlayerGame


class FourXGame(TwoPlayerGame):
    """
    Represent a 6x6 Four X game with restrictions on consecutive symbols.

    Players take turns placing their symbols on the board. Creating exactly
    three consecutive symbols is forbidden, while connecting four or more
    consecutive symbols wins the game.
    """

    def __init__(self, players):
        self.players = players
        super().__init__()
        self.board = [0 for i in range(6**2)]
        self.current_player = 1

        for p in self.players:
            p.game = self

    def possible_moves(self) -> list[int]:
        """Returns array with indexes where move can be done"""
        return [i for i in range(6**2) if self.board[i] == 0 and self._is_valid(i)]

    def _is_valid(self, move) -> bool:
        self.board[move] = self.current_player

        valid = self._has_four(self.current_player) or not self._has_three(self.current_player)

        self.board[move] = 0
        return valid

    def make_move(self, move):
        self.board[move] = self.current_player

    def unmake_move(self, move):
        self.board[move] = 0

    def _has_four(self, player) -> bool:
        """
        Check whether a player has four or more consecutive symbols.

        Searches horizontally, vertically, and diagonally in both diagonal
        directions.

        Args:
            player (int): The player identifier to check.
        """
        
        directions = [
            (0, 1),    # horizontal
            (1, 0),    # vertical
            (1, 1),    # diagonal \
            (1, -1),   # diagonal /
        ]

        for r in range(6):
            for c in range(6):
                for dr, dc in directions:
                    end_r = r + 3 * dr
                    end_c = c + 3 * dc

                    #Bounds check
                    if not (0 <= end_r < 6 and 0 <= end_c < 6):
                        continue

                    if all( self.board[(r + k * dr) * 6 + c + k * dc] == player
                            for k in range(4)
                        ):
                        return True

        return False

    def _has_three(self, player) -> bool:
        """
        Check whether a player has exactly three consecutive symbols.

        Searches in all four directions. A sequence is considered forbidden
        only if it cannot be extended by the same player's symbol at either
        end. Sequences that are part of a longer line are ignored.

        Args:
            player (int): The player identifier to check.
        """
        
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        for r in range(6):
            for c in range(6):
                for dr, dc in directions:
                    end_r = r + 2 * dr
                    end_c = c + 2 * dc

                    #Bounds check
                    if not (0 <= end_r < 6 and 0 <= end_c < 6):
                        continue

                    #Look for 3 in a row pattern
                    if not all( self.board[(r + k * dr) * 6 + c + k * dc] == player
                        for k in range(3)
                    ):
                        continue

                    #3 in a row pattern has been found, check if it is alone (forbidden)
                    # Before
                    prev_r = r - dr
                    prev_c = c - dc

                    #Bounds check and make sure it belongs to the player
                    prev_same = (
                        0 <= prev_r < 6
                        and 0 <= prev_c < 6
                        and self.board[prev_r * 6 + prev_c] == player
                    )

                    # After 
                    next_r = r + 3 * dr
                    next_c = c + 3 * dc

                    #Bounds check and make sure it belongs to the player
                    next_same = (
                        0 <= next_r < 6
                        and 0 <= next_c < 6
                        and self.board[next_r * 6 + next_c] == player
                    )

                    #alone 3 in a row pattern has been found
                    if not prev_same and not next_same:
                        return True

        return False

    def win(self):
        return self._has_four(self.current_player)

    def is_over(self):
        return self.win() or len(self.possible_moves()) == 0

    def scoring(self):
        return 100 if self.win() else 0

    def show(self):
        """Prints the plande with padding added and indexes"""
        print()

        for r in range(6):
            cells = []

            for c in range(6):
                index = r * 6 + c
                value = self.board[index]

                if value == 0:   symbol = str(index)
                elif value == 1: symbol = "X"
                else:            symbol = "O"

                #Add padding (3)
                cells.append(f"{symbol:>3}")

            print(" ".join(cells))

        print()

    def play(self):
        """Start the game"""

        while not self.is_over():
            self.show()

            valid_moves = self.possible_moves()

            if not valid_moves:
                print("Draw! No valid moves available.")
                break

            if self.current_player == 1:
                try:
                    move = int(input("Choose a cell (0-35): "))
                except ValueError:
                    print("Error: Please enter an integer.")
                    continue

                if move not in range(36):
                    print("Error: The cell index must be between 0 and 35.")
                    continue

                if move not in valid_moves:
                    print("Invalid move or move creates a forbidden triple.")
                    continue
            else:
                print("AI is thinking...")
                move = self.players[1].ask_move(self)
                print(f"AI selected cell: {move}")

            self.make_move(move)

            if self.win():
                self.show()
                print(
                    "Congratulations! You won!"
                    if self.current_player == 1
                    else "The AI won!"
                )
                return

            self.switch_player()

        self.show()
        print("Game over! It's a draw.")


if __name__ == "__main__":
    ai = Negamax(3)
    game = FourXGame([Human_Player(), AI_Player(ai)])
    game.play()