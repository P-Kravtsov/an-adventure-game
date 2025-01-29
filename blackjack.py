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

# Global variables
player_turn = True
game_over = False
winner_text = ""
shuffle_message = ""
shuffle_count = 0
previous_shuffles = []

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont('Arial', 36)
clock = pygame.time.Clock()

# Create card images
card_images = {}
for suit in SUITS:
    for rank in RANKS:
        # Create card image
        card_images[f'{rank}{suit}'] = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        card_images[f'{rank}{suit}'].fill(WHITE)
        pygame.draw.rect(card_images[f'{rank}{suit}'], BLACK, card_images[f'{rank}{suit}'].get_rect(), 2)

        # Render rank at top-left
        text_top_left = font.render(rank, 1, f"{'RED' if suit in '♥♦' else 'BLACK'}")
        card_images[f'{rank}{suit}'].blit(text_top_left, (10, 10))

        # Render suit at center
        text_center = font.render(suit, True, f"{'RED' if suit in '♥♦' else 'BLACK'}")
        card_images[f'{rank}{suit}'].blit(text_center, (
        (CARD_WIDTH - text_center.get_width()) // 2, (CARD_HEIGHT - text_center.get_height()) // 2))

        # Render rank at bottom-right
        text_bottom_right = font.render(rank, True, f"{'RED' if suit in '♥♦' else 'BLACK'}")
        card_images[f'{rank}{suit}'].blit(text_bottom_right, (
        CARD_WIDTH - text_bottom_right.get_width() - 10, CARD_HEIGHT - text_bottom_right.get_height() - 10))

# Deck of cards
deck = [f'{rank}{suit}' for suit in SUITS for rank in RANKS]
random.shuffle(deck)

# Deal initial cards
player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]


def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        card_rank = card[:-1] # - Extracts the rank (everything except the last character (suit) - `8H` becomes `H`, `AS` becomes `S`)
        if card_rank in 'JQK':
            value += 10
        elif card_rank == 'A':
            aces += 1
            value += 11
        else:
            value += int(card_rank)

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value


def draw_hand(hand, x, y, hide_first_card=False):
    for i, card in enumerate(hand):
        if hide_first_card and i == 0:
            pygame.draw.rect(screen, BLACK, (x + i * (CARD_WIDTH + 10), y, CARD_WIDTH, CARD_HEIGHT))
        else:
            screen.blit(card_images[card], (x + i * (CARD_WIDTH + 10), y))


def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, BLACK, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x + 2, y + 2, width - 4, height - 4))
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))


def reset_game():
    global player_hand, dealer_hand, deck, player_turn, game_over, winner_text, shuffle_message, shuffle_count, previous_shuffles
    deck = [f'{card_rank}{card_suit}' for card_suit in SUITS for card_rank in RANKS]
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    player_turn = True
    game_over = False
    winner_text = ""
    shuffle_message = ""
    shuffle_count = 0
    previous_shuffles = []


def shuffle_deck():
    global deck, shuffle_message, shuffle_count, previous_shuffles
    if shuffle_count < 3:
        previous_shuffles.append(deck[:3])  # Store the top three cards before shuffling
        random.shuffle(deck)
        shuffle_count += 1
        shuffle_message = f"Deck has been shuffled {shuffle_count}/3 times!"
    else:
        shuffle_message = "3 times shuffle limit!"


def check_winner():
    global game_over, winner_text, player_turn
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    if player_value > 21:
        winner_text = "Player busts! Dealer wins!"
        player_turn = False
    elif dealer_value > 21:
        winner_text = "Dealer busts! Player wins!"
    elif player_value > dealer_value:
        winner_text = "Player wins!"
    elif player_value < dealer_value:
        winner_text = "Dealer wins!"
    else:
        winner_text = "It's a tie!"
    game_over = True


def draw_previous_shuffles():
    x_offset = WIDTH - (3 * (CARD_WIDTH + 10)) - 50  # Position the cards on the right side
    y_offset = 20
    for i, shuffle in enumerate(previous_shuffles):
        shuffle_text = font.render(f'Shuffle {i+1}:', True, SILVER)
        screen.blit(shuffle_text, (x_offset, y_offset))
        for j, card in enumerate(shuffle):
            screen.blit(card_images[card], (x_offset + j * (CARD_WIDTH + 10), y_offset + 40))
        y_offset += CARD_HEIGHT + 60

def main():
    global player_turn, game_over, winner_text, shuffle_message
    running = True
    player_turn = True
    game_over = False
    winner_text = ""
    shuffle_message = ""
    draw_shuffles = False  # Flag to control drawing previous shuffles
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
                if player_turn:
                    if more_button_rect.collidepoint(event.pos):
                        player_hand.append(deck.pop())
                        if calculate_hand_value(player_hand) > 21:
                            check_winner()
                    elif stop_button_rect.collidepoint(event.pos):
                        player_turn = False
                        while calculate_hand_value(dealer_hand) < 17:
                            dealer_hand.append(deck.pop())
                        check_winner()
                    elif shuffle_button_rect.collidepoint(event.pos):  # Handle shuffle button click
                        shuffle_deck()
                elif game_over:
                    if replay_button_rect.collidepoint(event.pos):
                        reset_game()
                        draw_shuffles = False  # Reset the flag when the game is reset
                    elif draw_shuffles_button_rect.collidepoint(event.pos):  # Handle draw previous shuffles button click
                        draw_shuffles = True  # Set the flag to draw previous shuffles

        screen.fill(GREEN)
        draw_hand(player_hand, 50, 400)
        draw_hand(dealer_hand, 50, 50, hide_first_card=player_turn)

        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)

        player_text = font.render(f'Player score: {player_value}', True, SILVER)
        dealer_text = font.render(f'Dealer score: {dealer_value if not player_turn else "??"}', True, SILVER)

        screen.blit(player_text, (50, 350))
        screen.blit(dealer_text, (50, 5))

        draw_button("More", 450, 580, 100, 50)
        draw_button("Stop", 600, 580, 100, 50)
        draw_button("Shuffle", 300, 580, 100, 50)
        if game_over:
            draw_button("Replay", 750, 580, 100, 50)
            draw_button("Draw Shuffles", 40, 580, 200, 50)
            winner_text_render = font.render(winner_text, True, BLACK)
            screen.blit(winner_text_render, (50, HEIGHT // 2 - 130))
            if draw_shuffles:  # Draw previous shuffles only if the flag is set
                draw_previous_shuffles()

        if shuffle_message:
            shuffle_message_render = font.render(shuffle_message, True, SILVER)
            screen.blit(shuffle_message_render, (50, HEIGHT // 2 - 60))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()