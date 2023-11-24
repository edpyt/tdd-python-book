from typing import Optional

from pydantic import BaseModel


class ItemInterface:
    def save(self) -> None:
        sql = '''INSERT INTO item(text)
        VALUES(?)'''
        cur = self.session.cursor()
        cur.execute(sql, (self.text,))
        self.session.commit()
        return cur.lastrowid

    @classmethod
    def all(cls) -> list['Item']:
        sql = '''SELECT * FROM item'''
        cur = cls.session.cursor()
        cur.execute(sql)
        return [Item(id=row[0], text=row[1]) for row in cur.fetchall()]


class Item(BaseModel, ItemInterface):
    id: Optional[int] = None
    text: str = ''
