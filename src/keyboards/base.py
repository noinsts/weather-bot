from abc import ABC, abstractmethod


class BaseKeyboard(ABC):
    @abstractmethod
    def get_keyboard(self):
        pass
