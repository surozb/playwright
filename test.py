from playwright.sync_api import sync_playwright

def verify_column_headers(page):
    # Define expected headers
    expected_headers = [
        "SN",
        "Vendor Name",
        "Address",
        "PAN/VAT Number",
        "Status",
        "Actions"
    ]
    
    # Locate all column headers (button divs inside th)
    header_buttons = page.locator('thead th button div')

    # Loop through each expected header and verify it's present
    for i, expected_header in enumerate(expected_headers):
        # Get the actual text from the column header
        actual_header = header_buttons.nth(i).inner_text().strip()
        assert actual_header == expected_header, f"Header mismatch: Expected '{expected_header}', but got '{actual_header}'"

    print("All headers are displayed correctly")

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=2000)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the page with the table (Replace with your actual URL)
        page.goto("https://inventorydev.yenyasoft.com/auth/login")

        username = page.locator("#username")
        username.type('test@yopmail.com')

        password = page.locator("#password")
        password.type('Test@1234')

        signIn = page.locator('[type="submit"]').click()

        #Goto purchase Menu
        purchase = page.locator('[data-cy="/purchase"]').click()
        purchaseVendor = page.locator('[data-cy="/purchase/vendor"]').click()

        # Call the function to verify the headers
        verify_column_headers(page)

        browser.close()

if __name__ == "__main__":
    main()
