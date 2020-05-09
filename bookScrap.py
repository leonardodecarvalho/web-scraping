# Esse algoritmo coleta dados do site http://books.toscrape.com/ e cria uma planilha no excel com o nome, preço, nota,
# disponibilidade e genero.

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions as exc
import openpyxl as xl

# organizando a planilha do excel

wb = xl.Workbook() # cria uma nova planilha do excel no diretório atual
wb['Sheet'].title = 'Livros' # muda o titulo da aba para Livros
sheet = wb['Livros'] # a aba livros é a que esta atualmente aberta na planilha

# nome das colunas
sheet['A1'], sheet['B1'], sheet['C1'], sheet['D1'], sheet['E1'] = 'Nome', 'Preco', 'Disponivel', 'Genero', 'Nota (Max 5)'

with webdriver.Firefox() as driver:
	driver.get("http://books.toscrape.com/index.html") # acessa a loja de livros
	assert driver.title == "All products | Books to Scrape - Sandbox", "Titulo Diferente" # ve se o titulo do site é o correto, caso contrario
	# o programa para
	driver.implicitly_wait(5) # webdriver espera 5 segundos para a pagina carregar
	tags = driver.find_elements(By.CSS_SELECTOR, "li > a") # seleciona todas as categorias, por meio das tags <a> com pais <li>
	tags = tags[2:-2] # duas primeiras categorias (books e home, que contem as tags li e a) e a ultima, que dependendo da pagina pode conter no
	# final um botão com next para ser selecionado
	genero_link = [] # lista com os links para serem acessados
	genero_nome = [] # lista com os nomes das paginas para ser adicionado na coluna da planilha do excel
	for tag in tags:
		genero_link.append(tag.get_attribute('href')) # seleciona o link de referencia do atributo href e adiciona na lista genero_link
		genero_nome.append(tag.text) # seleciona o texto da tag a (nome do genero) e adiciona na lista genero_nome
	driver.implicitly_wait(5) # webdriver espera 5 segundos para carregar
	j = 2 # controle das linhas do excel
	for k, link in enumerate(genero_link):
		driver.get(link) # acessa o link do genero
		driver.implicitly_wait(5)
		while True:
			valor = []
			nomes_livros = driver.find_elements(By.CSS_SELECTOR, "h3 > a") # procura na pagina pelo nome dos livros
			precos_livros = driver.find_elements(By.CSS_SELECTOR, "div > p.price_color") # procura na pagina pelo preço deles
			disponivel = driver.find_elements(By.CSS_SELECTOR, "div > p.instock.availability") # procura na pagina se eles estao disponiveis
			notas = driver.find_elements(By.CSS_SELECTOR, "p.star-rating") # procura pela nota de cada livro na pagina
			for nota in notas:
				valor.append(nota.get_attribute('class')) # adiciona na lista as notas, utilizando a classe delas 
			driver.implicitly_wait(5)
			for i, nome in enumerate(nomes_livros):
				sheet['A'+str(j)].value = nomes_livros[i].text # adiciona embaixo da coluna Nome o nome do livro
				sheet['B'+str(j)].value = precos_livros[i].text # preco
				sheet['C'+str(j)].value = disponivel[i].text # disponibilidade
				sheet['D'+str(j)].value = genero_nome[k] # adiciona o genero, sendo o indice controlado pela variavel k
				sheet['E'+str(j)].value = valor[i][12:] # adiciona a nota, indo de "One" até "Five"
				j += 1 # adiciona no final do loop 1 na linha do excel para o proximo livro/preço/disponibilidade/genero serem incluidos
			driver.implicitly_wait(5)
			try:
				next_page = driver.find_element(By.CSS_SELECTOR, "li.next > a") # verifica se a pagina tem um botão de proximo no final dela,
				# já que elas só mostram no máximo 20 livros por página
				driver.get(next_page.get_attribute('href')) # vai para a próxima página do genero e o algoritmo volta para a estrutura while
			except exc.NoSuchElementException: # caso não tenha um botão de proximo, o loop é parado e o algoritmo livros na proxima pagina
			# de genero
				break
	wb.save('Selenium Livros.xlsx') # salva os dados no arquivo de excel "Selenium Livros"
