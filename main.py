from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from information import pw
from information import username

class InstaBot:
    """
    A class that represent a InstaBot

    Attributes
    ----------
    username : str
        the username of user
    password : str
        the password of user

    Methods
    -------
    get_unfollowers()
        Prints all the users that are on following list and do not follow back
    """
    def __init__(self, username, password):
        """
        Parameters
        ----------
        username : str
            The username of user
        password : str
            The password of user
        """

        self.username = username
        self.password = password

        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(2)

        #get username input element
        self.driver.find_element(
                by=By.XPATH,
                value="//input[@name=\"username\"]"
            ).send_keys(username)
        #get password input element
        self.driver.find_element(
                by=By.XPATH,
                value="//input[@name=\"password\"]"
            ).send_keys(password)
        #get login button element
        self.driver.find_element(
                by=By.XPATH,
                value='//button[@type="submit"]'
            ).click()

        sleep(5)
        #click on Save info button in pop up window
        #self.driver.find_element(by=By.XPATH, 
        #       value="//button[contains(text(), 'Save Info')]").click()
        #full xpath for saveinfo element
        self.driver.find_element(
                by=By.XPATH, 
                value="/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/\
                div[1]/div[2]/section/main/div/div/div/\
                section/div/button"
            ).click()
        
        
        sleep(2)
        #click on Not now button in pop up window for turn on notification
        self.driver.find_element(
                by=By.XPATH, 
                value="//button[contains(text(), 'Not Now')]"
            ).click()


    def get_unfollowers(self):
        """
        Prints all the users which are on following list that 
        do not follow back. Users eligible to unfollow.
        """

        sleep(3)
        #go to my profile
        self.driver.find_element(
                by=By.XPATH, 
                value="//a[contains(@href, '/{}')]".format(self.username)
            ).click()

        self.driver.implicitly_wait(3)

        #go to follwing
        self.driver.find_element(
                by=By.XPATH, 
                value="//a[contains(@href, '/{}/following')]"\
                .format(self.username)
            ).click()
        self.driver.implicitly_wait(3)

        #list of names that you follow
        following = self._get_names_following()

        self.driver.implicitly_wait(3)

        #go to followers
        self.driver.find_element(
            by=By.XPATH, 
            value="//a[contains(@href, '/{}/followers')]"\
                .format(self.username)
            ).click()
        self.driver.implicitly_wait(3)

        #list of names that follow you
        followers = self._get_names_followers()

        for_unfollow = [user for user in following if user not in followers]

        print(for_unfollow)

        
    def _get_names_following(self):
        """
        Returns a list of users that are on following list.
        """

        self.driver.implicitly_wait(3)
        #full xpath for scrollbox element
        scroll_box = self.driver.find_element(
                by=By.XPATH, 
                value="/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/\
                    div[2]/div/div/div[4]"
            )
        
        '''
        ignored_exceptions=(
            NoSuchElementException, StaleElementReferenceException
        )
        scroll_box = WebDriverWait(
            self.driver, 3, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.\
                presence_of_element_located((By.XPATH, path)
            )
        )
        '''
        #scrollbox
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            sleep(1.5)
            height = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
        
        links = scroll_box.find_elements(by=By.TAG_NAME, value='a')
        names = [name.text for name in links if name.text != '']

        sleep(2)
        
        # close button for following box
        # full xpath for close button(x) element
        self.driver.find_element(
                by=By.XPATH, 
                value="/html/body/div[5]/div[1]/div/div[2]/div/div/div/\
                    div/div[2]/div/div/div[1]/div/div[3]/div/button"           
            ).click()
        
        return names
    
    def _get_names_followers(self):
        """
        Returns a list of users that are on followers list.
        """
        
        self.driver.implicitly_wait(3)
        #full xpath for scrollbox element
        scroll_box = self.driver.find_element(
                by=By.XPATH, 
                value="/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/\
                    div[2]/div/div/div[3]"
            )
        
        #scrollbox
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            sleep(1.5)
            height = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
        
        links = scroll_box.find_elements(by=By.TAG_NAME, value='a')
        names = [name.text for name in links if name.text != '']

        sleep(2)
        
        # close button for followers box
        # full xpath for close button(x) element
        self.driver.find_element(
                by=By.XPATH, 
                value="/html/body/div[5]/div[1]/div/div[2]/div/div/div/\
                    div/div[2]/div/div/div[1]/div/div[3]/div/button"           
            ).click()
        
        return names


bot = InstaBot(username=username, password=pw)
bot.get_unfollowers()