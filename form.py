# Selenium Curse 

# Import necessary modules
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configure WebDriver options
edge_options = Options()
# Set the path to the adblocker extension
extension_path = os.path.join(os.getcwd(), ".gitignore", "adBlocker.crx")
# Add adblocker extension
edge_options.add_extension(extension_path)

# Initialize the WebDriver
driver = webdriver.Edge(options=edge_options)

# Target web page to automate
URL = "https://practice.expandtesting.com/form-validation"

# Open the target web page
driver.get(URL)
# Close the adblocker tab
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "adblockultimate.net" in driver.current_url:
        driver.close()
        break
# Switch back to the main window
driver.switch_to.window(driver.window_handles[0])
# Fill out the form fields
try:
    # Locate the contact name field
    contact_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "ContactName"))
    )
    contact_name.clear()
    contact_name.send_keys("John Doe")
    
    # Locate the contact number field
    contact_number = driver.find_element(By.NAME, "contactnumber")
    contact_number.clear()
    contact_number.send_keys("098-1234567")
    
    # Locate Pickup Date field
    pickup_date = driver.find_element(By.NAME, "pickupdate")
    pickup_date.send_keys("12/12/2024")

    # Locate the Payment Method dropdown
    payment_method = driver.find_element(By.NAME, "payment")
    for option in payment_method.find_elements(By.TAG_NAME, "option"):
        if option.text == "card":
            option.click()
            break
    
    # Locate and click the Register button
    register_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
    register_button.click()

    # Wait form was submitted and confirmation page loaded
    confirmation_page = WebDriverWait(driver, 10).until(
        EC.url_contains("form-confirmation")
    )
    print("Form submitted successfully")
except TimeoutException:
    print("Timeout.Element not found.")

# Cleanup
finally:
    driver.quit()