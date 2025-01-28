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
        card_images[f'{rank}{suit}'] = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        card_images[f'{rank}{suit}'].fill(WHITE)
        pygame.draw.rect(card_images[f'{rank}{suit}'], BLACK, card_images[f'{rank}{suit}'].get_rect(), 2)

        # Render rank at top-left
        text_top_left = font.render(rank, True, BLACK)
        card_images[f'{rank}{suit}'].blit(text_top_left, (10, 10))

        # Render rank at bottom-right
        text_bottom_right = font.render(rank, True, BLACK)
        card_images[f'{rank}{suit}'].blit(text_bottom_right, (CARD_WIDTH - text_bottom_right.get_width() - 10, CARD_HEIGHT - text_bottom_right.get_height() - 10))

        # Render suit at center
        text_center = font.render(suit, True, BLACK)
        card_images[f'{rank}{suit}'].blit(text_center, ((CARD_WIDTH - text_center.get_width()) // 2, (CARD_HEIGHT - text_center.get_height()) // 2))

# Deck of cards
deck = [f'{rank}{suit}' for suit in SUITS for rank in RANKS]
random.shuffle(deck)

# Deal initial cards
player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop()]

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card[:-1]
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

def draw_hand(hand, x, y):
    for i, card in enumerate(hand):
        screen.blit(card_images[card], (x + i * (CARD_WIDTH + 10), y))

def draw_button(text, x, y, width, height):
    pygame.draw.rect(screen, BLACK, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x + 2, y + 2, width - 4, height - 4))
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))

def main():
    global player_hand, dealer_hand, deck
    running = True
    player_turn = True
    game_over = False
    winner_text = ""
    more_button_rect = pygame.Rect(350, 500, 100, 50)  # More button position and size
    stop_button_rect = pygame.Rect(500, 500, 100, 50)  # Stop button position and size
    replay_button_rect = pygame.Rect(650, 500, 100, 50)  # Replay button position and size

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn:
                    if more_button_rect.collidepoint(event.pos):
                        player_hand.append(deck.pop())
                    elif stop_button_rect.collidepoint(event.pos):
                        player_turn = False
                        dealer_hand.append(deck.pop())  # Add the second dealer card
                elif game_over and replay_button_rect.collidepoint(event.pos):
                    # Reset the game
                    deck = [f'{rank}{suit}' for suit in SUITS for rank in RANKS]
                    random.shuffle(deck)
                    player_hand = [deck.pop(), deck.pop()]
                    dealer_hand = [deck.pop()]
                    player_turn = True
                    game_over = False
                    winner_text = ""

        if not player_turn and not game_over:
            player_value = calculate_hand_value(player_hand)
            dealer_value = calculate_hand_value(dealer_hand)
            if dealer_value > player_value:
                game_over = True
                winner_text = "Dealer wins!"
            else:
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                    screen.fill(GREEN)
                    draw_hand(player_hand, 50, 400)
                    draw_hand(dealer_hand, 50, 50)
                    player_value = calculate_hand_value(player_hand)
                    dealer_value = calculate_hand_value(dealer_hand)
                    player_text = font.render(f'Player: {player_value}', True, BLACK)
                    dealer_text = font.render(f'Dealer: {dealer_value}', True, BLACK)
                    screen.blit(player_text, (50, 350))
                    screen.blit(dealer_text, (50, 10))
                    pygame.display.flip()
                    pygame.time.wait(1000)  # Delay for 1 second
                game_over = True

                # Determine the winner
                player_value = calculate_hand_value(player_hand)
                dealer_value = calculate_hand_value(dealer_hand)
                if player_value > 21 or dealer_value > player_value:
                    winner_text = "Dealer wins!"
                elif dealer_value > 21 or player_value > dealer_value:
                    winner_text = "Player wins!"
                else:
                    winner_text = "It's a tie!"

        screen.fill(GREEN)
        draw_hand(player_hand, 50, 400)
        draw_hand(dealer_hand, 50, 50)

        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)

        player_text = font.render(f'Player: {player_value}', True, BLACK)
        dealer_text = font.render(f'Dealer: {dealer_value}', True, BLACK)

        screen.blit(player_text, (50, 350))
        screen.blit(dealer_text, (50, 10))

        draw_button("More", 350, 500, 100, 50)  # Draw the More button
        draw_button("Stop", 500, 500, 100, 50)  # Draw the Stop button
        if game_over:
            draw_button("Replay", 650, 500, 100, 50)  # Draw the Replay button
            winner_text_render = font.render(winner_text, True, BLACK)
            screen.blit(winner_text_render, (WIDTH // 2 - winner_text_render.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()