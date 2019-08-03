from contextlib import suppress, contextmanager
from sys import platform
import socket
import enum
import json
import os
import struct
import uuid


@contextmanager
def reconnect_on_failure(discord):
    try:
        yield
    except (OSError, socket.error, BrokenPipeError, ConnectionResetError):
        discord.reconnect()


class OP(enum.Enum):
    AUTHENTICATE = 0
    FRAME = 1
    CLOSE = 2


class Message:
    @staticmethod
    def authenticate(client_id, version=1):
        return {"v": version, "client_id": client_id}

    @staticmethod
    def set_activity(activity, nonce, pid=os.getpid()):
        return {
            "cmd": "SET_ACTIVITY",
            "args": {
                "activity": activity,
                "pid": pid
            },
            "nonce": nonce
        }


class DiscordError(Exception):
    pass


class NoDiscordClientError(DiscordError):
    pass


class ReconnectError(DiscordError):
    pass


class Discord(object):
    def __init__(self, client_id=None, reconnect_threshold=5):
        # Reconnect props
        self.reconnect_threshold = reconnect_threshold
        self.reconnect_counter = 0

        # Sockets
        self.socket = None

        # Discord
        if platform in ("win32", "cygwin"):
            self.ipc_path = "\\\\?\\pipe\\discord-ipc-0"
        else:
            # Stolen from https://github.com/GiovanniMCMXCIX/PyDiscordRPC/blob/master/rpc.py
            env_vars = ['XDG_RUNTIME_DIR', 'TMPDIR', 'TMP', 'TEMP']
            path = next((os.environ.get(path, None) for path in env_vars if path in os.environ), '/tmp')
            self.ipc_path = "{}/discord-ipc-0".format(path)
        self.client_id = client_id

    def connect(self, client_id=None):
        try:
            os.stat(self.ipc_path)
        except FileNotFoundError:
            raise NoDiscordClientError()
        self.client_id = self.client_id or client_id
        try:
            if platform in ("win32", "cygwin"):
                self.socket = open(self.ipc_path, "r+b")
            else:
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket.connect(self.ipc_path)
        except (OSError, ConnectionAbortedError, ConnectionRefusedError):
            raise NoDiscordClientError()
        self.handshake()

    def disconnect(self):
        with suppress(OSError, socket.error, BrokenPipeError):
            self.socket.close()
        self.socket = None

    def send(self, op, payload):
        if isinstance(op, OP):
            op = op.value
        payload = json.dumps(payload).encode("utf8")
        body = struct.pack("<ii", op, len(payload)) + payload
        with reconnect_on_failure(self):
            if platform in ("win32", "cygwin"):
                self.fp.write(body)
                self.fp.flush()
            else:
                return self.socket.sendall(body)
        return None

    def set_activity(self, activity, pid=os.getpid()):
        nonce = str(uuid.uuid4())
        self.send(OP.FRAME, Message.set_activity(activity, nonce, pid))
        op, length = self.recv()
        if not op and not length:
            # There was a successful reconnect attempt
            return self.set_activity(activity, pid)
        body = self.recv_body(length)
        if not body:
            return self.set_activity(activity, pid)
        assert body["cmd"] == "SET_ACTIVITY"
        assert body["nonce"] == nonce

    def shutdown(self):
        with suppress(OSError):
            self.send(OP.CLOSE, {})
        self.disconnect()

    def recv(self):
        with reconnect_on_failure(self):
            method = self.socket.recv
            if platform in ("win32", "cygwin"):
                method = self.socket.read
            return struct.unpack("<ii", method(8))
        return (None, None)

    def recv_body(self, length):
        method = self.socket.recv
        if platform in ("win32", "cygwin"):
            method = self.socket.read
        with reconnect_on_failure(self):
            body = json.loads(method(length).decode("utf8"))
            if body["evt"] == "ERROR":
                raise DiscordError(body["data"]["message"])
            return body
        return None

    def handshake(self):
        self.send(OP.AUTHENTICATE, Message.authenticate(str(self.client_id)))
        op, length = self.recv()
        assert op == OP.FRAME.value
        body = self.recv_body(length)
        assert body["evt"] == "READY"
        return body

    def reconnect(self):
        if self.reconnect_counter > self.reconnect_threshold:
            raise ReconnectError("reconnect_counter > reconnect_threshold")
        self.disconnect()
        self.reconnect_counter += 1
        self.connect(self.client_id)
