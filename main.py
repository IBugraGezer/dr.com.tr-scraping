from dr import *
from helpers import *
import urllib

currentPage = int(input("Şu sayfadan itibaren işlem yapılsın:"))
for pageNo in range(currentPage,555):
    
    path = "books/" + str(pageNo)
    if not os.path.exists(path):
        os.makedirs(path)
        os.makedirs(path + "/images")
    jsonFilePath = "books/" + str(pageNo) + "/data.json"
    file = open(jsonFilePath, "w+")
    file.write("[\n")
    file.close()
    url = "https://www.dr.com.tr/kategori/Kitap/Edebiyat/Roman/grupno=00211?ShowNotForSale=True&Page=" + str(pageNo) 

    print("****************")
    print("YENİ URLYE GEÇİLDİ")
    print(url)
    print("SAYFA NO:", pageNo)
    print("****************")
    
    productLinks = getProductLinksFromProductListPage(url)   

    print("LİNKLER ALINDI")

    indent = 4



    print("PARANTEZ AÇILDI")

    for productLink in productLinks:
        try:
            data = getBookData(productLink, pageNo)
            dumpJsonToFile(data, indent, "books/" + str(pageNo))
            print("sayfa: " + str(pageNo))
        except urllib.error.URLError:
            errorLog("urllib.error.URLError", productLink, pageNo)
            continue
        except:
            errorLog("error", productLink, pageNo)
            continue
        
    file = open(jsonFilePath, "a")
    file.write("]")
    file.close()
