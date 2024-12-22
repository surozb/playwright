from playwright.sync_api import sync_playwright
from faker import Faker

with sync_playwright() as playwright:
    #launch a browser
    browser = playwright.chromium.launch(args=["--start-maximized"], headless = False, slow_mo= 2000)

    #Create a new page
    context = browser.new_context(no_viewport=True)
    page = browser.new_page()

    #Visit the IMS landing page
    page.goto("https://inventorydev.yenyasoft.com/auth/login")

    username = page.locator("#username")
    username.type('test@yopmail.com')

    password = page.locator("#password")
    password.type('Test@1234')

    signIn = page.locator('[type="submit"]').click()

    #Goto purchase Menu
    purchase = page.locator('[data-cy="/purchase"]').click()
    purchaseVendor = page.locator('[data-cy="/purchase/vendor"]').click()

    # Hover over the '+' button
    plus_button_selector = "button[data-tooltip-id='Add New']"  # Target the button
    page.hover(plus_button_selector)

    #Verify the "Add Vendor" button is visible
    tooltip_selector = "[data-tooltip-id='Add New']"  # Tooltip element
    assert page.is_visible(tooltip_selector), "Tooltip 'Add New' is not visible after hover"

    #Verify that user can click on Add button
    page.click(plus_button_selector)

    #Verify mandatory fields
    save_button = "text='Save'"
    # Verify the 'Save' button is visible
    assert page.is_visible(save_button), "'Save' button is not visible."
    # Click the 'Save' button
    page.click(save_button)
    print("'Save' button is clicked successfully.")

    #Verify "Reset" button functionality
     # Generate dynamic dummy data using Faker
    fake = Faker()
    vendor_name = fake.company()
    address = fake.address()
    contact_number = fake.numerify("##########")  # Generates 10-digit number
    pan_number = fake.numerify("##########")      # Generates 10-digit PAN number
     # Fill out the form fields with Faker-generated data
    page.fill("input[placeholder='Enter Vendor Name']", vendor_name)
    page.fill("input[placeholder='Enter Address']", address)
    page.fill("input[placeholder='Enter Contact Number']", contact_number)
    page.fill("input[placeholder='Enter PAN Number']", pan_number)

    
    browser.close()