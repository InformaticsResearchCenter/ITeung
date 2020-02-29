from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from oauth2client.service_account import ServiceAccountCredentials
from lib import prodi
import face_recognition
import cv2
import numpy as np
#import gspread
import os

import random
from time import sleep
from googletrans import Translator

class Chatbot(object):
    def setProfile(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-data-dir=./user_data')
        self.driver = webdriver.Chrome(chrome_options=self.options)
    
    def openBrowser(self):
        self.setProfile()
        self.driver.get("https://web.whatsapp.com/")
        self.waitLogin()

    def splitString(self, string):
        li = list(string.split(" "))
        return li

    def waitLogin(self):
        self.target = '"_3RWII"'
        self.x_arg = '//div[contains(@class, ' + self.target + ')]'
        self.wait = WebDriverWait(self.driver, 600)
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.x_arg)))

    def typeAndSendMessage(self, message):
        self.getMessage_target = self.driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
        self.getMessage_target.send_keys(message)
        self.sendbutton = self.driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
        self.sendbutton.click()

    def deleteMessage(self):
        self.driver.find_elements_by_class_name('_3j8Pd')[-1].click()
        sleep(1)

        value_name = self.driver.find_elements_by_class_name('_3zy-4')
        sleep(1)

        if 'Exit group' in value_name[4].text:
            print('group')
            value_name[3].click()
            self.driver.find_elements_by_class_name('_2eK7W')[1].click()
        else:
            print('personal')
            value_name[4].click()
            self.driver.find_elements_by_class_name('_2eK7W')[1].click()

    def cekAndSendMessage(self):
        try:
            try:
                self.chat = self.driver.find_elements_by_class_name("P6z4j")[0]
                self.chat.click()
                self.chat.click()
                self.chat.click()
            except:
                print('skip data')

            sleep(0.5)

            stringMessage = self.driver.find_elements_by_xpath('(.//span)')[-11].text
            stringMessageLower = stringMessage.lower()
            message = self.splitString(stringMessageLower)

            numberPhone = self.driver.find_elements_by_class_name("ZObjg")[-1].text

            aliasName = self.driver.find_elements_by_class_name("_1F9Ap")[-1].text

            data = []
            data.append(numberPhone)
            data.append(aliasName)
            data.append(message)

            getNumberPhone = data[0]
            getAliasName = data[1]
            self.getMessage = data[2]

            if "wanda" in self.getMessage:
                list_jawaban = ["iyaaaaaa :-D", "iya, kenapa?", "iya, butuh bantuan?"]
                jawaban = random.choice(list_jawaban)
                self.typeAndSendMessage(jawaban)

            if "wanda" in self.getMessage and "perkenalkan" in self.getMessage or "kenalan" in self.getMessage:
                self.sendPictureWithoutPhoneNumber()
                self.typeAndSendMessage("Halo, perkenalkan Nama aku wanda, Aku seorang mahasiswi poltekpos, Salam kenal ya")

            if "terima" in self.getMessage and "kasih" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("sama sama :-)")

            if "nuhun" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("sami sami :-D")

            if "makasih" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("yoi, cama-cama")

            if "pintar" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("Oo, iya dong, makasih atas pujiannya")

            if "ngeselin" in self.getMessage or "kesal" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("hmm, maaf ya kalo wanda ada salah sama kamu")

            if "beliin" in self.getMessage and "rokok" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("bukannya wanda gak mau beliin, tapi rokok itu gak baik buat kesehatan, lebih baik rokoknya diganti sama wanda aja gimana?")

            if "centil" in self.getMessage or "nakal" in self.getMessage and "wanda" in self.getMessage:
                lst_jawaban = ["emang kenapa? ada masalah?", "trus? masalah buat kamu?"]
                answer = random.choice(lst_jawaban)
                self.typeAndSendMessage(answer)

            if "sidang" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("ok, tunggu sebentar ya :-D")
                getIndex = self.getMessage.index("sidang")
                try:
                    jadwal = prodi.cekJadwalSidang(self.getMessage[getIndex+1])
                    jadwal.pop(0)
                    jadwal.pop(0)

                    if jadwal == "no_pilihan":
                        self.typeAndSendMessage("pilihan salah")
                    else:
                        for i in jadwal:
                            self.typeAndSendMessage("NPM: "+i[0]+", Nama: "+i[1]+", Penguji utama: "+i[2]+", Penguji pendamping: "+i[3]+", Jam: "+i[5]+", Lokasi: "+i[6])
                except:
                    self.typeAndSendMessage("jadwal sidang "+self.getMessage[getIndex+1]+" tidak ada")

            if "nilai" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("sip, ti antosan sakeudap :-)")
                getIndex = self.getMessage.index("nilai")

                npm = self.getMessage[getIndex+1]
                pertemuan = self.getMessage[getIndex+2]
                hasil = prodi.getNilaiMahasiswa(npm, pertemuan)

                if hasil == "invalid":
                    self.typeAndSendMessage("maaf npmnya ga wanda temuin :'-(, mungkin npmnya salah, coba dicek lagi deh :-)")
                elif hasil == "pertemuan_invalid":
                    self.typeAndSendMessage("format salah, contoh: pertemuan1")
                else:
                    self.typeAndSendMessage("NPM: "+npm+", Nama: "+hasil[1]+", Nilai: "+hasil[0]+", Nilai rata-rata: "+hasil[2])


            if "love" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("love you too <3")
            
            if "aku" in self.getMessage and "cantik" in self.getMessage and "wanda" in self.getMessage:
                ihuy = [
                    "iya kamu cantik bangeett deehh (^o^)", "iya kamu cantik tapi masih cantikan akuu hehehe"
                    ,"iyaa zheyengg"
                ]
                love = random.choice(ihuy)
                self.typeAndSendMessage(love)
            if "kamu" in self.getMessage and "cantik" in self.getMessage and "wanda" in self.getMessage:
                ayey = [
                    "terima kasihh kakak yang maniss (/◕ヮ◕)/","awww terima kasiihh (≧▽≦)","love you kak (ㆁωㆁ*)"
                ]
                loveu = random.choice(ayey)
                self.typeAndSendMessage(loveu)
                
            if "bioskop" in self.getMessage:
                self.movieSchedule(self.getMessage)

            if "perhutani" in self.getMessage:
                self.perhutani()

            if "gmaps" in self.getMessage:
                self.getMessage.pop(0)
                desti2 = self.listToString(self.getMessage)
                self.gmaps(desti2)

            if "foto" in self.getMessage:
                sleep(1)
                name = self.getName()
                sleep(1)
                self.retrievePicture()
                sleep(1)
                self.renamePicture(name)
                sleep(1)
                self.sendPictureWithPhoneNumber(self.getMessage[1], name)
                sleep(1)
                self.deletePicture()
                sleep(1)

            if "gambar" in self.getMessage:
                sleep(1)
                name = self.getName()
                sleep(1)
                self.retrievePicture()
                sleep(1)
                self.renamePicture(name)
                sleep(1)
                objectnames = self.listToString(self.loadYolo(self.cocoNamesLoad(), name))
                sleep(1)
                self.deletePicture()
                sleep(1)
                print(objectnames)
                if objectnames != "":
                    self.typeAndSendMessage(
                        "Digambar yang kamu kirim wanda lihat ada " + objectnames)
                else:
                    self.typeAndSendMessage(
                        "ihhhh, wanda gak tau ada apa aja digambar yang kamu kirimin, maaf ya, coba kirimin gambar yang lebih jelas")

            if "face" in self.getMessage:
                sleep(1)
                name = self.getName()
                sleep(1)
                self.retrievePicture()
                sleep(1)
                self.renamePicture(name)
                sleep(1)
                faceNames = self.listToString(self.faceRecognition(name))
                sleep(1)
                self.deletePicture()
                sleep(1)
                if faceNames != "":
                    self.typeAndSendMessage("Difoto yang kamu kirimin wanda bisa menemukan foto kak " + faceNames)
                else:
                    self.typeAndSendMessage("Foto siapa ntuh, gak kenal ih")
                sleep(1)

            # bully #
            rage_sentence = ["bodoh", "jelek", "anjing", "bangsat", "bego", "tolol", "idiot", "bau"] #kata yg diperkirakan dimasukkan
            if any(x in self.getMessage for x in rage_sentence) and "wanda" in self.getMessage: #cek kata
                balesan = [
                    "Ya allah Tolongin Baim Ya allah (ಥ﹏ಥ)", "Kok kamu jahat bIiinNNNnngggGGHHiitzzz sich sama aku zheyeng ('・ω・')",
                    "Tak ada manusia yang terlahir \ndi download \n(´-﹏-`；)", "Ya Maaf (ಥ﹏ಥ)", "sudah cukup rhoma (｡ŏ﹏ŏ)",
                    "rangga yang kamu lakukan ke saya itu \n JAHAT \n(;´༎ຶД༎ຶ`)", "Kamu belom pernah liat aku marah yaaahhh!!! (；･`д･´)",
                    "Bumi ini aja aku pijak \napalagi kepala kau \n(；･`д･´)"
                ]
                marah = random.choice(balesan)
                self.typeAndSendMessage(marah)

            #formal
            if "selamat" in self.getMessage and "siang" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("iya, selamat siang :-)")
            if "selamat" in self.getMessage and "sore" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("iya, selamat sore :-)")
            if "selamat" in self.getMessage and "malam" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("iya, selamat malam :-)")
            if "selamat" in self.getMessage and "pagi" in self.getMessage and "wanda" in self.getMessage:
                self.typeAndSendMessage("iya, selamat pagi :-)")

            # Joke #
            joke_sentence = ["ngelucu", "ngelawak", "ngejoke", "ngereceh"] #kata yg diperkirakan dimasukkan
            if any(x in self.getMessage for x in joke_sentence) and "wanda" in self.getMessage: #cek kata
                list_joke = [
                "Sahabat dekat biasanya akan mengajak makan kepiting bareng, karena sahabat yang dekat adalah sahabat a crab :)",
                "Rombongan bebek lagi nyebrang \nTrus ada satu bebek yang ketabrak motor \nBebek 1: Kamu gpp? \nBebek 2: Aku bebek aja kok :)",
                "Kalo semua hal harus dipikirkan masak-masak, gimana nasib orang-orang yg ngga bisa masak :(",
                "Bang peseng es campurnya satu, tapi dipisah ya bang. Soalnya aku khawatir nggak bisa bedain mana yang tulus dan mana yg modus :)",
                "Pembeli: Bang, ngapain ngobrol sama martabak? \nPenjual: Kata pembelinya, martabaknya jgn dikacangin :)",
                "Pembeli: Mbak, beli es tehnya \nPenjual: Manis gak? \nPembeli: Gak usah manis-manis, yg penting setia dan mau menerima saya apa adanya :)",
                "Kalo ketemu begal di jalan, jgn takut. Kasi balsem aja, karena balsem bisa menghilangkan begal-begal :)",
                "Kalo bercanda jgn suka kelewatan, soalnya kalo kelewatan ntar lo mesti muter balik :)",
                "Jalan sama gebetan pake flat shoes, ditengah jalan ketemu mantannya dia, trus mereka ngobrol, aku dan sepatuku gak ada hak :')",
                "Cewek itu makhluk kuat, listrik aja dipake dibibir :(",
                "Kunci rumah gue hilang, mau masuk gak bisa. Gue cari dimana-mana gak ketemu. Akhirnya gue ambil napas panjang dan istigfar, eh pintunya kebuka. Baru inget kalo ternyata kuncinya sabar :')",
                "Pray for Banten, ibukotanya di serang :')",
                "Aku barusan ke kantor polisi bikin surat kehilangan, tp ditolak. Aku bilangnya aku kehilangan kamu :("
                ]
                joke = random.choice(list_joke) #milih random
                self.typeAndSendMessage(joke)

            # santuy #
            # if "salam" in self.getMessage and "wanda" in self.getMessage:
            #     self.typeAndSendMessage("assalamualaikum")
            #
            # if "assalamualaikum" in self.getMessage and "wanda" in self.getMessage:
            #     self.typeAndSendMessage("waalaikumsalam")
            #
            # if "gimana kabarmu?" in self.getMessage and "wanda" in self.getMessage:
            #     self.typeAndSendMessage("Saya baik-baik saja kok kak :-)")
            #
            # if "siapa yang menciptakan kamu?" in self.getMessage and "wanda" in self.getMessage:
            #     self.typeAndSendMessage("Tim IRC kakak, mereka hebat-hebat makanya sekarang wanda menjadi pintar :-)")
            #
            # if "aku cape" in self.getMessage and "wanda" in self.getMessage:
            #     self.typeAndSendMessage("jangan lupa makan dan istrahat ya kakak :-)")
            #
            # if "sampurasun" in self.getMessage and "wanda" in self.getMessage:
            #     self.typeAndSendMessage("Rampes")

            #teka-teki#
            teka_teki = ["teka-teki", "main"]
            if any(x in self.getMessage for x in teka_teki) and "wanda" in self.getMessage: #cek kata
                list_tekateki = [
                    "Ade ray kalau kentut bunyinya gimana? \n Brotot, brotot, brottott " , 
                    "Sandal apa yang paling enak di dunia? \n Sandal terasi", 
                    "Apa perbedaan aksi dengan demo? \n Kalo aksi rodanya empat kalo demo rodanya tiga",
                    "Pintu apa yang didorong nggak bakalan pernah bisa terbuka? \n Pintu yang ada tulisannya geser",
                    "Belut apa yg paling bahaya? \n belut-ang banyak ental bangklut",
                    "Kebo apa yg bikin kita lelah? \n kebogor jalan kaki",
                    "Ada 5 orang yang berjalan dibawah 1 payung kecil tapi anehnya tidak seorang pun yang kehujanan, kenapa? \n Karena tidak hujan",
                    "Bebek apa yang jalannya muter ke kiri terus? \n Bebek dikunci stang",
                    "Kaki seribu kalo belok kiri kakinya berapa? \n Tetep 1000, karena belok kiri jalan terus",
                    "Tamunya sudah masuk, malah yang punya diluar, apa? \n Tukang becak",
                    "Kentang apa yang paling dingin? \n KENTANGkuban perahu pada malam hari",
                    "Tukang apa yang setiap dipanggil pasti bakal menengok keatas? \n Tukang gali sumur",
                    "Tivi apa yang bisa berenang? \n TIVIkir vikir sih ikan",
                    "Tukang apa yang walaupun untung rugi tetap tepuk tangan? \n Tukang abu gosok",
                    "Aku ada diantara surga dan neraka. Siapakah aku? \n Dan",
                    "Aku adalah gelar yang tidak pas apabila diberikan kepada orang yang hidup. Gelar apakah aku? \n Gelar almarhum",
                    "Benda apa yang jika dipotong pasti nyambung lagi. Benda apakah itu? \n air",
                    "Masuk tanda seru dan keluar tanda tanya. Apakah itu? \n Ngupil",
                ]
                tekateki = random.choice(list_tekateki)
                self.typeAndSendMessage(tekateki)

            # hiburan
            if "wanda" in self.getMessage and "hibur" in self.getMessage or "hiburan" in self.getMessage:
                self.typeAndSendMessage("Boleh, mau lihat wanda ngedance atau nyanyi?")

            if "wanda" in self.getMessage and "ngedance" in self.getMessage or "dance" in self.getMessage or "nari" in self.getMessage:
                self.typeAndSendMessage("tunggu sebentar ya, wanda rekaman dulu")
                self.sendVideoWithoutPhoneNumber()

            if "wanda" in self.getMessage and "nyanyi" in self.getMessage or "menyanyi" in self.getMessage:
                self.typeAndSendMessage("tunggu sebentar ya, wanda rekaman dulu")
                self.sendVideoWithoutPhoneNumber()

            if "wanda" in self.getMessage and "gaya" in self.getMessage and "imutnya" in self.getMessage:
                self.typeAndSendMessage("bentar ya, rekaman dulu")
                self.sendVideoWithoutPhoneNumber()

            # gombalan #
            gombalan = ["gombal", "rayu", "baper", "gombalin", "baperin", "gombalan", "rayuan"] #kata yg diperkirakan dimasukkan
            if any(x in self.getMessage for x in gombalan) and "wanda" in self.getMessage: #cek kata
                list_gombal = [
                    "Sedang apa? Hari ini jika sehat berkenan lebih lama bersemayam di tubuh kita, maukah kau berkencan bersamaku? Hanya kita, berdua?", 
                    "Aku mengenalmu tanpa sengaja, lalu menyayangimu secara tiba-tiba, namun sayang belum jadi siapa-siapa, mungkin nanti atau esok?",
                    "Kamu sejenis keyboard ya? soalnya you are my type", 
                    "Kamu kenal iwan ga? bukan iwan fals, Iwan to be your boyfriend",
                    "Kamu isi pulpen ya? soalnya aku Tinta sama kamu", 
                    "Kamu tau bedanya kamu sama rumah hantu ga? Kalau rumah hantu sarang hantu, kalau kamu sarangheo",
                    "muka kamu kek pantun ya? soalnya cakep!!!", 
                    "Dijalan ada lampu, Dikuburan ada hantu, Dikerajaan ada ratu, dihatiku ada kamu", 
                    "Ada dua kata buat kamu, aku sayang kamu, karena aku dan kamu itukan satu",
                    "Kamu tau buah kan? aku suka buah apel, karena apel lah arti hidupku tanpa kamu",
                    "Tau gak, kenapa kalau belajar terus ngapal liatnya keatas? karena kalau merem langsung kebayang muka kamu",
                    "Kalo deket denganmu aku keringetan tapi kalo jauh denganmu aku jadi keingetan",
                    "Bambu bisa gantiin kayu, sendal bisa gantiin sepatu, tapi 1 hal yang harus kamu tau, gak akan ada yang bisa gantiin kamu",
                    "Berusaha melupakanmu sama sulitnya dengan mengingat seseorang yang tak pernah kukenal, karena dari aku kecil aku diajarin menghapal bukan melupakan",  
                ]
                gombal = random.choice(list_gombal)
                self.typeAndSendMessage(gombal)


        except Exception as e:
            print(e)
            print("errorr..")
            self.typeAndSendMessage("Duh maaf program yang diminta lagi rusak nih.. tulisannya : \n _"+str(e)+"_ \n minta tolong dong forwadin pesan diatas ke akang teteh mimin ya... Makasih :) ")

    def listToString(self, message):
        pesan = " "

        return (pesan.join(message))

    def movieSchedule(self, message):
        keyWatch = ["bioskop", "film", "pilem"]
        cityName = ["jakarta", "bandung"]
        locationName = ["braga", "btc"]
        cinemaName = ["xxi"]

        for i in message:
            if i in keyWatch:
                for j in message:
                    if j in cityName:
                        self.namkot = j
                    if j in cinemaName:
                        self.nambios = j
                    if j in locationName:
                        self.namlok = j

        sleep(1)

        self.driver.execute_script("window.open('https://jadwalnonton.com/bioskop/di-" + self.namkot + '/' + self.namlok + '-' + self.nambios + '-' + self.namkot + ".html');")

        self.driver.switch_to_window(self.driver.window_handles[1])
        try:
            error = self.driver.find_element_by_xpath("//div[contains(@class, 'caution')]").text
            if "404" in error:
                self.driver.close()
                sleep(1)
                self.driver.switch_to_window(self.driver.window_handles[0])
                sleep(1)
                self.typeAndSendMessage("Data not found")
        except:
            jumlah = self.driver.find_elements_by_xpath("//div[contains(@class, 'col-sm-10 sched_desc')]")
            jadwal = ""
            for i in jumlah:
                jadwal = i.text + jadwal
            self.driver.close()
            sleep(1)
            self.driver.switch_to_window(self.driver.window_handles[0])
            sleep(1)
            jadwalFix = jadwal.replace("LIHAT DI BIOSKOP LAIN", "")
            sleep(1)
            self.typeAndSendMessage(jadwalFix)

    def perhutani(self):
        usEmail = "email"
        usPass = "password"

        self.driver.execute_script("window.open('https://www.tokoperhutani.com/beranda/searchFromRecap/4140100/4141100/4141102/010')")
        sleep(.5)

        self.driver.switch_to_window(self.driver.window_handles[1])
        sleep(2)

        self.driver.find_element_by_link_text("Login").click()
        sleep(.5)

        self.driver.find_element_by_id("email").send_keys(usEmail)
        self.driver.find_element_by_id("password").send_keys(usPass)

        self.driver.find_elements_by_class_name("le-button")[0].click()
        sleep(60)

        wekser = ['193150214695', '193150214696', '193150214751', '193150215151', '193150215166', '193150215173',
                  '193150215178', '193150215190', '193150215192', '193150215398', '193150215511', '193150215524',
                  '193150214698', '193150215373']

        cariData = True

        forCounting = []

        self.driver.find_elements_by_class_name("paginate_button")[6].click()

        tableDataofOrder = self.driver.find_elements_by_xpath("//table[@id='example' and @class='display select nowrap dataTable no-footer']/tbody/tr")

        for i in tableDataofOrder:
            getNumberofOrder = i.text[9:22]
            splitting = getNumberofOrder.splitlines()
            forCounting.append(splitting)

        count = 10 - len(forCounting)

        while cariData:
            asd = self.driver.find_elements_by_xpath("//table[@id='example' and @class='display select nowrap dataTable no-footer']/tbody/tr")

            for i in asd:
                count += 1
                getNumberofOrder = i.text[9:22]
                splitting = getNumberofOrder.splitlines()

                if splitting[0] in wekser:
                    i.click()
                    wektow = wekser.index(splitting[0])
                    wekser.pop(wektow)

                if len(wekser) == 0:
                    cariData = False
                    self.driver.find_elements_by_class_name("le-button")[1].click()
                if count == 10 and len(wekser) >= 1:
                    print("There still another order, still working..")
                    count = 0
                    self.driver.find_element_by_id("example_previous").click()

    def gmaps(self, destination):
        self.driver.find_elements_by_class_name("_15Rkh")[-1].click()
        sleep(1)

        self.driver.switch_to_window(self.driver.window_handles[1])
        sleep(1)

        self.destination = destination
        sleep(1)

        self.coordinate = self.driver.find_element_by_id("searchboxinput").get_attribute("value")
        sleep(1)

        self.driver.find_element_by_id("sb_cb50").click()
        sleep(1)

        self.driver.find_element_by_id("searchboxinput").send_keys(self.destination + Keys.ENTER)
        sleep(4)

        try:
            self.driver.find_elements_by_class_name("iRxY3GoUYUY__taparea")[0].click()
            sleep(1)
        except Exception as e:
            print(e)
            print("There are 2 object or more destination!")

            cekButton = self.driver.find_elements_by_class_name("section-result-action-text")[0].text

            if cekButton == "Website":
                print("Websites")
                self.driver.find_elements_by_class_name("section-result-action-text")[1].click()
                sleep(2)
            else:
                self.driver.find_elements_by_class_name("section-result-action-text")[0].click()
                sleep(2)

        self.driver.find_elements_by_class_name("tactile-searchbox-input")[2].click()
        sleep(1)

        self.driver.find_elements_by_class_name("tactile-searchbox-input")[2].send_keys(Keys.BACKSPACE)
        sleep(1)

        self.driver.find_elements_by_class_name("tactile-searchbox-input")[2].send_keys(self.coordinate + Keys.ENTER)
        sleep(1)

        currentUrl = self.driver.current_url
        sleep(1)

        self.driver.close()
        sleep(1)

        self.driver.switch_to_window(self.driver.window_handles[0])
        sleep(1)

        self.typeAndSendMessage(currentUrl)
        sleep(1)

    def sendPictureWithPhoneNumber(self, phoneNumber, filePath):
        self.driver.get("https://web.whatsapp.com/send?phone=" + phoneNumber)

        self.waitLogin()
        sleep(3)

        self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
        sleep(2)

        path = r"C:\Users\rolly\Downloads"
        nameFile = filePath + ".jpeg"

        result = os.path.join(path, nameFile)

        self.driver.find_element_by_css_selector("input[type='file']").send_keys(result)
        sleep(1)

        self.driver.find_element_by_css_selector("span[data-icon='send-light").click()
        sleep(1)

    #change wanda photo
    def sendPictureWithoutPhoneNumber(self):
        self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
        sleep(2)

        path = r"C:\Users\rolly\Downloads"
        nameFile = ["wanda.jpeg", "wanda1.jpeg", "wanda2.jpeg", "wanda3.jpeg"]

        namaFile = random.choice(nameFile)

        result = os.path.join(path, namaFile)

        self.driver.find_element_by_css_selector("input[type='file']").send_keys(result)
        sleep(1)

        self.driver.find_element_by_css_selector("span[data-icon='send-light").click()
        sleep(1)

    #add video hiburan wanda
    def sendVideoWithoutPhoneNumber(self):
        self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
        sleep(2)

        path = r"C:\Users\rolly\Downloads"

        if "ngedance" in self.getMessage and "wanda" in self.getMessage:
            nameFile = ["wanda.mp4", "ngedance1.mp4", "ngedance2.mp4"]
            namaFile = random.choice(nameFile)
        if "nyanyi" in self.getMessage and "wanda" in self.getMessage:
            namaFile = "nyanyi.mp4"
        if "imutnya" in self.getMessage and "wanda" in self.getMessage and "gaya" in self.getMessage:
            nameFile = ["imut1.mp4", "imut2.mp4"]
            namaFile = random.choice(nameFile)

        result = os.path.join(path, namaFile)

        self.driver.find_element_by_css_selector("input[type='file']").send_keys(result)
        sleep(1)

        self.driver.find_element_by_css_selector("span[data-icon='send-light").click()
        sleep(1)

        self.driver.find_element_by_class_name("_1g8sv NOJWi").click()
        sleep(1)

    def retrievePicture(self):
        self.driver.find_elements_by_class_name("_18vxA")[-1].click()
        sleep(1)

        self.driver.find_element_by_css_selector("span[data-icon='download']").click()
        sleep(1)

        self.driver.find_element_by_css_selector("span[data-icon='x-viewer']").click()
        sleep(1)

    def deletePicture(self):
        dir_name = "/Users/rolly/Downloads/"
        list = os.listdir(dir_name)

        for item in list:
            if item.endswith(".jpeg"):
                os.remove(os.path.join(dir_name, item))

    def getName(self):
        try:
            self.driver.find_element_by_class_name("_3fs0K").click()
            sleep(1)

            self.driver.find_element_by_class_name("_2vJOg").click()
            sleep(1)

            name = self.driver.find_elements_by_class_name("_F7Vk")[1].text
            sleep(1)

            self.driver.find_element_by_css_selector("span[data-icon='x-viewer']").click()
            sleep(1)
        except Exception as e:
            print(e)
            print("Grup")

            name = self.driver.find_elements_by_class_name("_3u328")[0].text
            sleep(1)

        return name

    def renamePicture(self, fileName):
        dir_name = "/Users/rolly/Downloads/"
        list = os.listdir(dir_name)

        print(list)

        for item in list:
            if item.endswith(".jpeg"):
                os.rename(os.path.join(dir_name, item), os.path.join(dir_name, fileName + ".jpeg"))

    def cocoNamesLoad(self):
        listClass = []

        with open("coco.names", "r") as daftarNama:
            for i in daftarNama.readlines():
                cocoNames = i.strip()
                listClass.append(cocoNames)

        return listClass

    def loadYolo(self, coconames, fileName):
        model = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

        layerNames = model.getLayerNames()

        outputLayer = []

        for i in model.getUnconnectedOutLayers():
            outputLayer.append(layerNames[i[0] - 1])

        path = r"C:\Users\rolly\Downloads"
        nameFile = fileName + ".jpeg"

        result = os.path.join(path, nameFile)

        img = cv2.imread(result)

        width, height, channels = img.shape

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        model.setInput(blob)
        outs = model.forward(outputLayer)

        boxes = []
        class_ids = []
        confidences = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)

                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    class_ids.append(class_id)
                    confidences.append(float(confidence))

        #translate
        translate = Translator()
        namaObjek = []
        for i in range(len(boxes)):
            label = coconames[class_ids[i]]
            hasilTranslate = translate.translate(label, dest='id').text
            print(hasilTranslate)

            if hasilTranslate in namaObjek:
                print("The object exist of list")
            else:
                namaObjek.append(hasilTranslate)

        return namaObjek

    def faceRecognition(self, fileName):

        rolly_picture = face_recognition.load_image_file("rolly.jpg")
        rolly_encoding = face_recognition.face_encodings(rolly_picture)[0]

        angga_picture = face_recognition.load_image_file("angga.jpg")
        angga_encoding = face_recognition.face_encodings(angga_picture)[0]

        known_face_encodings = [
            rolly_encoding,
            angga_encoding
        ]

        known_face_names = [
            "Rolly M.A.",
            "Tri Angga D.S"
        ]

        path = r"C:\Users\rolly\Downloads"
        nameFile = fileName + ".jpeg"

        result = os.path.join(path, nameFile)

        test_image = face_recognition.load_image_file(result)

        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        name = []

        for face_encoding in face_encodings:
            results = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)

            if True in results:
                match_index = results.index(True)
                name.append(known_face_names[match_index])

        return name


