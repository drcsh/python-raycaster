import os
from typing import Any, Optional

import pygame
import pygame_gui

from engine.gui.screens.base_screen import BaseScreen
from engine.gui.screens.main_menu.menu_action import MainMenuAction
from engine.gui.components.menu_button import MenuButton
from engine.gui.components.selectable_list import SelectableList
from engine.asset_loaders.campaign_loader import CampaignLoader


class CampaignSelectScreen(BaseScreen):
    """
    Screen for selecting a campaign to play.

    Lists available campaigns and allows selection.
    Returns the selected campaign path or RETURN_TO_MAIN action.
    """

    CAMPAIGNS_DIRECTORY = "assets/campaigns"

    def __init__(self, gui_manager: pygame_gui.UIManager,
                 screen_width: int, screen_height: int):
        """
        Initialize campaign select screen.

        Args:
            gui_manager: pygame_gui UIManager instance
            screen_width: Screen width for centering
            screen_height: Screen height for positioning
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.campaign_list: Optional[SelectableList] = None
        self.start_button: Optional[MenuButton] = None
        self.back_button: Optional[MenuButton] = None
        self.selected_campaign_path: Optional[str] = None
        super().__init__(gui_manager)

    def _create_ui_elements(self):
        """Create campaign selection UI elements"""
        center_x = self.screen_width // 2

        # Title
        title_rect = pygame.Rect(0, 0, 400, 50)
        title_rect.center = (center_x, 100)
        title = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="SELECT CAMPAIGN",
            manager=self.gui_manager
        )
        self.ui_elements.append(title)

        # Load available campaigns
        campaign_items = self._load_campaign_items()

        # Campaign list
        list_rect = pygame.Rect(0, 0, 400, 300)
        list_rect.center = (center_x, 300)
        self.campaign_list = SelectableList(
            self.gui_manager,
            campaign_items,
            list_rect,
            on_select=self._on_campaign_select
        )
        self.ui_elements.extend(self.campaign_list.ui_elements)

        # Start Game button (initially disabled until selection)
        self.start_button = MenuButton(
            self.gui_manager, "Start Campaign", center_x, 500
        )
        self.start_button.button.disable()
        self.ui_elements.append(self.start_button.button)

        # Return to Main Menu button
        self.back_button = MenuButton(
            self.gui_manager, "Return to Main Menu", center_x, 570
        )
        self.ui_elements.append(self.back_button.button)

    def _load_campaign_items(self) -> list[tuple[str, str]]:
        """
        Load available campaigns and format for SelectableList.

        Returns:
            List of (display_name, campaign_path) tuples
        """
        items = []

        if not os.path.exists(self.CAMPAIGNS_DIRECTORY):
            return items

        for entry in os.listdir(self.CAMPAIGNS_DIRECTORY):
            campaign_dir = os.path.join(self.CAMPAIGNS_DIRECTORY, entry)
            campaign_file = os.path.join(campaign_dir, "campaign.json")

            if os.path.isdir(campaign_dir) and os.path.exists(campaign_file):
                try:
                    # Load campaign to get name
                    campaign = CampaignLoader.load_campaign(campaign_file)
                    display_name = campaign.name
                    if hasattr(campaign, 'difficulty') and campaign.difficulty:
                        display_name = f"{campaign.name} ({campaign.difficulty})"
                    items.append((display_name, campaign_file))
                except Exception:
                    # Skip invalid campaigns
                    pass

        return items

    def _on_campaign_select(self, campaign_path: str):
        """Handle campaign selection"""
        self.selected_campaign_path = campaign_path
        self.start_button.button.enable()

    def _handle_event(self, event: pygame.event.Event) -> tuple[bool, Any]:
        """Handle events for campaign selection"""
        # Check for campaign list selection
        self.campaign_list.handle_event(event)

        # Check button clicks
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.start_button.is_clicked(event) and self.selected_campaign_path:
                return (True, self.selected_campaign_path)

            if self.back_button.is_clicked(event):
                return (True, MainMenuAction.SHOW_MAIN_MENU)

        return (False, None)

    def _cleanup(self):
        """Clean up all UI elements"""
        if self.campaign_list:
            self.campaign_list.kill()
        if self.start_button:
            self.start_button.kill()
        if self.back_button:
            self.back_button.kill()
        super()._cleanup()
