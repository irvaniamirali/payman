from abc import ABC, abstractmethod


class CallbackBase(ABC):

    @property
    @abstractmethod
    def is_success(self) -> bool:
        """
        Indicates whether the callback represents a successful payment.
        """

        pass
