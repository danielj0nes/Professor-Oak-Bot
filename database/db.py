import sqlite3


class SQL:
    def __init__(self):
        self.conn = sqlite3.connect("professor_oak_database.db")
        self.cur = self.conn.cursor()

    def get_prefix(self, bot, message):
        self.cur.execute("SELECT command_prefix FROM guilds WHERE (gid) = (?)", [str(message.guild.id)])
        return self.cur.fetchone()

    def add_prefix(self, guild, prefix):
        cur = self.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO guilds (gid, command_prefix) VALUES (?, ?)", [str(guild), prefix])  # Default prefix
        self.conn.commit()

    def update_prefix(self, guild, prefix):
        cur = self.conn.cursor()
        cur.execute("UPDATE guilds SET (command_prefix) = (?) WHERE (gid) = (?)", [prefix, str(guild)])
        self.conn.commit()