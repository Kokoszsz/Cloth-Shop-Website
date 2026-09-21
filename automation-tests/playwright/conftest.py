import os
import socket
import subprocess
import sys
import time
import urllib.request
from collections.abc import Iterator
from pathlib import Path

import pytest
from data import CATALOGUE_FILE, PRODUCT_IDS
from pages.basket_page import BasketPage
from pages.catalogue_page import CataloguePage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.menu import MenuPage
from pages.product_page import ProductPage
from playwright.sync_api import APIRequestContext, Page, Playwright

HOST = '127.0.0.1'
WEB = Path(__file__).resolve().parents[2] / 'cloth-shop' / 'Web'
STARTUP_TIMEOUT = 30


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind((HOST, 0))
        return probe.getsockname()[1]


def seed_database(database_url: str) -> None:
    subprocess.run(
        [sys.executable, str(WEB / 'create_database.py')],
        env={**os.environ, 'DATABASE_URL': database_url, 'SEED_JSON': str(CATALOGUE_FILE)},
        check=True,
    )


def wait_until_ready(server: subprocess.Popen, url: str) -> None:
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        if server.poll() is not None:
            raise RuntimeError(f'The shop exited with code {server.returncode} while starting')
        try:
            with urllib.request.urlopen(url, timeout=1):
                return
        except OSError:
            time.sleep(0.2)
    raise RuntimeError(f'The shop did not answer on {url} within {STARTUP_TIMEOUT}s')


@pytest.fixture(scope='session')
def shop_server(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    database = tmp_path_factory.mktemp('shop') / 'shop.db'
    database_url = f'sqlite:///{database.as_posix()}'
    seed_database(database_url)

    port = free_port()
    url = f'http://{HOST}:{port}'
    server = subprocess.Popen(
        [
            sys.executable, '-m', 'flask', '--app', 'main:create_app()',
            'run', '--host', HOST, '--port', str(port), '--no-reload',
        ],
        cwd=WEB,
        env={**os.environ, 'APP_ENV': 'development', 'DATABASE_URL': database_url},
    )
    try:
        wait_until_ready(server, url)
        yield url
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()


@pytest.fixture(scope='session')
def base_url(shop_server: str) -> str:
    return shop_server

@pytest.fixture
def menu_page(page: Page) -> MenuPage:
    return MenuPage(page)


@pytest.fixture
def catalogue_page(page: Page) -> CataloguePage:
    return CataloguePage(page)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)


@pytest.fixture
def basket_page(page: Page) -> BasketPage:
    return BasketPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def other_request(playwright: Playwright, base_url: str) -> Iterator[APIRequestContext]:
    request = playwright.request.new_context(base_url=base_url)
    yield request
    request.dispose()


@pytest.fixture(scope='session')
def unrated_products() -> Iterator[int]:
    return iter(PRODUCT_IDS.values())
