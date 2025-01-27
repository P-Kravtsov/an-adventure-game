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
dealer_hand = [deck.pop(), deck.pop()]

def draw_hand(hand, x, y):
    for i, card in enumerate(hand):
        screen.blit(card_images[card], (x + i * (CARD_WIDTH + 10), y))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GREEN)
        draw_hand(player_hand, 50, 400)
        draw_hand(dealer_hand, 50, 50)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()