import time
import os
import argparse
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_headers import Headers

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--heroku', default=False, action='store_true', help='Heroku config')
args = parser.parse_args()


header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate only Windows platform
    headers=False
)

if args.heroku:
    print('Initialiting bot with Heroku config.')
    customUserAgent = header.generate()['User-Agent']
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={customUserAgent}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-data-dir=selenium")

    bot = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    bot.implicitly_wait(20)

else:
    customUserAgent = header.generate()['User-Agent']
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={customUserAgent}")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("user-data-dir=/Users/leandrohandal/Library/Application Support/Google/Chrome/Profile 1")

    s = Service(ChromeDriverManager(log_level=0).install())
    bot = webdriver.Chrome(service=s, options=options)
    bot.implicitly_wait(10)

print('Fetching page...')
bot.get('https://seguro.camelot.casandra.com.mx/webapp/default.aspx')
try:
    username_field = bot.find_element(by='id', value='ctl00_Contenido_UID')
    username_field.send_keys('CA-0405i3')
    print('Logging in...')
    password_field = bot.find_element(by='id', value='ctl00_Contenido_PWD')
    password_field.send_keys('handal405')

    login_button = bot.find_element(by='id', value='ctl00_Contenido_BLogin')
    login_button.click()

except NoSuchElementException:
    print('Already logged in. Continuing...')
    pass
print('Clicking on reservations')
bot.execute_script("javascript:location.href='reservaciones.aspx'")
# Gym
print('Selecting GIMNASIO CLAUDEL...')
bot.find_element(by='id', value='ctl00_Contenido_REPACS_ctl05_BSel').click()
print('Acepting pop-up')
banner = bot.find_element(by='id', value='ctl00_Contenido_UpdatePanel3')
banner.find_element(by='class name', value='btn-success').click()
time.sleep(2)
print('Selecting day view')
dia = bot.find_element(by='class name', value='rsHeaderDay').click()
time.sleep(5)
print('Selecting tomorrow as date')
bot.find_element(by='class name', value='rsNextDay').click()
time.sleep(5)
print('Clicking on first slot')
slots = bot.find_element(by='class name', value='rsContentScrollArea')
slots = [el for el in slots.find_elements(by='tag name', value='tr')]
print('Right clicking to reserve')
action = ActionChains(bot)
action.context_click(slots[0]).perform()
reserva_popup = bot.find_element(by='id', value='ctl00_Contenido_CalRsv_timeSlotContextMenu_detached')
print('Selecting reserve option')
# Nueva Reservacion
time.sleep(2)
reserva_popup.find_elements(by='tag name', value='li')[0].click()
print('Filling data for reservation...')
instrucciones_field = bot.find_element(by='id', value='ctl00_Contenido_CalRsv_Form_RsvIns_txtInstrucciones')
instrucciones_field.send_keys('.')
start = '9:00'
end = '10:00'
start_time = bot.find_element(by='id', value='ctl00_Contenido_CalRsv_Form_RsvIns_StartTime_dateInput')
start_time.clear()
start_time.send_keys(start)

end_time = bot.find_element(by='id', value='ctl00_Contenido_CalRsv_Form_RsvIns_EndTime_dateInput')
end_time.clear()
end_time.send_keys(end)

print('Submitting')
submit_btn = bot.find_element(by='id', value='ctl00_Contenido_CalRsv_Form_RsvIns_UpdateButton')
submit_btn.click()
time.sleep(5)
print('Done! Closing now...')
cerrar_btn = bot.find_element(by='id', value='ctl00_Contenido_BCerrar')
cerrar_btn.click()
bot.quit()