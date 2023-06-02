from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

profile = FirefoxProfile()
profile.set_preference("signon.rememberSignons", True)
profile.set_preference("signon.autologin.proxy", True)
profile_path = "/files_conf/profile/"
profile.set_preference("webdriver.firefox.profile", profile_path)

options = Options()
options.headless = True
options.profile = profile
driver = webdriver.Firefox(options=options)

print('Login to your youtube channel! (Ignore if you dont want youtube functionalities)')

driver.get("https://www.youtube.com/account_advanced?hl=en-GB")

print('Youtube email: ')
email_field = driver.find_element_by_id("identifierId")
email_input = input()
email_field.send_keys(email_input)


next_button = driver.find_element_by_id("identifierNext")
next_button.click()
driver.implicitly_wait(5)

print('Youtube password: ')
password_field = driver.find_element_by_name("password")
password_input = input()
password_field.send_keys(password_input)

login_button = driver.find_element_by_id("passwordNext")
login_button.click()

profile.update_preferences()
profile.save(profile_path)