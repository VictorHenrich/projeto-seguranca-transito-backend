from typing import Protocol, Generic, TypeVar, TypeAlias, Tuple, Dict, Any


T = TypeVar("T", contravariant=True)
Args: TypeAlias = Tuple[Any, ...]
Kwargs: TypeAlias = Dict[str, Any]


class ICommand(Protocol, Generic[T]):
    @property
    def name(self) -> str:
        ...

    def execute(self, props: T) -> None:
        ...