from pages.login_page import LoginPage

def test_valid_login(playwright):
    page = playwright.chromium.launch(headless=False).new_page()
    login = LoginPage(page)
    login.goto()
    login.perform_login("test@yopmail.com", "Test@1234")
    assert "Dashboard" in page.title()
