from __future__ import annotations
from abc import ABC
import asyncio
from collections.abc import Awaitable, Iterable
import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import Any, override
import json
from aiohttp import web

from raphson_music_client.track import Track


class Topic(Enum):
    ACTIVITY = "activity"


@dataclass(kw_only=True)
class Command(ABC):
    name: str

    def data(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_data(cls, data: dict[str, str]) -> Command:
        assert data["name"] == cls.name
        return cls(**data)

    async def send(self, ws: web.WebSocketResponse):
        try:
            await ws.send_json(self.data())
        except ConnectionError:
            pass


@dataclass(kw_only=True)
class ServerCommand(Command, ABC):
    """Represents a command from the server"""


@dataclass(kw_only=True)
class ClientCommand(Command, ABC):
    """Represents a command from the client"""


@dataclass(kw_only=True)
class TrackCommand(ABC):
    track: dict[str, str | int | bool | list[str] | None]

    def get_track(self):
        return Track.from_dict(self.track)


@dataclass(kw_only=True)
class PlayerControlCommand(ABC):
    player_id: str


@dataclass(kw_only=True)
class ClientPlaying(ClientCommand):
    name: str = "c_playing"
    track: str
    paused: bool
    position: float


@dataclass(kw_only=True)
class ClientSubscribe(ClientCommand):
    name: str = "c_subscribe"
    topic: Topic

    @override
    @classmethod
    def from_data(cls, data: dict[str, str]) -> Command:
        return cls(topic=Topic(data["topic"]))


@dataclass(kw_only=True)
class ClientToken(ClientCommand):
    name: str = "c_token"
    csrf: str


@dataclass(kw_only=True)
class ClientPlay(ClientCommand, PlayerControlCommand):
    name: str = "c_play"


@dataclass(kw_only=True)
class ClientPause(ClientCommand, PlayerControlCommand):
    name: str = "c_pause"


@dataclass(kw_only=True)
class ClientPrevious(ClientCommand, PlayerControlCommand):
    name: str = "c_previous"


@dataclass(kw_only=True)
class ClientNext(ClientCommand, PlayerControlCommand):
    name: str = "c_next"


@dataclass(kw_only=True)
class ServerPlaying(ServerCommand, TrackCommand):
    name: str = "s_playing"
    player_id: str
    username: str
    update_time: float
    paused: bool
    position: float


@dataclass(kw_only=True)
class ServerPlayed(ServerCommand, TrackCommand):
    name: str = "s_played"
    played_time: int
    username: str


class FileAction(Enum):
    INSERT = "insert"
    DELETE = "delete"
    UPDATE = "update"


@dataclass(kw_only=True)
class ServerFileChange(ServerCommand):
    name: str = "s_file_change"
    change_time: int
    action: FileAction
    track: str
    username: str | None

    @override
    def data(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "change_time": self.change_time,
            "action": self.action.value,
            "track": self.track,
            "username": self.username,
        }

    @override
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Command:
        return cls(
            change_time=data["change_time"],
            action=FileAction(data["action"]),
            track=data["track"],
            username=data["username"],
        )


@dataclass(kw_only=True)
class ServerPlay(ServerCommand):
    name: str = "s_play"


@dataclass(kw_only=True)
class ServerPause(ServerCommand):
    name: str = "s_pause"


@dataclass(kw_only=True)
class ServerPrevious(ServerCommand):
    name: str = "s_previous"


@dataclass(kw_only=True)
class ServerNext(ServerCommand):
    name: str = "s_next"


COMMMANDS: list[type[Command]] = [
    ClientPlaying,
    ClientSubscribe,
    ClientToken,
    ClientPlay,
    ClientPause,
    ClientPrevious,
    ClientNext,
    ServerPlaying,
    ServerPlayed,
    ServerFileChange,
    ServerPlay,
    ServerPause,
    ServerPrevious,
    ServerNext,
]

_BY_NAME: dict[str, type[Command]] = {}

for command in COMMMANDS:
    _BY_NAME[command.name] = command


def parse(message: str) -> Command:
    json_message = json.loads(message)
    command_t = _BY_NAME.get(json_message["name"])
    if command_t is None:
        raise ValueError("unknown command")
    command = command_t.from_data(json_message)
    return command


async def send(sockets: web.WebSocketResponse | Iterable[web.WebSocketResponse], commands: Command | Iterable[Command]):
    if isinstance(sockets, web.WebSocketResponse):
        sockets = [sockets]
    if isinstance(commands, Command):
        commands = [commands]

    awaitables: list[Awaitable[None]] = []
    for socket in sockets:
        awaitables.extend([command.send(socket) for command in commands])

    await asyncio.gather(*awaitables)
