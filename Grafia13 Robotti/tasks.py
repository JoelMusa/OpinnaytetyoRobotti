from robocorp.tasks import task, teardown

from RPA.Browser.Selenium import Selenium
from RPA.Images import Images
from RPA.Desktop import Desktop
from RPA.Windows import Windows
from RPA.PDF import PDF
from fpdf import FPDF
from RPA.Tables import Tables

from PIL import Image


import time

import csv





#Muuttujat
työpöytä = Desktop()
selain = Selenium()
ikkuna = Windows()

global merkki
global kierros
kierros = 0


#Taskit alku
@task
def Kerää_tiedot():

    #Toiminnot

    #Avaa selain
    Avaa_selain("https://holvi.com/shop/grafia13/")


    #Kiellä keksit
    Kiellä_keksit()

    #Etsi ensimmäinen kokoelma
    Etsi_kokoelma()

    #Lopuksi sulje selaimet
    Sulje_selain()





#Määrittelyt alku

def Avaa_selain(url):
    selain.open_available_browser(url)
    #selain.set_window_size(1920, 1080)
    print('Selain auki')


def Kiellä_keksit():

    #selain.wait_until_element_is_visible(locator="id:onetrust-reject-all-handler")
    selain.click_element(locator="id:onetrust-reject-all-handler")
    print('Keksit kiinni')



def Talleta_tiedot():
            
        Teosnimi = selain.get_text('class:product-name.break-word')
        string = str(Teosnimi)

        #Matti Hintikan teoksen Ve’en edessä nimeä täytyi muokata PDF varten

        korjaus = string.replace('’', "'")
        string = korjaus
        korjaus = string.replace('–', '-')
        Teosnimi = korjaus
        print(Teosnimi)

        Kuvaus = selain.get_text('class:product-description.col-xs-12')
        string = str(Kuvaus)
        korjaus = string.replace('€', 'e')
        Kuvaus = korjaus


        print(Kuvaus)

        selain.set_screenshot_directory('Kuvat')

        #Tallennusfunktio


        kohde = selain.get_element_attribute('class:carousel-bgimage', 'style')
        kohde = kohde[23:-3]
        print(kohde)

        


        selain.go_to(kohde)

        selain.wait_until_element_is_visible('css:img')

        selain.screenshot('css:img', 'Taideteos.jpg')
        selain.go_back()

        Hinta = selain.get_text('class:product-price')
        
        string = str(Hinta)
        korjaus4 = string.replace('€', 'e')
        Hinta = korjaus4

        print(Hinta)
        
        ALV = selain.get_text('class=vat_notice.smallp')
        print(ALV)

        Tarjolla = selain.get_text('class:thincaps.product-item-stock')
        print(Tarjolla)
        print('\n')

        Päivämäärä = selain.get_element_attribute('class:carousel-bgimage', 'style')       
        Päivämäärä = 'Lisatty v/kk/pp '+Päivämäärä[67:77]

        global kuva
        kuva = "Taideteos.jpg"
        
        








        def Luo_PDF():

                global kierros
                
                print(kierros)

                pdf = FPDF()
                pdf.add_page()

                pdf.set_font('Arial', '', 12)
                    
                merkki = str(kierros)

                pdf.cell(200, 10, txt='Tekniset tiedot', ln=True)
                pdf.cell(200, 10, txt='Special characters: ä, ö', ln=True)
                pdf.cell(200, 10, txt='Kuvan nimi', ln=True)
                pdf.cell(200, 10, txt='Taideteos'+merkki+'.jpg', ln=True)
                pdf.cell(200, 10, txt='Teoksen tiedot', ln=True)
                pdf.cell(200, 10, txt=Teosnimi, ln=True)
                pdf.cell(200, 10, txt=Kuvaus, ln=True)
                pdf.cell(200, 10, txt=Päivämäärä, ln=True)
                pdf.cell(200, 10, txt=Hinta, ln=True)
                pdf.cell(200, 10, txt=ALV, ln=True)
                pdf.cell(200, 10, txt=Tarjolla, ln=True)
            
                tiedosto0 = 'Teostiedot'+merkki+'.pdf'
                pdf.output(tiedosto0)




                #CSV tiedoston luonti
                
                teksti0 = 'Taideteos'
                teksti1 = merkki
                teksti2 = '.jpg'

                sisältö0 = [teksti0+teksti1+teksti2]
                sisältö1 = [Teosnimi]
                sisältö2 = [Kuvaus]
                sisältö3 = [Päivämäärä]
                sisältö4 = [Hinta]
                sisältö5 = [ALV]
                sisältö6 = [Tarjolla]
                
                tiedosto1 = 'GrafiaTeos'+str(kierros)+'.csv'
                
                global tiedostonimi                
                tiedostonimi = tiedosto1

                header = ['File Name', 'Artwork Name', 'Description', 'Date', 'Price', 'VAT', 'Available']

                sisältö = [sisältö0, sisältö1, sisältö2, sisältö3, sisältö4, sisältö5, sisältö6]


                with open(tiedosto1, 'w', newline='') as tiedosto1:
                        kirjoittaja = csv.writer(tiedosto1, quoting=csv.QUOTE_ALL)
                        kirjoittaja.writerow(header)
                        kirjoittaja.writerow(sisältö)

                print(f"'CSV  {tiedosto1}' valmis")

                #Giga CSV?

                
                #Kuva JPG
                with Image.open(kuva) as img:

                    RGB = img.convert('RGB')

                    RGB.save('Taideteos'+merkki+'.jpg', format='JPEG')

                kierros+=1
        
        Luo_PDF()





           

def Avaa_kokoelma():
    teokset = selain.get_webelements(locator="class:store-item-image")
    loppuunyydyt = selain.get_webelements(locator="class:store-item-sold-out-banner-text")
    
    miinus = len(loppuunyydyt)

    kerta = 0
    kerta2 = 0
    
    pituus2 = len(teokset) - miinus
    pituus3 = len(teokset)

    while kerta < pituus2:
        klikkaa = teokset[kerta]
        selain.click_element(klikkaa)
        Talleta_tiedot()
        selain.go_back()
        kerta += 1

    while kerta2 < miinus:
        klikkaa = loppuunyydyt[kerta2]
        selain.click_element(klikkaa)
        Talleta_tiedot()
        selain.go_back()
        kerta2 += 1

        if kerta2 == miinus:
            break

    loppuunyydyt = 0
    kerta = 0
    kerta2 = 0



def Etsi_kokoelma():


    kokoelma = selain.get_webelements(locator="class:store-navigation-subsection-name")
    print(len(kokoelma))

    pituus = len(kokoelma)
    kohta = 0
    

    while kohta < pituus:
    
        selain.go_to("https://holvi.com/shop/grafia13/")
        kokoelma = selain.get_webelements(locator="class:store-navigation-subsection-name")
        paina = kokoelma[kohta]
        selain.click_element(paina)


        kohta+=1
        Avaa_kokoelma()
        selain.go_back()







    






def Sulje_selain():
    selain.close_all_browsers()
    print('Selaimet suljettu')


#Kannattaa lopuksi sulkea Task managerista käytetyt selaimet prosesseista, jotka jäävät mahdollisesti päälle ja hidastavat konetta!

    
