import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# It opens the Chrome browser and maximizes the window.
wd = webdriver.Chrome(executable_path="chromedriver.exe")
wd.maximize_window()


def skip_cookie():
    cookies = wd.find_element(By.ID, "tarteaucitronPersonalize2")
    return cookies.click()


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
    try:
        y = open_json()
        for i in y["user_details"]:
            email.send_keys(i["mail"])
            passwrd.send_keys(i["password"])
            confPass.send_keys(i["ConfirmPass"])
        button_log = wd.find_element(By.CLASS_NAME, "btn_l1_quaternary")
        button_log.click()
    except:
        print("Impossible de crée le compte")
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
    try:
        y = open_json()
        for i in y["user_details"]:
            email.send_keys(i["mail"])
            passwd.send_keys(i["password"])
        button_log = wd.find_element(By.CLASS_NAME, "btn_l1_quaternary")
        button_log.click()
    except:
        print("impossible de se connecter")
    time.sleep(3)
    skip_cookie()
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
    time.sleep(2)
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
    time.sleep(2)
    url = wd.current_url
    assert product in url
    print(product, "is in", url)
    skip_cookie()


    
# --------------------------#
#      Ajouter article      #
# --------------------------#
def add_article():
    """
    It opens the website, clicks on the first product, and adds it to the cart
    """
    wd.get("https://www.glisshop.com/glisshop/resultat-de-recherche-produits.html?searchText=jones%20mtb")
    product = wd.find_element(By.CLASS_NAME, "df-card__main")
    product.click()
    time.sleep(4)
    skip_cookie()
    element = wd.find_element(By.XPATH, '//button[ @data-ng-click="addShippingCategoriesProduct()" ]')
    wd.execute_script("arguments[0].click();", element)

    
   

# --------------------------#
#        Voir article       #
# --------------------------#
def show_cart():
    """
    The function show_cart() opens the cart page and clicks on the "My cart" button
    """
    add_article()
    time.sleep(4)
    badge_cart = wd.find_element(By.XPATH, '//span[@class="badge"]')
    if badge_cart.text < str(1):
        print("Le panier est vide")
    else:
        element = wd.find_element(By.XPATH, '//button[@data-ng-click="continueShopping()"]')
        wd.execute_script("arguments[0].click();", element)
        cart = wd.find_element(By.XPATH, '//a[@class="dropdown-toggle header_link fake-link"]')
        wd.execute_script("arguments[0].click();", cart)



# --------------------------#
#        Delete article     #
# --------------------------#
def delete_article():
    """
    It clicks on the "delete" button of the first article in the cart, then checks if the cart is empty
    """
    show_cart()
    time.sleep(3)
    number_el = wd.find_element(By.XPATH, '//button[@class="fake-link btn-reset"]')
    wd.execute_script("arguments[0].click();", number_el)
    time.sleep(2)
    badge_cart = wd.find_element(By.XPATH, '//span[@class="badge"]')
    print(badge_cart.text)
    if badge_cart.text > str(0):
        print("Le panier n'est vide")
    else:
        print("vide")


# --------------------------#
#        Modify article     #
# --------------------------#
def modify():
    """
    This function is used to modify the user's information
    """
    connection_page()
    info = wd.find_element(By.XPATH, '//a[@title="Mes informations"]')
    wd.execute_script("arguments[0].click();", info)
    button_modify = wd.find_element(By.XPATH, '//button[@data-ng-click="openEdit()"]')
    wd.execute_script("arguments[0].click();", button_modify)
    name = wd.find_element(By.ID, "rbs-user-firstName")
    lastname = wd.find_element(By.ID, "rbs-user-lastName")
    phone = wd.find_element(By.XPATH, '//input[@data-ng-model="rawNumber"]')
    birth = wd.find_element(By.ID, "rbs-user-birthDate")
    pseudo = wd.find_element(By.ID, "rbs-user-pseudonym")
    try:
        y = open_json()
        for i in y["user_details"]:
            name.send_keys(i["Name"])
            lastname.send_keys(i["Lastname"])
            phone.send_keys(i["phone"])
            birth.send_keys(i["birth"])
            pseudo.send_keys(i["pseudo"])
        return_modify = wd.find_element(By.XPATH, '//button[@data-ng-click="saveAccount()"]')
        wd.execute_script("arguments[0].click();", return_modify)
    except:
        print("Impossible de Modifier les donnée")


#connection_page()
#disconnect_page()
#delete_article()
#modify()
#create_account()
#add_article()
#search_bar_article()
