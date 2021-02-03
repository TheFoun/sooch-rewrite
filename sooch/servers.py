"""
Contain models for server-specific information such as its name and
server boosts.
"""
from dataclasses import dataclass


class Servers:
    """Wrap around a SQL database and return servers."""

    def __init__(self, database):
        self.database = database

    async def get_server(self, discord_id: int) -> "Server":
        """Return the server info associated with the ID requested"""
        cursor = self.database.connection.cursor()
        cursor.execute(
            ("SELECT `name`, `command_prefix` FROM `server` "
             "WHERE `discord_id` = ?"),
            (discord_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return Server(
            discord_id,
            row[0],
            row[1]
        )

    async def add_server(self, server: "Server"):
        """Add the provided server into the database"""
        cursor = self.database.connection.cursor()
        cursor.execute(
            ("INSERT INTO `server`"
             "(`discord_id`, `name`, `command_prefix`)"
             "VALUES(?, ?, ?)"),
            (server.discord_id, server.name, server.command_prefix)
        )
        self.database.connection.commit()


@dataclass
class Server:
    """Represent an instance of a guild in Discord."""
    discord_id: int
    name: str
    command_prefix: str = "s!"
