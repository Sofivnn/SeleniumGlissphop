import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# It opens the Chrome browser and maximizes the window.
wd = webdriver.Chrome(executable_path="chromedriver.exe")
wd.maximize_window()


def open_json():
    """
    It opens the file data.json, loads the data into a variable called data, and returns the data
    :return: A dictionary
    """
    f = open("data.json")
    data = json.load(f)
    return data


# --------------------------#
#     Création de compte    #
# --------------------------#
def create_account():
    """
    This function is used to create an account on the website
    """
    wd.get("https://www.glisshop.com/glisshop/creation-de-compte.html")
    email = wd.find_element(By.NAME, "email")
    passwrd = wd.find_element(By.NAME, "password")
    confPass = wd.find_element(By.NAME, "confirmPassword")
    y = open_json()
    for i in y["user_details"]:
        email.send_keys(i["mail"])
        passwrd.send_keys(i["password"])
        confPass.send_keys(i["ConfirmPass"])
    button_log = wd.find_element(By.CLASS_NAME, "btn_l1_quaternary")
    button_log.click()
    time.sleep(3)

    # ----------------------- assertion code -----------------------
    expectedURL = "https://www.glisshop.com/glisshop/creation-de-compte.html"
    assert expectedURL == wd.current_url
    print("expected URL is equals with currentURL")
    connection_page()


# --------------------------#
#         Connection        #
# --------------------------#
def connection_page():
    # A function that allows the user to connect to the website.
    wd.get("https://www.glisshop.com/identification/")
    email = wd.find_element(By.ID, "block2-login")
    passwd = wd.find_element(By.ID, "block2-password")
    y = open_json()
    for i in y["user_details"]:
        email.send_keys(i["mail"])
        passwd.send_keys(i["password"])
    button_log = wd.find_element(By.CLASS_NAME, "btn_l1_quaternary")
    button_log.click()
    time.sleep(3)
    cookies = wd.find_element(By.ID, "tarteaucitronPersonalize2")
    cookies.click()

    # ----------------------- assertion code -----------------------
    expectedURL = "https://www.glisshop.com/mon-compte/mon-compte.html"
    assert expectedURL == wd.current_url
    print("expected URL is equals with currentURL")


# --------------------------#
#        Déconnexion        #
# --------------------------#
def disconnect_page():
    connection_page()
    # Logging out the user.
    time.sleep(4)
    log_out = wd.find_element(By.XPATH, "//a[contains(text(),'Déconnexion')]")
    log_out.click()
    time.sleep(4)
    print(wd.current_url)


# --------------------------#
#    Recherche article      #
# --------------------------#
def search_bar_article(product):
    """
    This function takes a string as an argument, and searches for it in the search bar of the website.

    :param name: the name of the article you want to search for
    """
    wd.get("https://www.glisshop.com/")
    search_bar = wd.find_element(By.NAME, "searchText")
    search_bar.send_keys(product)
    submit = wd.find_element(By.CLASS_NAME, "btn_transparent")
    submit.click()
    time.sleep(4)
    url = wd.current_url
    assert product in url
    print(product, "is in", url)


def add_article():
    """
    It opens the website, clicks on the first product, and adds it to the cart
    """
    wd.get("https://www.glisshop.com/glisshop/resultat-de-recherche-produits.html?searchText=jones%20mtb")
    product = wd.find_element(By.CLASS_NAME, "df-card__main")
    product.click()
    time.sleep(2)
    wd.find_element(By.CSS_SELECTOR, '.btn.btn-quaternary.btn-lg.btn-block.btn-wrap.uppercase').click()


def show_cart():
    """
    The function show_cart() opens the cart page and clicks on the "My cart" button
    """
    add_article()
    time.sleep(4)
    wd.get("https://www.glisshop.com/glisshop/mon-panier.html")
    time.sleep(2)
    expectedURL = "https://www.glisshop.com/glisshop/mon-panier.html"
    assert expectedURL == wd.current_url
    print("expected URL is equals with currentURL")


def modify_account():
    connection_page()
    wd.get("https://www.glisshop.com/mon-compte/mes-informations.html")
    modify = wd.find_element(By.CLASS_NAME, 'btn.btn_l.btn_l1.btn_full')


def delete_article():
    show_cart()
    time.sleep(2)
    close = wd.find_element(By.XPATH,"//*[@id='content-column']/div/div[7]/div[1]/div/div[1]/div[3]/div/div[2]/table/tbody/tr/td/div/div/div[1]/div/div[2]/div/span/div/button")
    close.click()



