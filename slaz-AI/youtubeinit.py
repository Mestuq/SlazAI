from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import iniload

# Initialize Firefox profile with specific preferences
profile = FirefoxProfile()
profile.set_preference("signon.rememberSignons", True)  # Remember login credentials
profile.set_preference("signon.autologin.proxy", True)  # Enable autologin for proxy
profile_path = "/files_conf/profile/"
profile.set_preference("webdriver.firefox.profile", profile_path)  # Set the profile path

# Configure Firefox options for headless mode and set the profile
options = Options()
options.headless = True  # Run Firefox in headless mode (no GUI)
options.profile = profile  # Use the configured profile
driver = webdriver.Firefox(options=options)  # Initialize the Firefox WebDriver with the options

print('Login to your YouTube channel! (Ignore if you don\'t want YouTube functionalities)')

# Navigate to YouTube's advanced account settings page
driver.get("https://www.youtube.com/account_advanced?hl=en-GB")

# Find the email input field and enter the email
email_field = driver.find_element_by_id("identifierId")
email_input = iniload.ini_load('dane.conf', 'YoutubeModule', 'email', '0')  # Load email from config file
if email_input == '0':  # If email is not found in config, prompt user for input
    print('YouTube email: ')
    email_input = input()
email_field.send_keys(email_input)  # Enter the email into the field

# Click the "Next" button to proceed to the password input
next_button = driver.find_element_by_id("identifierNext")
next_button.click()
driver.implicitly_wait(5)  # Wait for the page to load

# Find the password input field and enter the password
password_field = driver.find_element_by_name("password")
password_input = iniload.ini_load('dane.conf', 'YoutubeModule', 'password', '0')  # Load password from config file
if password_input == '0':  # If password is not found in config, prompt user for input
    print('YouTube password: ')
    password_input = input()
password_field.send_keys(password_input)  # Enter the password into the field

# Click the "Next" button to complete the login process
login_button = driver.find_element_by_id("passwordNext")
login_button.click()

# Update and save the Firefox profile with the new preferences
profile.update_preferences()
profile.save(profile_path)