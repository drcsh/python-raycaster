from dataclasses import dataclass


@dataclass
class Config:
    """Data class holding configuration values"""
    dev_mode: bool
    resolution_width: int
    resolution_height: int
    field_of_view: int