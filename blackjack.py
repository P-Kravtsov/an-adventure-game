import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
CARD_WIDTH, CARD_HEIGHT = 80, 120

# Card suits and ranks
SUITS = ['♥', '♦', '♠', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont('Arial', 36)
clock = pygame.time.Clock()

# Load card images
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
        rank = card[:-1] # - Extracts the rank (everything except the last character (suit) - `8H` becomes `H`, `AS` becomes `S`)
        if rank in 'JQK':
            value += 10
        elif rank == 'A':
            aces += 1
            value += 11
        else:
            value += int(rank)

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
    global player_hand, dealer_hand, deck, player_turn, game_over, winner_text
    deck = [f'{rank}{suit}' for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    player_turn = True
    game_over = False
    winner_text = ""


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


def main():
    global player_turn, game_over, winner_text
    running = True
    player_turn = True
    game_over = False
    winner_text = ""
    more_button_rect = pygame.Rect(350, 500, 100, 50)
    stop_button_rect = pygame.Rect(500, 500, 100, 50)
    replay_button_rect = pygame.Rect(650, 500, 100, 50)

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
                elif game_over and replay_button_rect.collidepoint(event.pos):
                    reset_game()

        screen.fill(GREEN)
        draw_hand(player_hand, 50, 400)
        draw_hand(dealer_hand, 50, 50, hide_first_card=player_turn)

        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)

        player_text = font.render(f'Player: {player_value}', True, BLACK)
        dealer_text = font.render(f'Dealer: {dealer_value if not player_turn else "??"}', True, BLACK)

        screen.blit(player_text, (50, 350))
        screen.blit(dealer_text, (50, 10))

        draw_button("More", 350, 500, 100, 50)
        draw_button("Stop", 500, 500, 100, 50)
        if game_over:
            draw_button("Replay", 650, 500, 100, 50)
            winner_text_render = font.render(winner_text, True, BLACK)
            screen.blit(winner_text_render, (WIDTH // 2 - winner_text_render.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
