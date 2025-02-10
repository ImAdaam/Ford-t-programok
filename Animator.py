import pygame
import sys

class DriveAnimator:
    def __init__(self, playbook):
        self._field_length = 100
        self._field_width = 50
        self._playbook = playbook
        self._play_count = 0

    def start(self):
        self._play_count += 1
        if self._playbook.getTotalPlayCount() >= self._play_count:
            self.animate(self._playbook.getPlay(self._play_count-1))

    def animate(self, play):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions in pixels
        ENDZONE_WIDTH = 100  # 10 yards
        WIDTH, HEIGHT = 1300, 533  # 120 yards, 53.3 yards
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Set title
        pygame.display.set_caption(f"Football Play Visualization: {play[3]}")

        # Colors
        GREEN = (34, 139, 34)
        DARK_GREEN = (10, 54, 10)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 255)
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)

        # Field and player dimensions in pixels
        FIELD_MARGIN = 50
        QB_START = (150+(play[4]*10), HEIGHT // 2)  # 100 pixels + 50 margin( = 150 pixel = 10 yards) + the start of the snap
        if play[0] == 'pass':
            WR_START = ((150+(play[4]*10)+(play[2]*10)), HEIGHT // play[6])  # +500 pixels = +50 yards
            BALL_START = QB_START
        else:
            RB_START = (150+(play[4]*10)-30, HEIGHT // 2)  # +500 pixels = +50 yards
            WR_START = ((150 + (play[4] * 10) + (play[2] * 10)), HEIGHT // 2)  # +500 pixels = +50 yards
            BALL_START = RB_START

        # Clock
        clock = pygame.time.Clock()
        fps = 60

        # Ball movement interpolation
        def interpolate(start, end, progress):
            return start[0] + progress * (end[0] - start[0]), start[1] + progress * (end[1] - start[1])

        progress = 0  # Ball animation progress (0 to 1)

        # Main loop
        running = True
        while running:
            # Fill background
            screen.fill(GREEN)

            # Draw end zones
            pygame.draw.rect(screen, DARK_GREEN, (FIELD_MARGIN, FIELD_MARGIN, ENDZONE_WIDTH, HEIGHT - 2 * FIELD_MARGIN))
            pygame.draw.rect(screen, DARK_GREEN, (
            WIDTH - FIELD_MARGIN - ENDZONE_WIDTH, FIELD_MARGIN, ENDZONE_WIDTH, HEIGHT - 2 * FIELD_MARGIN))

            # Draw field boundaries
            pygame.draw.rect(screen, WHITE,
                             (FIELD_MARGIN, FIELD_MARGIN, WIDTH - 2 * FIELD_MARGIN, HEIGHT - 2 * FIELD_MARGIN), 5)

            # Draw vertical yard lines
            for i in range(0, 11, 1):
                x = (ENDZONE_WIDTH + i * 100) + 50
                pygame.draw.line(screen, WHITE, (x, FIELD_MARGIN), (x, HEIGHT - FIELD_MARGIN), 1)

            # Draw hashmarks
            HASHMARK_LENGTH = 10
            for i in range(6, 105):  # Every yard except boundaries
                x = (ENDZONE_WIDTH + i * 10)
                y_top = HEIGHT // 3  # Top hashmarks
                y_bottom = 2 * HEIGHT // 3  # Bottom hashmarks

                pygame.draw.line(screen, WHITE, (x, y_top - HASHMARK_LENGTH // 2), (x, y_top + HASHMARK_LENGTH // 2), 1)
                pygame.draw.line(screen, WHITE, (x, y_bottom - HASHMARK_LENGTH // 2),
                                 (x, y_bottom + HASHMARK_LENGTH // 2), 1)

            # Draw players
            pygame.draw.circle(screen, BLUE, QB_START, 15)  # Quarterback
            if play[0] == 'pass':
                pygame.draw.circle(screen, RED, WR_START, 15)  # Receiver

            # Draw ball
            if play[0] == 'pass':
                if progress < 1:
                    BALL_POS = interpolate(BALL_START, WR_START, progress)
                    progress += 0.01  # Increment progress
                pygame.draw.circle(screen, YELLOW, (int(BALL_POS[0]), int(BALL_POS[1])), 10)
            else:
                if progress < 1:
                    BALL_POS = interpolate(BALL_START, WR_START, progress)
                    RB_POS = interpolate(BALL_START, WR_START, progress)
                    progress += 0.01  # Increment progress
                pygame.draw.circle(screen, RED, (int(RB_POS[0]), int(RB_POS[1])), 15)  # Running back
                if int(RB_POS[0]) >= int(QB_START[0]):
                    pygame.draw.circle(screen, YELLOW, (int(BALL_POS[0]), int(BALL_POS[1])), 10)
                else:
                    pygame.draw.circle(screen, YELLOW, QB_START, 10)

            # Update display
            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Limit frame rate
            clock.tick(fps)

        self.start()
        pygame.quit()
        if self._playbook.getTotalPlayCount() < self._play_count:
            sys.exit()