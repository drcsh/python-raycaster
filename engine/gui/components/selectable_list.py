from typing import Any, Callable, Optional

import pygame
import pygame_gui


class SelectableList:
    """
    Reusable scrollable list component for displaying selectable items.

    Used for campaign selection and save game lists.
    """

    def __init__(self,
                 gui_manager: pygame_gui.UIManager,
                 items: list[tuple[str, Any]],
                 rect: pygame.Rect,
                 on_select: Optional[Callable[[Any], None]] = None):
        """
        Create a selectable list.

        Args:
            gui_manager: pygame_gui UIManager instance
            items: List of (display_text, value) tuples
            rect: Rectangle defining list position and size
            on_select: Optional callback when item is selected
        """
        self.gui_manager = gui_manager
        self.items = items
        self.on_select = on_select
        self.selected_value = None
        self.ui_elements = []

        # Create UISelectionList from pygame_gui
        item_list = [item[0] for item in items]

        self.selection_list = pygame_gui.elements.UISelectionList(
            relative_rect=rect,
            item_list=item_list,
            manager=gui_manager,
            allow_multi_select=False
        )
        self.ui_elements.append(self.selection_list)

    def handle_event(self, event: pygame.event.Event) -> Optional[Any]:
        """
        Handle selection events.

        Returns:
            Selected value if an item was selected, None otherwise
        """
        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.selection_list:
                selected_text = event.text
                # Find the corresponding value
                for display_text, value in self.items:
                    if display_text == selected_text:
                        self.selected_value = value
                        if self.on_select:
                            self.on_select(value)
                        return value
        return None

    def get_selected_value(self) -> Optional[Any]:
        """Return the currently selected value"""
        return self.selected_value

    def kill(self):
        """Remove all UI elements"""
        for element in self.ui_elements:
            element.kill()
        self.ui_elements.clear()
