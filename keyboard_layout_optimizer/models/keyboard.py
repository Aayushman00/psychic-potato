from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class KeyboardKey:
    label: str
    row: int
    x: float
    y: float
    hand: str
    finger: str
    modifier: bool = False
    hardware_group: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "row": self.row,
            "x": self.x,
            "y": self.y,
            "hand": self.hand,
            "finger": self.finger,
            "modifier": self.modifier,
            "hardware_group": self.hardware_group,
        }
