import asyncio
import pytest
import pytest_asyncio
from nundb import NunDB

@pytest_asyncio.fixture(scope="function")
async def nundb():
    """Fixture to initialize the NunDB client."""
    client = NunDB("ws://localhost:3012", "user-name", "user-pwd")
    await client.connect(client.url, client.name, client.pwd)
    await client.create_db("aware", "aware")
    await client.use_db("aware", "aware")
    try:
        yield client
    finally:
        await client.websocket.close()


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_get_value_before_setting(nundb):
    """Test: Retrieve a value before setting it."""
    value = await nundb.get("before")
    print(f"VALOR DE VALUE {value}")
    assert value == "<Empty>"


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_get_value_after_setting(nundb):
    """Test: Retrieve a value after setting it."""
    await nundb.set("after", "ok")
    value = await nundb.get("after")
    assert value == "ok"


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_watching_value(nundb):
    """Test: Watch a value in real-time."""
    cache = []

    def watcher_callback(data):
        cache.append(data)

    await nundb.add_watch("km", watcher_callback)
    await nundb.set("km", "2")
    await nundb.set("km", "3")
    await nundb.set("km", "4")
    await nundb.set("km", "5")

    await asyncio.sleep(0.5)
    assert len(cache) == 4
    assert all(item in cache for item in ["2", "3", "4", "5"])


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_increment_value(nundb):
    """Test: Increment a value."""
    await nundb.set("age", "17")
    await nundb.increment("age", 1)
    value = await nundb.get("age")
    assert value == "18"


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_remove_watcher(nundb):
    """Test: Remove a watcher."""
    cache = []

    def watcher_callback(data):
        cache.append(data)

    await nundb.add_watch("remove", watcher_callback)
    await nundb.set("remove", "initial")
    await asyncio.sleep(0.1)
    await nundb.remove_watcher("remove")
    await nundb.set("remove", "modified")

    await asyncio.sleep(0.5)
    assert len(cache) == 1
    assert cache[0] == "initial"


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_get_keys(nundb):
    """Test: Retrieve all keys."""
    await nundb.set("test", "123")
    await nundb.set("km", "1")
    await nundb.set("after", "1")
    await nundb.set("remove", "1")

    await asyncio.sleep(0.5)
    all_keys = await nundb.all_keys()
    keys_containing = await nundb.keys_contains("es")
    keys_starting_with = await nundb.keys_starting_with("t")
    keys_ending_with = await nundb.keys_ending_with("st")

    print(all_keys)

    expected_keys = ["$$token", "$connections", "after", "km", "remove", "test"]
    assert all(key in all_keys for key in expected_keys)
    assert keys_containing == ["test"]
    assert keys_starting_with == ["test"]
    assert keys_ending_with == ["test"]


@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_get_all_databases(nundb):
    """Test: Retrieve all databases."""
    all_databases = await nundb.get_all_databases()
    assert "$admin" in all_databases
    assert "aware" in all_databases
