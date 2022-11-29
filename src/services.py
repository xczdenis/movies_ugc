from dataclasses import dataclass

from db.base import BaseDBClient


@dataclass
class DBService:
    clients: list[BaseDBClient]

    def init_db(self):
        for client in self.clients:
            client.init_db()
