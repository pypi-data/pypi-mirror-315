from selenium.webdriver import Chrome
from Adlib.funcoes import *
from Adlib.api import *
from time import sleep


def assumirSolicitacao(virtaus: Chrome, nomeFerramenta: str, tipoFiltro: str = "Atendimento | EmissaoDeNovaSenhaLoginExterno", HORA_FINALIZACAO: str = "19:00"):
    try:
        while True:
            try:
                virtaus.get("https://adpromotora.virtaus.com.br/portal/p/ad/pagecentraltask")

                qntBotoes = len(esperarElementos(virtaus, '//*[@id="centralTaskMenu"]/li'))
                idxBtn = qntBotoes - 1
                try:
                    # Clica em "Tarefas em Pool: Grupo"
                    clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/a').click()
                except Exception as e:
                    print(e)

                # Seleciona o filtro de "Emissão De Nova Senha Login Externo"
                clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/ul//a[contains(text(), "{tipoFiltro}")]').click()

                # Busca pelo nome da ferramenta
                esperarElemento(virtaus, '//*[@id="inputSearchFilter"]').send_keys(nomeFerramenta)

                # Clica no primeira item da lista de solicitações
                clickarElemento(virtaus, f"//td[contains(@title, '{nomeFerramenta}')]").click()
                break

            except Exception as e:

                agora = datetime.datetime.now()
                hora = agora.strftime("%H:%M")
                print(f"Não há solicitações do banco {nomeFerramenta.title()} no momento {hora}")

                if HORA_FINALIZACAO == hora:
                    putRequestFunction(EnumStatus.DESLIGADO, EnumProcesso.RESET, EnumBanco.DIGIO)
                    sys.exit()

                sleep(30)
        
        try:
            print("Assumindo Tarefa")
            # Clica em Assumir Tarefa e vai para o menu de Cadastro de usuário
            clickarElemento(virtaus, '//*[@id="workflowActions"]/button[1]').click()
        
        except:
            print("Erro ao assumir tarefa")
    except:
        pass