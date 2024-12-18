'''
liege.py
I didn't realize that you could just control access to the controls with permissions, so I built my entire system around the existence of a 
single admin (the liege), only to realize I built no easy way to manage who that was. This class exists as a bandaid for that purpose.
Last updated: 2024 12 17

'''

import sqlite3

class Liege:
    def __init__(self, liege:int = 0, storagefile:str = "liege.db"): # 0 means no liege
        self.conn = sqlite3.connect(storagefile)
        self.curr = self.conn.cursor()
        self.make_liege_record(liege)
    
    def make_liege_record(self, liege:int=0) -> None: #remakes liege table, with provided liege(default no liege)
        self.curr.execute("DROP TABLE liege_record")
        self.curr.execute("CREATE TABLE liege_record(id)")
        self.curr.execute("INSERT INTO liege_record VALUES (?)", (liege,))
        self.conn.commit()

    def remove_liege(self) -> str: #changes liege id to 0 (no liege value) and returns string description of what it did
        self.curr.execute("UPDATE liege_record SET id = ?",(0,))
        self.conn.commit()
        return f"Liege removed."
        
    def add_liege(self, liege) -> str: #changes saved liege id to provided liege id, and returns string description of what it did
        self.curr.execute("UPDATE liege_record SET id = ?",(liege,))
        self.conn.commit()
        return f"Liege added."
    
    def get_liege(self) -> int: #returns current liege id
        return self.curr.execute("SELECT * FROM liege_record").fetchone()[0]
    
    def is_liege(self, id:int) -> bool: #returns whether provided id is liege
        return id == self.get_liege()
    
    def exists_liege(self) -> bool: #returns whether there is a liege or not (if there is a liege, returns true)
        return bool(self.curr.execute("SELECT * FROM liege_record").fetchone()[0])
