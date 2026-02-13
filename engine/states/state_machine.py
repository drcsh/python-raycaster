from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, Type
import pygame
from dataclasses import dataclass
from engine.game_manager import GameManager

@dataclass
class StateTransition:
    target_state_id: str
    kwargs: Dict[str, Any] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}

class State(ABC):
    """
    Abstract base class for game states.
    States are now decoupled from the StateMachine and only reference constants.
    """
    def __init__(self, game_manager: Any):
        self.game_manager = game_manager

    def enter(self):
        """Called when the state is entered."""
        pass

    def exit(self):
        """Called when the state is exited."""
        pass

    @abstractmethod
    def update(self, dt: float) -> Optional[StateTransition]:
        """
        Update the state.
        :param dt: Time delta in seconds
        :return: Optional StateTransition
        """
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        """
        Render the state.
        :param surface: The surface to render to
        """
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[StateTransition]:
        """
        Handle a single event.
        :param event: The pygame event
        :return: Optional StateTransition
        """
        pass


class StateMachine:
    """
    Manages the current game state and transitions.
    """
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager
        self.current_state: Optional[State] = None
        self.state_registry: Dict[str, Type[State]] = {}

    def register_state(self, state_id: str, state_class: Type[State]):
        """Register a state class with an ID."""
        self.state_registry[state_id] = state_class

    def change_state(self, state_id: str, **kwargs):
        """
        Switch to a new state by ID.
        instantiates the new state with game_manager and kwargs.
        """
        if state_id not in self.state_registry:
            print(f"Error: State ID '{state_id}' not registered.")
            return

        if self.current_state:
            self.current_state.exit()

        state_class = self.state_registry[state_id]
        self.current_state = state_class(self.game_manager, **kwargs)
        self.current_state.enter()

    def update(self, dt: float):
        """
        Update the current state and handle transitions returned by update.
        """
        if self.current_state:
            transition = self.current_state.update(dt)
            if transition:
                self.change_state(transition.target_state_id, **transition.kwargs)

    def render(self, time_delta: float):
        """
        Render the current state.
        """
        if self.current_state:
            self.current_state.render(time_delta)

    def handle_event(self, event: pygame.event.Event):
        """
        Pass event to the current state and handle transitions returned by handle_event.
        """
        if self.current_state:
            transition = self.current_state.handle_event(event)
            if transition:
                self.change_state(transition.target_state_id, **transition.kwargs)
