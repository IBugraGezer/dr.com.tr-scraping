# -*- coding: utf-8 -*-

import os
from helpers import downloadImage, iri2uri, slugify
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
def getBookName(soup):
    pageTitle = soup.title.text
    bookName = pageTitle.split("|")[0]
    return bookName
    

def getCoverImageSrc(soup):
    imageCollapser = soup.find('div', {'class':'detail-slider-show'}).find('div')
    image = imageCollapser.findChild('img')
    return image['src']

def getDescriptionText(soup):
    textDiv = soup.find('div', {'class':'product-description-header section-cover mb-40 fs-3_5'})
    title = textDiv.findChild('h2', {'class':'standart-h2-title'})
    title.decompose()
    return textDiv.text

def getAuthorName(soup):
    authorLinkTag = soup.find('div', 'author').find('a')
    return authorLinkTag.text

def getAuthorUrl(soup):
    authorLinkTag = soup.find('div', 'author').find('a')
    return authorLinkTag['href']

def getCoverImage(url, bookName, pageNo):
    
    parsedFileName = os.path.basename(url).split(".")
    
    fileName = parsedFileName[0]
    extension = parsedFileName[1]
    
    
    pathToDownloadImage = "books/" + str(pageNo) + "/images/" + slugify(bookName) + "." + extension
    
    downloadImage(url, pathToDownloadImage)
    
    return pathToDownloadImage
    

def createSoup(url):
    try:
        page = urlopen(url)
    except UnicodeEncodeError:
        page = urlopen(iri2uri(url))
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

def getBookData(bookPageUrl, pageNo):
    print("-------------------")
    print("KİTAP ALINIYOR...")
    soup = createSoup(bookPageUrl)
    bookName = getBookName(soup)
    coverImageUrl = getCoverImageSrc(soup)
    coverImagePath = getCoverImage(coverImageUrl, bookName, pageNo)
    descriptionText = getDescriptionText(soup)
    authorName = getAuthorName(soup)
    authorUrl = getAuthorUrl(soup)
    
    print(bookName + " ALINDI")
    data = {
        'bookName':bookName.strip(), 
        'coverImageUrl':coverImageUrl.strip(),
        'coverImagePath':coverImagePath.strip(),
        'descriptionText':descriptionText.strip(),
        'authorName':authorName.strip(),
        'authorUrl':authorUrl.strip()
    }
    
    return data

def getProductLinksFromProductListPage(url):
    productListSoup = createSoup(url)
    
    productLinks = []
    
    productElements = productListSoup.find_all("div", {"class":"product-img"})
    
    for element in productElements:
        link = element.findChild('a')['href']
        productLinks.append("https://www.dr.com.tr" + link)
        
    return productLinks
    
