import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        yield browser
        browser.close()
