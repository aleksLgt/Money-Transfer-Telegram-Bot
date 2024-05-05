from enum import Enum


class GameStatus(Enum):
    CREATED = 1
    PAUSED = 2
    STOPPED = 3


list(GameStatus)
