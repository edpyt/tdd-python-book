from typing import Optional

from pydantic import BaseModel


class ItemInterface:
    def save(self) -> None:
        if self.id:
            self.update(self.id, text=self.text)
        else:
            item = self.create(self.text)
            self.id = item.id

    @classmethod
    def all(cls) -> list['Item']:
        sql = '''SELECT * FROM item ORDER BY id'''
        cur = cls.session.cursor()
        cur.execute(sql)
        return [cls._get_item_obj(row) for row in cur.fetchall()]

    @classmethod
    def get(cls, id_, **kwargs) -> 'Item':
        sql = 'SELECT * FROM item WHERE id=?'
        cur = cls.session.cursor()
        cur.execute(sql, (id_, ))
        return cls._get_item_obj(cur.fetchone())

    @classmethod
    def update(cls, id_: int, **kwargs) -> 'Item':
        update_keys = cls._get_update_keys(kwargs)
        sql = f'''UPDATE item SET {update_keys} WHERE id = ?'''
        cur = cls.session.cursor()
        cur.execute(sql, kwargs.values())
        return cls._get_item_obj(cur.lastrowid)

    @classmethod
    def first(cls) -> 'Item':
        sql = '''SELECT * FROM item ORDER BY id LIMIT 1'''
        cur = cls.session.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        return cls._get_item_obj(res)

    @classmethod
    def create(cls, *args) -> 'Item':
        sql = '''INSERT INTO item(text)
        VALUES(?)'''
        cur = cls.session.cursor()
        cur.execute(sql, args)
        cls.session.commit()
        return cls._get_item_obj(cur.lastrowid)

    @staticmethod
    def _get_update_keys(data) -> str:
        update_keys = ', '.join(map('{update_key} = ?'.format, data.keys()))
        return update_keys

    @classmethod
    def _get_item_obj(cls, cur_lastrowid) -> 'Item':
        if not isinstance(cur_lastrowid, tuple):
            return cls.get(cur_lastrowid)
        return Item(id=cur_lastrowid[0], text=cur_lastrowid[1])


class Item(BaseModel, ItemInterface):
    id: Optional[int] = None
    text: str = ''
