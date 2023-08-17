import sys
sys.dont_write_bytecode = True

import sqlite3

class DatabaseUtils:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def add_warn(self, user_id, warn_grund):
        max_warn_id = self.cursor.execute("select max(warn_id) from warns where user_id = ?", (user_id,)).fetchone()

        if max_warn_id[0] is None:
            new_count = 1
        else:
            new_count = max_warn_id[0] + 1

        self.cursor.execute("INSERT INTO warns (user_id, warn_grund, warn_id) VALUES (?, ?, ?)", (user_id, warn_grund, new_count,))
        self.conn.commit()
        return True
    
    def get_warn(self, user_id):
        warns = self.cursor.execute("SELECT warn_grund FROM warns WHERE user_id = ?", (user_id,)).fetchall()

        if not warns or warns[0][0] is None:
            return False
        else:
            return warns
    
    def del_warn(self, user_id, position):
        try:
            position = int(position)
        except ValueError:
            return False
        
        if position <= 0:
            return False
        
        warns = self.cursor.execute("SELECT warn_id, warn_grund FROM warns WHERE user_id = ?", (user_id,)).fetchall()
        
        if not warns:
            return False
        
        if position > len(warns):
            return False
        
        warn_id_to_delete = warns[position - 1][0]
        
        self.cursor.execute("DELETE FROM warns WHERE warn_id = ?", (warn_id_to_delete,))
        self.conn.commit()

        remaining_warns = warns[:position - 1] + warns[position:]
        for idx, (warn_id, _) in enumerate(remaining_warns, start=1):
            self.cursor.execute("UPDATE warns SET warn_id = ? WHERE warn_id = ?", (idx, warn_id))
            self.conn.commit()
        return True 


    def close(self):
        self.conn.close()