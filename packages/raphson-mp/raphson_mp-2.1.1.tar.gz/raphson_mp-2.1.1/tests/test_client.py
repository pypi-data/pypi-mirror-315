import asyncio
import random
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType

import pytest
from aiohttp.test_utils import TestServer

from raphson_mp import db, logconfig, settings
from raphson_mp.client import RaphsonMusicClient
from raphson_mp.client.track import Track
from raphson_mp.common.image import ImageFormat, ImageQuality
from raphson_mp.common.track import AudioFormat
from raphson_mp.server import Server


def setup_module(_module: ModuleType):
    settings.data_dir = Path("./data").resolve()
    settings.music_dir = Path("./music").resolve()
    logconfig.apply_debug()


@pytest.fixture
async def client() -> AsyncIterator[RaphsonMusicClient]:
    with db.connect(read_only=True) as conn:
        (token,) = conn.execute("SELECT token FROM session LIMIT 1").fetchone()

    print("obtained arbitrary token from database:", token)

    server = Server(False)
    test_server = TestServer(server.app)
    await test_server.start_server()
    client = RaphsonMusicClient()
    base_url = str(test_server._root)
    await client.setup(base_url=base_url, token=token, user_agent="client test suite")
    yield client
    await client.close()
    await test_server.close()


async def get_random_track(client: RaphsonMusicClient) -> Track:
    playlist = random.choice(await client.playlists())
    return await client.choose_track(playlist)


async def test_choose_track(client: RaphsonMusicClient):
    track = await get_random_track(client)
    track2 = await client.get_track(track.path)
    assert track == track2


async def test_download_news(client: RaphsonMusicClient):
    await client.get_news()


async def test_list_tracks(client: RaphsonMusicClient):
    playlist = random.choice(await client.playlists())
    tracks = await client.list_tracks(playlist.name)
    track = random.choice(tracks)
    await client.get_track(track.path)  # verify the track exists


async def test_download_cover(client: RaphsonMusicClient):
    track = await get_random_track(client)
    await asyncio.gather(
        *[
            track.get_cover_image(format=format, quality=quality, meme=meme)
            for format in ImageFormat
            for quality in ImageQuality
            for meme in (False, True)
        ]
    )


# this test is at the end because it takes a while
async def test_download_audio(client: RaphsonMusicClient):
    track = await get_random_track(client)
    await asyncio.gather(*[track.get_audio(format) for format in AudioFormat])
