import asyncio
import enum
import json
import os
from typing import Optional, List

import requests

import server_rnr


@enum.unique
class RunnerStatus(enum.Enum):
    STANDING_BY = enum.auto()
    UPDATING = enum.auto()
    RUNNING = enum.auto()


class MCRunner:
    def __init__(self, path: str):
        self._path = path
        self._status = RunnerStatus.STANDING_BY
        self._connections: List[server_rnr.WSConnection] = []
        self._process: Optional[asyncio.subprocess.Process] = None

    @property
    def status(self):
        return self._status.name

    def register_connection(self, connection):
        self._connections.append(connection)

    def unregister_connection(self, connection):
        self._connections.remove(connection)

    def get_ws_handler(self):
        return server_rnr.WSConnection.ws_handler(self)

    def update(self, version: str):
        if self._status != RunnerStatus.STANDING_BY:
            return

        async def run():
            await self._set_status(RunnerStatus.UPDATING)
            await self._update(version)
            await self._set_status(RunnerStatus.STANDING_BY)

        asyncio.create_task(run())

    async def _update(self, version: str):
        url = self._fetch_version_url(version)
        if url is not None:
            details = json.loads(requests.get(url).content)
            if not os.path.exists(self._path):
                os.mkdir(self._path)
            with open(os.path.join(self._path, 'server.jar'), 'wb') as server_file:
                response = requests.get(details['downloads']['server']['url'], stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:
                    server_file.write(response.content)
                else:
                    done = 0
                    total_length = int(total_length)
                    for chunk in response.iter_content(chunk_size=1024 * 512):
                        done += len(chunk)
                        server_file.write(chunk)
                        await asyncio.sleep(0)
                        await self._notify_connections(f'UPDATING:{done}:{total_length}')

    def run(self):
        if self._status != RunnerStatus.STANDING_BY:
            return

        async def run():
            await self._set_status(RunnerStatus.RUNNING)
            await self._run()
            await self._set_status(RunnerStatus.STANDING_BY)

        asyncio.create_task(run())

    async def _run(self):
        self._process = await asyncio.create_subprocess_exec(
            'java', '-Xmx1024M', '-Xms1024M', '-jar', os.path.join(self._path, 'server.jar'), 'nogui',
            cwd=self._path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE)
        for task in iter(self._process.stdout.readline, ''):
            line = await task
            if len(line) > 0:
                await self._notify_connections(f'STDOUT:{line.rstrip().decode("utf-8")}')
            else:
                break
        self._process = None

    def write(self, command):
        async def run():
            await self._write(command)
        asyncio.create_task(run())

    async def _write(self, command):
        if self._process is not None:
            self._process.stdin.write((command + '\n').encode('UTF-8'))
            await self._process.stdin.drain()

    async def _notify_connections(self, message: str):
        for connection in self._connections:
            await connection.push_message(message)

    async def _set_status(self, status: RunnerStatus):
        self._status = status
        await self._notify_connections(f'STATUS:{self.status}')

    def _fetch_version_url(self, version: str) -> Optional[str]:
        versions = json.loads(
            requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json').content
        )['versions']
        for v in versions:
            if v['id'] == version:
                return v['url']
        return None
