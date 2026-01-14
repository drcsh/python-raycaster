import pygame
import pygame_gui


class VictoryScreen:
    """
    Victory screen displayed when a level is completed.
    Shows level statistics and waits for player input to continue.
    """

    def __init__(self, gui_manager: pygame_gui.UIManager, level_name: str, stats: dict):
        """
        Initialize victory screen with level stats

        Args:
            gui_manager: pygame_gui UIManager instance
            level_name: Name of the completed level
            stats: Dictionary with completion stats (enemies_defeated, total_enemies, time_elapsed)
        """
        self.gui_manager = gui_manager
        self.level_name = level_name
        self.stats = stats
        self.ui_elements = []

        # Create UI elements
        self._create_ui_elements()

    def _create_ui_elements(self):
        """Create all UI elements for the victory screen"""
        # Title
        title_rect = pygame.Rect(0, 0, 400, 50)
        title_rect.center = (512, 150)
        title = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="LEVEL COMPLETE!",
            manager=self.gui_manager
        )
        self.ui_elements.append(title)

        # Level name
        level_name_rect = pygame.Rect(0, 0, 400, 40)
        level_name_rect.center = (512, 210)
        level_label = pygame_gui.elements.UILabel(
            relative_rect=level_name_rect,
            text=self.level_name,
            manager=self.gui_manager
        )
        self.ui_elements.append(level_label)

        # Stats
        enemies_defeated = self.stats.get('enemies_defeated', 0)
        total_enemies = self.stats.get('total_enemies', 0)
        time_elapsed = self.stats.get('time_elapsed', 0)

        stats_text = f"Enemies Defeated: {enemies_defeated}/{total_enemies}\n"
        stats_text += f"Time: {time_elapsed:.1f} seconds"

        stats_rect = pygame.Rect(0, 0, 400, 80)
        stats_rect.center = (512, 290)
        stats_label = pygame_gui.elements.UITextBox(
            html_text=stats_text,
            relative_rect=stats_rect,
            manager=self.gui_manager
        )
        self.ui_elements.append(stats_label)

        # Continue prompt
        continue_rect = pygame.Rect(0, 0, 400, 40)
        continue_rect.center = (512, 380)
        continue_label = pygame_gui.elements.UILabel(
            relative_rect=continue_rect,
            text="Press SPACE to continue",
            manager=self.gui_manager
        )
        self.ui_elements.append(continue_label)

    def show(self, display_surface: pygame.Surface, background_surface: pygame.Surface, clock: pygame.time.Clock):
        """
        Display the victory screen and wait for player input

        Args:
            display_surface: Main display surface
            background_surface: Background surface
            clock: Pygame clock for frame timing

        Returns:
            bool: True when player wants to continue
        """
        waiting = True
        time_delta = 0

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

                self.gui_manager.process_events(event)

            # Update and draw UI
            self.gui_manager.update(time_delta)

            display_surface.blit(background_surface, (0, 0))
            self.gui_manager.draw_ui(display_surface)

            pygame.display.flip()

            time_delta = clock.tick(60) / 1000.0

        # Clean up UI elements
        self._cleanup()
        return True

    def _cleanup(self):
        """Remove all UI elements"""
        for element in self.ui_elements:
            element.kill()
        self.ui_elements.clear()
