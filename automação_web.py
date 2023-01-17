
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd

#Passo 1: Transformar o selenium do chrome pro brave

driver_path = r"C:\Users\Dante\Documents\Python\chromedriver.exe"
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
navegador = webdriver.Chrome(executable_path=driver_path, options=option)


#Passo 2: Pegar a cotação do dólar

navegador.get("https://www.google.com/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_dolar = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cotacao_dolar)


#Passo 3: Pegar a cotação do euro

navegador.get("https://www.google.com/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cotacao_euro)


#Passo 4: Pegar a cotação do ouro

navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",", '.')
print(cotacao_ouro)


# Passo 5: importar a base de dados e atualizar a base

tabela = pd.read_excel("Produtos.xlsx")
print(tabela)

#Passo 6: Recalcular os preços

# atualizar a cotação

tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

print(tabela)

#preço de compra = cotação * preço original

tabela["Preço de Compra"] = tabela["Preço Original"] * tabela["Cotação"]

# preço de venda = preço de compra * margem

tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

# recalcular os preços

tabela["Preço de Venda"] = tabela["Preço de Venda"].map("R${:.5f}".format)
tabela["Preço Original"] = tabela["Preço Original"].map("R${:.5f}".format)
tabela["Cotação"] = tabela["Cotação"].map("R${:.5f}".format)
tabela["Preço de Compra"] = tabela["Preço de Compra"].map("R${:.5f}".format)

print(tabela)


# Passo 7: Exportar a base atualizada

tabela.to_excel("Produtos Novo.xlsx", index=False)