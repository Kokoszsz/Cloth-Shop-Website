import json
import re
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

CATALOGUE_FILE = Path(__file__).with_name('catalogue.json')
DEFAULT_PASSWORD = 'longpass1'
PRICE_IN_DOLLARS = re.compile(r'\d+\.\d{2} \$')

PRODUCT_IDS = {
    name: product_id
    for product_id, name, *_ in json.loads(CATALOGUE_FILE.read_text())['products']
}


@dataclass(frozen=True)
class Customer:
    username: str
    email: str
    password: str


def unique_username() -> str:
    return f'user_{uuid4().hex[:8]}'


def unique_email() -> str:
    return f'{uuid4().hex[:8]}@shop.test'


def product_id(name: str) -> int:
    return PRODUCT_IDS[name]
