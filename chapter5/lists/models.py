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
        sql = '''SELECT * FROM item ORDER BY id'''
        cur = cls.session.cursor()
        cur.execute(sql)
        return [Item(id=row[0], text=row[1]) for row in cur.fetchall()]

    @classmethod
    def first(cls) -> 'Item':
        sql = '''SELECT * FROM item ORDER BY id LIMIT 1'''
        cur = cls.session.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        return cls(id=res[0], text=res[1])


class Item(BaseModel, ItemInterface):
    id: Optional[int] = None
    text: str = ''
