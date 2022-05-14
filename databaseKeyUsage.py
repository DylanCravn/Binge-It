import sqlite3
class keyUsage():
    def __init__(self):
        self.connection = sqlite3.connect("scripts/dataShow.db")
        self.cur = self.connection.cursor()

    def keyToUse(self):
        self.cur.execute("select * from apiKeyUsage where uses < 20 limit 1")
        response = self.cur.fetchone
        self.count = response[0]    
        self.key = response[1]

    def updateKey(self):
        count += 1
        self.cur.execute()
