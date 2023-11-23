from pydantic import BaseModel


class Item(BaseModel):
    text: str


class ItemInterface:
    def save(self) -> None:
        ...

    @classmethod
    def all(self) -> list['Item']:
        return []
