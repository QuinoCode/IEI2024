from fnmatch import translate
import os
from selenium import webdriver
from selenium.webdriver.common import service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class Scrapper:
    def __init__(self):
        self.geckodriver_path = os.path.join(os.path.dirname(__file__), "../../../geckodriver")
        self.install_dir = "/usr/bin"
        self.binary_loc = os.path.join(self.install_dir, "firefox")

        self.driver = self.instantiate_service_with_driver()
        self.wait = WebDriverWait(self.driver, 10)

        self.type_of_coordenate_system = None
        self.decimal_switcher = None
        self.x_coordenate = None
        self.y_coordenate = None
        self.transform_button = None
        self.longitudeDegree = None
        self.longitudeOrientation = None
        self.latitudeDegree = None
        self.latitudeOrientation = None

    #Instantiate a service with the driver
    def instantiate_service_with_driver(self):
        service = FirefoxService(self.geckodriver_path)
        opts = webdriver.FirefoxOptions()
        opts.binary_location = self.binary_loc
        opts.add_argument("-profile")
        opts.add_argument("/home/ayuda106/snap/firefox/common/.mozilla/firefox/1hjffc8i.selenium-profile")
        #Assign the service to the driver and the options
        driver = webdriver.Firefox(service=service, options=opts)
        return driver


    def stablish_connection_and_initialize_variables(self):
        self.driver.get("https://www.ign.es/WebServiceTransformCoordinates/")

        self.type_of_coordenate_system = self.driver.find_element(By.ID, "sourceCRSCombo")
        self.decimal_switcher = self.driver.find_element(By.ID, "targetDegreeCombo")
        self.x_coordenate = self.driver.find_element(By.ID, "inputX")
        self.y_coordenate = self.driver.find_element(By.ID, "inputY")
        self.transform_button = self.driver.find_element(By.ID, "transformPoint")
        self.longitudeDegree = self.driver.find_element(By.ID, "outputLongitudeDegreeDec")
        self.longitudeOrientation = self.driver.find_element(By.ID, "outputLongitudeEO")
        self.latitudeDegree = self.driver.find_element(By.ID, "outputLatitudeDegreeDec")
        self.latitudeOrientation = self.driver.find_element(By.ID, "outputLatitudeNS")

    def set_up_site(self):
        self.type_of_coordenate_system.send_keys("UTM")
        self.type_of_coordenate_system.send_keys(Keys.RETURN)
        self.decimal_switcher.send_keys("G")
        self.decimal_switcher.send_keys(Keys.RETURN)

    def close_driver(self):
        self.driver.close()

    # Type x and y coordenates
    def type_new_coordenates(self, x: str, y: str):
        self.x_coordenate.clear()
        self.y_coordenate.clear()
        self.x_coordenate.send_keys(x)
        self.x_coordenate.send_keys(Keys.RETURN)
        self.y_coordenate.send_keys(y)
        self.y_coordenate.send_keys(Keys.RETURN)


    ## Wait function
    def process_data(self, x: str, y: str):
        if (x == "" or y == "" or x == None or y == None):
            return "", ""
        self.type_new_coordenates(x,y)
        self.transform_button.click()
        self.wait.until(lambda driver: self.element_has_text(self.longitudeDegree))
        return self.retrieve_data()

    def retrieve_data(self):
        longitude = float(self.longitudeDegree.get_attribute("value").replace(",","."))
        latitude = float(self.latitudeDegree.get_attribute("value").replace(",","."))
        if self.longitudeOrientation.get_attribute("value") == "E": 
            longitude = -longitude
            print(longitude)
        if self.latitudeOrientation.get_attribute("value") == "S": 
            latitude = -latitude
            print(latitude)

        return longitude, latitude

    def element_has_text(self, element):
        condition = element.get_attribute("value") != ""
        return condition


