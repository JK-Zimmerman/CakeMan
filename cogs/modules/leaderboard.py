'''
leaderboard.py
An object that maintains a leaderboard with sqlite3
Last updated: 2024 12 17
'''
import sqlite3

class Leaderboard_Manager:
    #object to manage the leaderboard
    def __init__(self, word:str = 'point', plural:str = 's', storagefile:str = "leaderboard.db") -> None: 
        self.word = word
        self.plural = plural
        self.con = sqlite3.connect(storagefile)
        self.cur = self.con.cursor()

        if not self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leaderboard'").fetchone():
            self.create_leaderboard()
    
    def create_leaderboard(self) -> None: #makes table
        self.cur.execute("CREATE TABLE leaderboard(username, score)")
        self.con.commit()

    def update(self, username:str) -> str: #to update leaderboard, returns description of result as string
        val = self.cur.execute("SELECT score FROM leaderboard WHERE username = ?", (username,)).fetchone() #check database for provided username
        if val is None: #if query turns up nothing
            self.cur.execute("INSERT INTO leaderboard VALUES (?, 1)", (username,)) #add user, with their score
            self.con.commit()
            return f'{username} added to database.'
        val = val[0] #add one to score is user exists
        self.cur.execute("UPDATE leaderboard SET score = ? WHERE username = ?", (val+1, username))
        self.con.commit()
        return f"{username}'s score updated. They now have {val+1} {self.get_count_word(val+1)}."
        
    
    def override(self, username, n:int = 1) -> str: #cahnges username's score to n, returns description of result as string
        if n < 0: #don't do anything if n is invalid
            return f"It is impossible to have less than zero {self.get_count_word(2)}."
        
        val = self.cur.execute("SELECT score FROM leaderboard WHERE username = ?", (username,)).fetchone() #check database for provided username
        if val is None: #add user if it isn't already there
            self.cur.execute("INSERT INTO leaderboard VALUES (?, ?)", (username, n))
            self.con.commit()
            return f"{username} has been added to the leaderboard with {n} {self.get_count_word(n)}"
        
        if n == 0: #setting score to 0 deletes user
            self.cur.execute("DELETE FROM leaderboard WHERE username = ?", (username,))
            self.con.commit()
            return f"{username} has been removed from the leaderboard"
        
        #if valid and doesn't need special case, simply update score to n
        self.cur.execute("UPDATE leaderboard SET score = ? WHERE username = ?", (n, username))
        self.con.commit()
        return f"{username}'s score has been updated to {n} {self.get_count_word(n)}."
    
    def total_reset(self) -> str: #leaderboard is wiped, returns description of result as string
        self.cur.execute("DROP TABLE leaderboard")
        self.create_leaderboard()
        return 'Leaderboard is wiped.'

    def get_count_word(self, n:int) -> str: #returns keyword for string formatting purposes (adds plural suffix if n > 1)
        if n < 1:
            raise ValueError('CountKeyword Dept: Something fucked up the backend really bad.')
        elif n == 1:
            return self.word
        else:
            return self.word + self.plural
        
    def ldr_quick_save(self) -> str: #returns description of result as string
        self.con.commit()
        return 'Committed.'

    def get_leaderboard(self) -> list: #returns list of leaderboard, [(USERNAME, SCORE)]
        return self.cur.execute("SELECT * FROM leaderboard ORDER BY score DESC").fetchall()

    def __str__(self) -> str: # gives entire leaderboard as string, formatted like #PLACE - USERNAME (SCORE keyword(s) \n)
        res = self.cur.execute("SELECT * FROM leaderboard ORDER BY score DESC").fetchall()
        place = 1
        cutoff = 0
        ldr = ''

        for row in res:
            username = row[0]
            score = row[1]
            if score < cutoff: # if score is tied, they are tied, so place can't move
                place += 1
            ldr += f"#{place} - {username} ({score} {self.get_count_word(score)})\n"
            cutoff = score # new score to be compared for next entry

        if ldr: # return string if anything exists in leaderboard, or send empty message
            return ldr
        else:
            return "Leaderboard is empty."
