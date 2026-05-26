import sqlite3
import json
from typing import List, Dict, Any, Optional, Tuple
from repositories.interface import IOrderRepository

class OrderRepository(IOrderRepository):
    def __init__(self, db_path: str = 'loja.db') -> None:
        self.db = sqlite3.connect(db_path)
        self.c = self.db.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS ped (
                          id INTEGER PRIMARY KEY, cli TEXT, itens TEXT,
                          tot REAL, st TEXT, dt TEXT, tp TEXT)''')
        self.db.commit()

    def add(self, client: str, items_str: str, total: float, status: str, date: str, client_type: str) -> int:
        self.c.execute("INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
                       (client, items_str, total, status, date, client_type))
        self.db.commit()
        return self.c.lastrowid

    def get(self, order_id: int) -> Optional[Dict[str, Any]]:
        self.c.execute("SELECT * FROM ped WHERE id=?", (order_id,))
        r = self.c.fetchone()
        if r:
            return {'id': r[0], 'cli': r[1], 'itens': json.loads(str(r[2])),
                    'tot': r[3], 'st': r[4], 'dt': r[5], 'tp': r[6]}
        return None

    def update_status(self, order_id: int, status: str) -> None:
        self.c.execute("UPDATE ped SET st=? WHERE id=?", (status, order_id))
        self.db.commit()

    def get_all_by_client(self, client: str) -> List[Tuple[Any, ...]]:
        self.c.execute("SELECT * FROM ped WHERE cli=?", (client,))
        return self.c.fetchall()

    def get_all(self) -> List[Tuple[Any, ...]]:
        self.c.execute("SELECT * FROM ped")
        return self.c.fetchall()
        
    def get_all_clients(self) -> List[Tuple[Any, ...]]:
        self.c.execute("SELECT DISTINCT cli, tp FROM ped")
        return self.c.fetchall()

    def close(self) -> None:
        self.db.close()