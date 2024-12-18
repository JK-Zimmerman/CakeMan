'''
authenticate.py
An object that maintains a database of dates with sqlite3 and can provide details about it, relative to a provided date
Last updated: 2024 12 16
'''
import sqlite3

class Authenticator:
    def __init__ (self, storagefile = "authenticate.db"):
        self.conec = sqlite3.connect(storagefile)
        self.cursor = self.conec.cursor()

        if not self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='record'").fetchone():
            self.create_record()

    def create_record(self) -> None: #creates table
        self.cursor.execute("CREATE TABLE record(year, month, day)")
        self.conec.commit()
    
    def complete_reset(self) -> str: #wipes records, returns description of result as a string 
        self.cursor.execute("DROP TABLE record")
        self.create_record()
        return f'All dates reset.'

    def addDate(self, year:int, month:int, day:int) -> None: #adds provided date
        self.cursor.execute("INSERT INTO record VALUES (?, ?, ?)", (year, month, day))
        self.conec.commit()
        return f"{year} {month} {day} added to records."

    def deleteDate(self, year:int, month:int, day:int) -> str: #deletes provided date from records
        val = self.cursor.execute("SELECT * FROM record WHERE year = ? AND month = ? AND day = ?", (year, month, day)).fetchone()
        if val is not None: #if query exists
            self.cursor.execute("DELETE FROM record WHERE year = ? AND month = ? AND day = ?", (year, month, day))
            self.conec.commit()
            return f"{year} {month} {day} has been deleted from records."
        return "Date not found in records."
    
    def authenticateToday(self, year:int, month:int, day:int) -> bool: # returns True if there is no record of today
        val = self.cursor.execute("SELECT * FROM record WHERE year = ? AND month = ? AND day = ?", (year, month, day)).fetchone()
        return not bool(val) 

    def authenticateAllTime(self, month:int, day:int) -> bool: # returns True if there is a record of this day, regardless of year
        val = self.cursor.execute("SELECT * FROM record WHERE month = ? AND day = ?", (month, day)).fetchone()
        return bool(val) 
    
    def record_quick_save(self) -> str: # returns description of result as string
        self.conec.commit()
        return 'Committed.'
    
    def __str__(self): # lists all dates, formatted like YYYY MM DD \n
        res = self.cursor.execute("SELECT * FROM record").fetchall()
        rn = ''
        for row in res:
            rn += f'{row[0]} {row[1]:02} {row[2]:02}\n'
        if res:
            return rn
        return 'Record is empty.'
