"""This module allows communication between objects without the Program."""

from copy import deepcopy


class ObjectSignal:
    """Signal to allow communication between objects."""

    return_value = None

    def emit(self) -> any:
        """Returns whatever is connected to it (If nothing, than None)."""
        return deepcopy(self.return_value)
