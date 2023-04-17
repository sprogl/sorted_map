from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool: ...


Comparable = TypeVar('CT', bound=Comparable)
