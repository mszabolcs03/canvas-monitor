import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.chrome.service import Service
from seleniumbase import Driver


import pyperclip
import random
import datetime
import pyautogui
notifier = notifications.ToastNotificationManager.create_toast_notifier('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe')


def log(text, type):
    log_file = open("log.txt", 'a')
    log_file.write(str(datetime.datetime.now())[0:19] + ": " + text + "\n")
    log_file.close()

    if type == "success":
        print(bcolors.OKGREEN + text + bcolors.ENDC)
    if type == "error":
        print(bcolors.FAIL + text + bcolors.ENDC)
    if type == "group":
        print(bcolors.UNDERLINE + text + bcolors.ENDC)
    if type == "info":
        print(bcolors.OKBLUE + text + bcolors.ENDC)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def notify(text, type):
    tString = "<toast><visual><binding template='ToastGeneric'><text>" + text + "</text></binding></visual></toast>"
    xDoc = dom.XmlDocument()
    xDoc.load_xml(tString)
    log(text, type)
    # notifier.show(notifications.ToastNotification(xDoc))

def type(w):
    for i in w:
        pyautogui.typewrite(i)
        time.sleep(random.uniform(0, 0.02))

pyautogui.PAUSE = 0

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# driver = webdriver.Chrome(service=service, options=options)

driver = Driver(browser="chrome", driver_version="118")


course = "26299"
url = "https://canvas.tue.nl/courses/" + course + "/groups"


email = ""
pw = ""
def login():
    log("Starting...", "success")
    time.sleep(2)

    driver.get(url)

    time.sleep(2)
    type(email)
    pyautogui.press("ENTER")
    time.sleep(3)
    type(email)
    pyautogui.press("TAB")
    type(pw)
    pyautogui.press("ENTER")

    # time.sleep(10)

# pyperclip.copy(email)
# input()
# pyperclip.copy(pw)
# print("Running")
# print()

success = False
groups = [
    "3 Tue"
]

def check():
    global success
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "student-group-join")))
        for group in groups:
            title_element = driver.find_elements(By.XPATH, "//*[contains(text(), '" + group + "')]")[0]
            title_element_parents = title_element.find_elements(By.XPATH, "//div[.//h2[contains(text(), '" + group + "')]]")

            # find group_element
            for element in title_element_parents:
                # print(i.get_attribute("class"))
                if element.get_attribute("class") == "student-group-header align-items-center clearfix":
                    group_element = element

            join_element = group_element.find_element(By.CLASS_NAME, "student-group-join").find_element(By.XPATH, ".//*")

            join_type = join_element.get_attribute("aria-label").split(" ")[0].lower()
            if join_type == "group": join_type = "full"

            log((group + ": " + join_type), "group")

            if join_type == "switch" or join_type == "join":
                join_element.click()
                success = True
                notify(("JOINED GROUP " + group +"!"), "success")
                return
    except:
        notify(("Error"), "error")



login()
while success == False:
    try:
        check()
    except:
        driver.get(url)
    for i in range(2 + random.randint(0,2)):
        print(".", end="")
        time.sleep(1 + random.uniform(0, 0.2))
    print("")
    # print(bcolors.OKCYAN + "refreshing ("  + str(datetime.datetime.now()) + ")" + bcolors.ENDC)
    log("refreshing ("  + str(datetime.datetime.now()) + ")", "info")
    try:
        driver.get(url)
    except:
        #notify(("Error"), "error")
        # login()
        pass
