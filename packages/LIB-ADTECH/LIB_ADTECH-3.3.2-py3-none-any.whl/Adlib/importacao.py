from Adlib.api import *
from Adlib.funcoes import *
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

tokenTelegram = '7502689321:AAHrPDp9Y-MsVhcTzh_OImoRZXJsOPNoNKk'
chat_id = '-794597825'

def importacaoVirtaus(virtaus: Chrome, filepath: Path, nomeBanco: str, enumBanco: EnumBanco, options: dict):
    
    portabilidade = options.get("portabilidade")
    layout = options.get("layout")

    while True:
        putRequestFunction(EnumStatus.IMPORTANDO, EnumProcesso.IMPORTACAO, enumBanco)
        try:
            virtaus.get('https://adpromotora.virtaus.com.br/portal/p/ad/pageworkflowview?processID=ImportacaoArquivoEsteira')
            sleep(10)
            try:
                alert = virtaus.switch_to.alert
                try:
                    alert.accept()
                except:
                    alert.dismiss()
            except:
                print('Carregando')
            sleep(5)
            iframe = virtaus.find_elements('tag name','iframe')[0]
            virtaus.switch_to.frame(iframe)

            # Banco
            clickarElemento(virtaus, '/html/body/div/form/div/div[1]/div[2]/div/div[1]/span/span[1]/span/ul/li/input').click()
            esperarElemento(virtaus, '/html/body/div/form/div/div[1]/div[2]/div/div[1]/span/span[1]/span/ul/li/input').send_keys(nomeBanco)
            sleep(5)
            esperarElemento(virtaus, '/html/body/div/form/div/div[1]/div[2]/div/div[1]/span/span[1]/span/ul/li/input').send_keys(Keys.ENTER)

            # Layout
            try:
                dropdown = esperarElemento(virtaus, '//*[@id="selectLayout"]')
                select = Select(dropdown)
                try:
                    select.select_by_visible_text(layout)
                except Exception as e:
                    print(f"Error selecting option: {e}")
            except:
                print(f"Input de Layout não encontrado")

            # Portabilidade
            try:
                dropdown = esperarElemento(virtaus, '//*[@id="selectPortabilidade"]')
                select = Select(dropdown)
                try:
                    select.select_by_visible_text(portabilidade)
                except Exception as e:
                    print(f"Error selecting option: {e}")
            except Exception as e:
                print(f"Error selecting option: {e}")
                print(f"Input de portabilidade não encontrado")

            virtaus.switch_to.default_content()          

            clickarElemento(virtaus, '//*[@id="tab-attachments"]/a/span').click()
            sleep(5)
            esperarElemento(virtaus, '//*[@id="lb-input-upload"]')
            
            virtaus.find_element('xpath','//*[@id="ecm-navigation-inputFile-clone"]').send_keys(str(filepath))
            sleep(3)
            
            # Upload arquivo
            clickarElemento(virtaus,'//*[@id="workflowActions"]/button[1]').click()
            sleep(3)

            elemento = esperarElemento(virtaus, '/html/body/div[1]/div[3]/div/div/div[2]/div/div/div/div[3]/div[1]/div/div[1]/span/a')
            numeroSolicitacao = elemento.text

            putTicket(numeroSolicitacao, EnumProcesso.IMPORTACAO, enumBanco)
            mensagem = f"Importação Efetuada: <b> {nomeBanco} - {numeroSolicitacao}</b>"

            mensagemTelegam(tokenTelegram, chat_id, mensagem)
            putRequestFunction(EnumStatus.LIGADO, EnumProcesso.IMPORTACAO, enumBanco)
            break

        except Exception as e:
            print(e)
            print('Erro ao tentar importar no Virtaus')
            putRequestFunction(EnumStatus.ERRO, EnumProcesso.IMPORTACAO, enumBanco)

