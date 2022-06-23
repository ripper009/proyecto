#Se utiliza pagina web para realizar pruebas de scraping, se recomienda realizar el funcionamiento en Jupyter notebook
#Este proyecto no tiene fines malisiosos, es un modelo de proyecto para la Universidad Privada Franz Tamayo en la materia de Segurudad informatica. 
#Se importan diferentes variables para poder realizar el pryecto
import requests
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import IPython
from IPython.display import Image
from IPython.core.display import HTML

#declaracion de variables y se establece la pagina donde se realizara el barrido

url_inicial='https://books.toscrape.com/index.html'
url_root='https://books.toscrape.com/index.html'

r=requests.get(url_inicial)

r.status_code=200

s= BeautifulSoup(r.text,'lxml')

lista_article=s.find_all('article', class_='product_pod')
links_libros=[x.find('h3').find('a').get('href') for x in lista_article]
links_libros=[urljoin(url_root,i) for i in links_libros]
links_libros


#funcion de obtener links
def get_url_items(soup,url):
    lista_article=soup.find_all('article', class_='product_pod')
    links_libros=[x.find('h3').find('a').get('href') for x in lista_article]
    links_libros=[urljoin(url,i) for i in links_libros]
    return links_libros

links_items=[]
i=0
while i <50:
    i+=1
    print(f'Estoy en la pagina {url_inicial}')
    r_pag=requests.get(url_inicial)
    s_p=BeautifulSoup(r_pag.text,'lxml')
    links=get_url_items(s_p, url_inicial)
    links_items.append(links) 
    next_a=s_p.select('li.next > a')
    if not next_a or not next_a[0].get('href'):
        break
    url_inicial = urljoin(url_inicial, next_a[0].get('href'))
    #links_items.append(links)

    list_scraper=[]
    for i in links_items:
        for j in i:
            list_scraper.append(j)
    len(list_scraper)

    #quedarse con un link para obtener elementos
uno=list_scraper[0]
r_item=requests.get(uno)
s_item=BeautifulSoup(r_item.text,'lxml')

#Obtencion de elementos

#titulo
titulo=s_item.find('h1').get_text(strip=True)
#precio
precio=s_item.find('p', class_='price_color').get_text(strip=True)
#buscar etiqueta hermana para obtener descripcion de producto
ancla_desc=s_item.find('div', id='product_description')
text_descripcion=ancla_desc.find_next_sibling('p').get_text(strip=True)
#imagen
src_img=s_item.find('div', class_='item active').find('img').get('src')
src_img=urljoin(url_root,src_img)
#requests.get(src_img).content
#Image(requests.get(src_img).content)

#Funcion para realizar el scraper de los componentes
def scraper_book(url):
    content_book={}
    r=requests.get(url)
    s_item=BeautifulSoup(r.text,'lxml')
    #se utiliza la variable de libro
    titulo=s_item.find('h1').get_text(strip=True)
    if titulo:
        content_book['Titulo']=titulo
    else:
        content_book['Titulo']=None
    # se utiliza la variable de precio
    precio=s_item.find('p', class_='price_color').get_text(strip=True)
    if precio:
        content_book['Precio']=precio
    else:
        content_book['Precio']=None
    #Se establece la descripcion del producto
    ancla_desc=s_item.find('div', id='product_description')
    if precio:
        content_book['Descripcion']=ancla_desc.find_next_sibling('p').get_text(strip=True)
    else:
        content_book['Descripcion']=None
    #Se obtiene imagen
    src_img=s_item.find('div', class_='item active').find('img').get('src')
    if src_img:
        content_book['Url_img']=urljoin(url_root,src_img)
    else:
        content_book['Url_img']=None
    return content_book

    #se muestra la lista
list_scraper=list_scraper[0:10]
datos_book=[]
for idx, i in enumerate(list_scraper):
        print('Se realiza el scraping de la pagina {idx}')
        datos_book.append(scraper_book(i))

#Se crea el catalogo
df_catalogo=pd.DataFrame(datos_book)
df_catalogo

#se usa imagen a traves de html


def path_html_img(url):
    return '<img src="'+url+'"width="60">'

df_catalogo['Vis_img']=df_catalogo['Url_img'].apply(lambda x : path_html_img(x))
df_catalogo

# Se llama al frame para generar un html
df_catalogo.to_html(escape=False, formatters=dict(Portada=path_html_img))

HTML(df_catalogo.to_html(escape=False, formatters=dict(Portada=path_html_img)))









