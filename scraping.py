from selenium import webdriver

# Set the path to the Chromedriver
DRIVER_PATH = '/chromedriver-win64'

# Initialize the Chrome driver
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# Navigate to the URL
driver.get('https://google.com')

# It's a good practice to close the browser when done
driver.quit()