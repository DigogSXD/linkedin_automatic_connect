import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# --- CONFIGURAÇÃO ---
options = Options()
options.add_argument("--log-level=3") 
driver = webdriver.Chrome(options=options)

# QUANTAS PESSOAS VOCÊ QUER ADICIONAR?
META_CONEXOES = 50 

try:
    print("=== MODO RECARGA AUTOMÁTICA ===")
    driver.get("https://www.linkedin.com/login")
    input("Faça o login e pressione ENTER aqui para começar...")

    driver.get("https://www.linkedin.com/mynetwork/grow/")
    time.sleep(3) # Espera inicial para carregar a página

    conectados = 0
    
    # Loop principal: Continua rodando até bater a meta
    while conectados < META_CONEXOES:
        
        # 1. Procura todos os botões 'Conectar' visíveis AGORA
        xpath_botao = "//button[.//span[text()='Conectar']]"
        botoes = driver.find_elements(By.XPATH, xpath_botao)
        
        print(f"--> Encontrei {len(botoes)} botões na tela. Processando...")

        # Se não achou nenhum botão na tela, ROLA A PÁGINA para carregar mais
        if len(botoes) == 0:
            print("Sem botões visíveis. Rolando para baixo para carregar mais...")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3) # Tempo para o LinkedIn carregar os novos perfis
            continue # Volta para o início do loop para buscar de novo

        # 2. Clica nos botões encontrados
        for btn in botoes:
            if conectados >= META_CONEXOES:
                break
            
            try:
                # Clique JS (Rápido)
                driver.execute_script("arguments[0].click();", btn)
                conectados += 1
                print(f"[{conectados}/{META_CONEXOES}] Conectado!")

                # Verificação ultra-rápida de popup (Enviar sem nota) via JS
                # Isso fecha janelas que atrapalham o fluxo
                driver.execute_script(
                    """
                    var btn = document.evaluate("//button[.//span[text()='Enviar sem nota'] or .//span[text()='Enviar']]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (btn) { btn.click(); }
                    """
                )
                
                # Pausa mínima para não travar o navegador (0.2 a 0.5s)
                time.sleep(0.3)

            except Exception:
                # Se o botão sumiu ou deu erro (StaleElement), apenas ignora e vai pro próximo
                pass

        # 3. Depois de clicar em todos da tela atual, rola para baixo para pegar o próximo lote
        print("Lote finalizado. Buscando mais...")
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2) # Espera carregar o novo lote

except Exception as e:
    print(f"Erro: {e}")

finally:
    print(f"FIM! Total de conexões disparadas: {conectados}")
