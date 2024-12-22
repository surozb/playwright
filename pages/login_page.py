class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_field = "#username"
        self.password_field = "#password"
        self.submit_button = "[type='submit']"

    def goto(self):
        self.page.goto("https://inventorydev.yenyasoft.com/auth/login")

    def perform_login(self, username, password):
        self.page.fill(self.username_field, username)
        self.page.fill(self.password_field, password)
        self.page.click(self.submit_button)
