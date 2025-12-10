# Selenium Curse 

# Import necessary modules
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.edge.options import Options

# Configure WebDriver options
edge_options = Options()
# Set the path to the adblocker extension
extension_path = os.path.join(os.getcwd(), ".gitignore", "adBlocker.crx")
# Add adblocker extension
edge_options.add_extension(extension_path)  

# Initialize the WebDriver
driver = webdriver.Edge(options=edge_options)

# Web page to automate
base_url = "https://www.globalsqa.com/demo-site/"

# Open the web page
driver.get(base_url)
# Close the adblocker tab
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "adblockultimate.net" in driver.current_url:
        driver.close()
        break
# Switch back to the main window
driver.switch_to.window(driver.window_handles[0])
# Wait for the button 'Porgress Bar' presnce and click it
try:
    progress_bar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='post-2715']/div[2]/div/div/div[2]/div[1]/ul/li[7]"))
    )
    progress_bar_button.click()
except TimeoutException:
    print("Timeout")