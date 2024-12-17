from functools import wraps
from selenium import webdriver
from Adlib.funcoes import esperarElemento, clickarElemento, getCredenciais, setupDriver
from selenium.webdriver.common.keys import Keys
from time import sleep


def login_decorator(func):

    @wraps(func)
    def wrapper(driver: webdriver.Chrome, usuario: str, senha: str, *args, **kwargs):
        try:
            func(driver, usuario, senha, *args, **kwargs)
        except Exception as e:
            print(f"Erro ao realizar login: {func.__name__}")
            print(e)
    return wrapper


@login_decorator
def loginDigio(digio: webdriver.Chrome, usuario: str, senha: str):

    digio.get("https://funcaoconsig.digio.com.br/FIMENU/Login/AC.UI.LOGIN.aspx")

    esperarElemento(digio, "//*[@id='EUsuario_CAMPO']").send_keys(usuario)
    esperarElemento(digio, "//*[@id='ESenha_CAMPO']").send_keys(senha)
    clickarElemento(digio, '//*[@id="lnkEntrar"]').click()
    clickarElemento(digio, '//*[@id="ctl00_ContentPlaceHolder1_DataListMenu_ctl00_LinkButton2"]').click()


@login_decorator
def loginBlip(blip: webdriver.Chrome, usuario: str, senha: str):

    blip.get('https://takegarage-7ah6a.desk.blip.ai/')
    sleep(5)
    shadow_host = blip.find_element('css selector', '#email-input')
    shadow_root = blip.execute_script("return arguments[0].shadowRoot", shadow_host)
    
    shadow_root.find_element('class name', 'input__container__text').send_keys(usuario)
    blip.find_element('css selector', ".input__container__text").send_keys(senha + Keys.ENTER + Keys.ENTER)

    sleep(5)


@login_decorator
def loginFacta(facta: webdriver.Chrome, usuario: str, senha: str):

    facta.get('https://desenv.facta.com.br/sistemaNovo/login.php')
    
    esperarElemento(facta, '//*[@id="login"]').send_keys(usuario)
    esperarElemento(facta, '//*[@id="senha"]').send_keys(senha)

    esperarElemento(facta,'//*[@id="btnLogin"]').click()

    sleep(5)


@login_decorator
def loginMargem(acces: webdriver.Chrome, usuario: str, senha: str):
    acces.get('https://adpromotora.promobank.com.br/') 

    loginElementmargem = esperarElemento(acces, '//*[@id="inputUsuario"]').send_keys(usuario)
    passwordElementmargem = esperarElemento(acces, '//*[@id="passField"]').send_keys(senha + Keys.ENTER)
    sleep(5)


@login_decorator
def loginBanrisul(banrisul: webdriver.Chrome, usuario, senha):

    banrisul.get('https://desenv.banrisul.com.br/sistemaNovo/login.php')
 
    esperarElemento(banrisul, '//*[@id="usuario"]').send_keys(usuario)
    esperarElemento(banrisul, '//*[@id="senha"]').send_keys(senha)

    esperarElemento(banrisul,'//*[@id="btnLogin"]').click()
    sleep(5)


@login_decorator
def loginCashCard(cashcard: webdriver.Chrome, user: str, senha: str):
    
    cashcard.get(f"http://18.217.139.90/WebAppBPOCartao/Login/ICLogin?ReturnUrl=%2FWebAppBPOCartao%2FPages%2FRelatorios%2FICRLProducaoAnalitico")
    
    esperarElemento(cashcard, '//*[@id="txtUsuario_CAMPO"]').send_keys(user)
    esperarElemento(cashcard, '//*[@id="txtSenha_CAMPO"]').send_keys(senha)

    esperarElemento(cashcard, '//*[@id="bbConfirmar"]').click()

    sleep(5)

if __name__=="__main__":

    driver = setupDriver(r"C:\Users\dannilo.costa\Documents\chromedriver.exe")

    user, senha = getCredenciais(232)
    loginBlip(driver, user, senha)