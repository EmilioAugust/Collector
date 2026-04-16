from enum import Enum

class Status(str, Enum):
    watched = "Watched"
    watching = "Watching"
    planning = "Planning"

class StatusBook(str, Enum):
    read = "Read"
    reading = "Reading"
    planning = "Planning"

class Separators:
    first_sep = "----------"
    second_sep = "(source)"