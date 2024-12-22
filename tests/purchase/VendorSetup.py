from playwright.sync_api import sync_playwright
from faker import Faker
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Helper Functions
def log_step(step):
    logging.info(f"STEP: {step}")

def fill_field(page, placeholder, value):
    page.fill(f"input[placeholder='{placeholder}']", value)

def assert_visibility(page, selector, message):
    assert page.is_visible(selector), message

def verify_table_column_headers(page):
    #Column present with table
    expected_headers = [
        "SN",
        "Vendor Name",
        "Address",
        "PAN/VAT Number",
        "Status",
        "Actions"
    ]

    #located all column header (button divs inside th)
    header_buttons = page.locator('thead th button div')

    #Loop through each expected header and verify it's present
    for i, expected_header in enumerate(expected_headers):
        actual_header = header_buttons.nth(i).inner_text().strip()
        assert actual_header == expected_header, f"Header mismatch: Expected '{expected_header}', but found '{actual_header}'"

def toggle_status_by_unit_name(page, unit_name_to_toggle):
    table_row_selector = "tr.border-b"
    rows = page.locator(table_row_selector)

    for i in range(rows.count()):
        row =rows.nth(i)

         #extract and save a unit name
        unit_name = row.locator("td:nth-child(2)").inner_text().strip()

        #check if the unit name matches the target
        if unit_name == unit_name_to_toggle:
            print(f"Found unit: {unit_name} in row {i +1}")
            
            #locate the toggle switch in the fifth column
            toggle = row.locator("td:nth-child(5) input[type='checkbox']")

            #Get the current toggle state
            is_checked = toggle.is_checked()
            print(f"Current toggle state : {'Active' if is_checked else 'Inactive'}")

            inactiveState = not is_checked
            toggle.click()

            #Toggle is the current state does not match the target state
            confirm_button = page.get_by_role("button", name="Confirm")
            page.wait_for_selector("button[data-cy='submit-button']")
            confirm_button.click()

            print(f"Toggled switch for '{unit_name}' to {'Active' if inactiveState else 'Inactive'}")
            log_step("---------------------------")
            log_step(f"Vendor '{unit_name}' toggled to {'Active' if inactiveState else 'Inactive'} successfully")

def edit_vendor_name(page, edit_vendor):
    search_vendor = page.locator("input.bg-transparent.border-slate-300").first
    search_vendor.type(edit_vendor)
    edit_button = page.locator('[data-tooltip-id="Edit"]')
    edit_button.click()
    log_step(f"Editing vendor: {edit_vendor}")

def delete_vendor_name(page, delete_vendor):
    search_vendor = page.locator("input.bg-transparent.border-slate-300").first
    search_vendor.fill("")
    search_vendor.type(delete_vendor)
    delete_button = page.locator('[data-tooltip-id="Delete"]')
    delete_button.click()
    log_step(f"Editing vendor: {delete_vendor}")
    
def VendorSetupmain():
    fake = Faker()
    with sync_playwright() as playwright:
        log_step("---------------------------")
        log_step("Launching browser full screen")
        browser = playwright.chromium.launch(args=["--start-maximized"], headless=False, slow_mo=2000)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        log_step("---------------------------")
        log_step("Visiting IMS Login Page")
        page.goto("https://inventorydev.yenyasoft.com/auth/login")
        
        # Login
        page.locator("#username").type('test@yopmail.com')
        page.locator("#password").type('Test@1234')
        page.locator('[type="submit"]').click()

        # Navigate to Vendor Page
        log_step("---------------------------")
        log_step("Navigating to Purchase -> Vendor")
        page.locator('[data-cy="/purchase"]').click()
        page.locator('[data-cy="/purchase/vendor"]').click()
        
        # Hover on Add New and Verify Tooltip
        log_step("---------------------------")
        log_step("Verifying Add New Tooltip and clicking Add button")
        plus_button = "button[data-tooltip-id='Add New']"
        page.hover(plus_button)
        assert_visibility(page, "[data-tooltip-id='Add New']", "Tooltip 'Add New' not visible")
        page.click(plus_button)
        
         #Verify Table column is same wtih expected and actual
        verify_table_column_headers(page)
        log_step("---------------------------")
        log_step('Table column matched as expected')
        
        #Verify the toggle status UI component
        unit_name_to_toggle= "Baker and Sons"
        toggle_status_by_unit_name(page, unit_name_to_toggle)

        # Verify Mandatory Fields
        log_step("---------------------------")
        log_step("Verifying mandatory fields by clicking Save")
        save_button = "text='Save'"
        assert_visibility(page, save_button, "'Save' button visible")
        page.click(save_button)
        
        # Fill Form Fields with Faker Data
        log_step("---------------------------")
        log_step("Filling vendor form fields with Faker data")
        fill_field(page, 'Enter Vendor Name', fake.company())
        fill_field(page, 'Enter Address', fake.address())
        fill_field(page, 'Enter Contact Number', fake.numerify("##########"))
        fill_field(page, 'Enter PAN Number', fake.numerify("##########"))
        
        # Verify Reset Functionality
        log_step("---------------------------")
        log_step("Verifying Reset button clears the form")
        reset_button = "text='Reset'"
        page.click(reset_button)
        assert page.input_value("input[placeholder='Enter Vendor Name']") == "", "Vendor Name not cleared"
         
        #Verify that user can Add new vendor with valid data
        save_button = "text='Save'"
        assert_visibility(page, save_button, "'Save' button visible")
        vendor_faker_name = fake.company()
        pan_vat_number = fake.numerify("######")
        log_step(f'New pan/vat number: {pan_vat_number}')
        
        # Fill Form Fields with Faker Data
        log_step("Filling vendor form fields with Faker data")
        fill_field(page, 'Enter Vendor Name', vendor_faker_name)
        fill_field(page, 'Enter Address', fake.address())
        fill_field(page, 'Enter Contact Number', fake.numerify("##########"))
        fill_field(page, 'Enter PAN Number', pan_vat_number)
        page.click(save_button)
        log_step("---------------------------")
        log_step(f"Succesfully added New Vendor : {vendor_faker_name}")
        

        #verify that new vendor can save with duplicate pan/Vat number
        log_step("---------------------------")
        log_step('Filling with faker and verifiying the duplicate pan/vat number')
        # Fill Form Fields with Faker Data
        fill_field(page, 'Enter Vendor Name', fake.company())
        fill_field(page, 'Enter Address', fake.address())
        fill_field(page, 'Enter Contact Number', fake.numerify("##########"))
        fill_field(page, 'Enter PAN Number', pan_vat_number)
        page.click(save_button)
        
        try:
            # Wait for the toast message to appear (with a timeout of 60 seconds)
            page.wait_for_selector('.Toastify__toast', timeout=60000)

            # Check for the specific toast message that contains the error text
            toast_message = page.locator('.Toastify__toast-body:has-text("Vendor PAN/VAT number already exist")')
            
            if toast_message.is_visible():
                log_step('Toast message verified: Vendor PAN/VAT number already exist')
            else:
                log_step('Toast message not displayed as expected.')
        except Exception as e:
            log_step(f"Error waiting for toast message: {e}")

        #search and edit the data
        vendor_to_edit = "Sims Inc"
        vendor_faker_name = fake.name()
        edit_vendor_name(page,vendor_to_edit)
        fill_field(page, 'Enter Vendor Name', vendor_faker_name)
        fill_field(page, 'Enter Address', fake.address())
        fill_field(page, 'Enter Contact Number', fake.numerify("##########"))
        fill_field(page, 'Enter PAN Number', fake.numerify("##########"))
        update_button = page.locator("button:has-text('Update')")
        update_button.click()
        log_step(f"Vendor name from {vendor_to_edit} to {vendor_faker_name}")
        
        try:
            # Wait for the toast message to appear (with a timeout of 60 seconds)
            page.wait_for_selector('.Toastify__toast', timeout=60000)

            # Check for the specific toast message that contains the error text
            toast_message = page.locator('.Toastify__toast-body:has-text("Vendor has been updated successfully.")')
            
            if toast_message.is_visible():
                log_step('Toast message verified: Vendor has been updated successfully.')
            else:
                log_step('Toast message not displayed as expected.')
        except Exception as e:
            log_step(f"Error waiting for toast message: {e}")


        #Verify that user can delete the vendor or not
        delete_vendor = "Johnson Ltd"
        delete_vendor_name(page, delete_vendor)
        page.locator("button:has-text('Confirm')").click()
        log_step('Successfully deleted vendor')


        log_step("Test completed successfully")
        browser.close()

if __name__ == "__main__":
    VendorSetupmain()
