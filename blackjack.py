import pygame
import random

# Constants
WIDTH, HEIGHT = 900, 650
WHITE = (210, 210, 210)
BLACK = (0, 0, 0)
GREEN = (0, 100, 20)
SILVER = (135, 135, 135)
CARD_WIDTH, CARD_HEIGHT = 80, 120

# Card suits and ranks
SUITS = ['♥', '♦', '♠', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class BlackjackGame:
    def __init__(self):
        """Initialize the game, Pygame, and its state."""
        # Game and UI state
        self.player_turn = True
        self.game_over = False
        self.winner_text = ""
        self.shuffle_message = ""
        self.shuffle_count = 0
        self.previous_shuffles = []

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Blackjack")
        self.font = pygame.font.SysFont('Arial', 36)
        self.clock = pygame.time.Clock()

        # Create card images
        self.card_images = {}
        for suit in SUITS:
            for rank in RANKS:
                # Create a surface for the card
                self.card_images[f'{rank}{suit}'] = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
                self.card_images[f'{rank}{suit}'].fill(WHITE)
                pygame.draw.rect(self.card_images[f'{rank}{suit}'], BLACK, self.card_images[f'{rank}{suit}'].get_rect(), 2)

                # Render and draw text for card rank and suit
                text_top_left = self.font.render(rank, 1, f"{'RED' if suit in '♥♦' else 'BLACK'}")
                self.card_images[f'{rank}{suit}'].blit(text_top_left, (10, 10))

                text_center = self.font.render(suit, True, f"{'RED' if suit in '♥♦' else 'BLACK'}")
                self.card_images[f'{rank}{suit}'].blit(text_center, (
                    (CARD_WIDTH - text_center.get_width()) // 2, (CARD_HEIGHT - text_center.get_height()) // 2))

                text_bottom_right = self.font.render(rank, True, f"{'RED' if suit in '♥♦' else 'BLACK'}")
                self.card_images[f'{rank}{suit}'].blit(text_bottom_right, (
                    CARD_WIDTH - text_bottom_right.get_width() - 10, CARD_HEIGHT - text_bottom_right.get_height() - 10))

        self.reset_game()

    def reset_game(self):
        """Reset the game state and shuffle the deck."""
        # Initialize the deck and shuffle it
        self.deck = [f'{rank}{suit}' for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)

        # Deal initial hands
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        # Reset game state
        self.player_turn = True
        self.game_over = False
        self.winner_text = ""
        self.shuffle_message = ""
        self.shuffle_count = 0
        self.previous_shuffles = []

    def shuffle_deck(self):
        """Shuffle the deck with a limit of 3 times."""
        if self.shuffle_count < 3:
            # Save the top 3 cards from the current deck
            self.previous_shuffles.append(self.deck[:3])
            random.shuffle(self.deck)
            self.shuffle_count += 1
            self.shuffle_message = f"Deck has been shuffled {self.shuffle_count}/3 times!"
        else:
            self.shuffle_message = "3 times shuffle limit!"

    def calculate_hand_value(self, hand):
        """Calculate the Blackjack value of a given hand."""
        value = 0
        aces = 0

        # Calculate card values
        for card in hand:
            card_rank = card[:-1] # Extracts the rank (everything but the last character (suit) - `8H` -> `H`, `AS` -> `S`)
            if card_rank in 'JQK':
                value += 10
            elif card_rank == 'A':
                aces += 1
                value += 11
            else:
                value += int(card_rank)

        # Adjust for aces if the value exceeds 21
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def check_winner(self):
        """Determine the winner based on hand values."""
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        # Determine winner conditions
        if player_value > 21:
            self.winner_text = "Player busts! Dealer wins!"
            self.player_turn = False
        elif dealer_value > 21:
            self.winner_text = "Dealer busts! Player wins!"
        elif player_value > dealer_value:
            self.winner_text = "Player wins!"
        elif player_value < dealer_value:
            self.winner_text = "Dealer wins!"
        else:
            self.winner_text = "It's a tie!"
        self.game_over = True

    def draw_hand(self, hand, x, y, hide_first_card=False):
        """Draw a hand of cards on the screen."""
        for i, card in enumerate(hand):
            if hide_first_card and i == 0:
                pygame.draw.rect(self.screen, BLACK, (x + i * (CARD_WIDTH + 10), y, CARD_WIDTH, CARD_HEIGHT))
            else:
                self.screen.blit(self.card_images[card], (x + i * (CARD_WIDTH + 10), y))

    def draw_button(self, text, x, y, width, height):
        """Draw a button with text."""
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height))
        pygame.draw.rect(self.screen, WHITE, (x + 2, y + 2, width - 4, height - 4))
        button_text = self.font.render(text, True, BLACK)
        self.screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))

    def draw_previous_shuffles(self):
        """Draw the previous shuffle results on the screen."""
        x_offset = WIDTH - (3 * (CARD_WIDTH + 10)) - 50
        y_offset = 20

        for i, shuffle in enumerate(self.previous_shuffles):
            shuffle_text = self.font.render(f'Shuffle {i + 1}:', True, SILVER)
            self.screen.blit(shuffle_text, (x_offset, y_offset))

            for j, card in enumerate(shuffle):
                self.screen.blit(self.card_images[card], (x_offset + j * (CARD_WIDTH + 10), y_offset + 40))
            y_offset += CARD_HEIGHT + 60

    def main(self):
        running = True
        draw_shuffles = False
        more_button_rect = pygame.Rect(450, 580, 100, 50)
        stop_button_rect = pygame.Rect(600, 580, 100, 50)
        replay_button_rect = pygame.Rect(750, 580, 100, 50)
        shuffle_button_rect = pygame.Rect(300, 580, 100, 50)
        draw_shuffles_button_rect = pygame.Rect(40, 580, 200, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player_turn:
                        if more_button_rect.collidepoint(event.pos):
                            self.player_hand.append(self.deck.pop())
                            if self.calculate_hand_value(self.player_hand) > 21:
                                self.check_winner()
                        elif stop_button_rect.collidepoint(event.pos):
                            self.player_turn = False
                            while self.calculate_hand_value(self.dealer_hand) < 17:
                                self.dealer_hand.append(self.deck.pop())
                            self.check_winner()
                        elif shuffle_button_rect.collidepoint(event.pos):
                            self.shuffle_deck()
                    elif self.game_over:
                        if replay_button_rect.collidepoint(event.pos):
                            self.reset_game()
                            draw_shuffles = False
                        elif draw_shuffles_button_rect.collidepoint(event.pos):
                            draw_shuffles = True

            self.screen.fill(GREEN)
            self.draw_hand(self.player_hand, 50, 400)
            self.draw_hand(self.dealer_hand, 50, 50, hide_first_card=self.player_turn)

            player_value = self.calculate_hand_value(self.player_hand)
            dealer_value = self.calculate_hand_value(self.dealer_hand)

            player_text = self.font.render(f'Player score: {player_value}', True, SILVER)
            dealer_text = self.font.render(f'Dealer score: {dealer_value if not self.player_turn else "??"}', True, SILVER)

            self.screen.blit(player_text, (50, 350))
            self.screen.blit(dealer_text, (50, 5))

            self.draw_button("More", 450, 580, 100, 50)
            self.draw_button("Stop", 600, 580, 100, 50)
            self.draw_button("Shuffle", 300, 580, 100, 50)
            if self.game_over:
                self.draw_button("Replay", 750, 580, 100, 50)
                self.draw_button("Draw Shuffles", 40, 580, 200, 50)
                winner_text_render = self.font.render(self.winner_text, True, BLACK)
                self.screen.blit(winner_text_render, (50, HEIGHT // 2 - 130))
                if draw_shuffles:
                    self.draw_previous_shuffles()

            if self.shuffle_message:
                shuffle_message_render = self.font.render(self.shuffle_message, True, SILVER)
                self.screen.blit(shuffle_message_render, (50, HEIGHT // 2 - 60))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = BlackjackGame()
    game.main()