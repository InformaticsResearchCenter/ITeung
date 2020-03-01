from lib import wa,reply
import config
from module import prodi
import face_recognition
import cv2
import numpy as np
#import gspread
import os

import random
from time import sleep
from googletrans import Translator

class Chatbot(object):
    def __init__(self):
        driver = wa.setProfile(config.profile_folder)
        wa.loginWA(driver)
        while True:
            self.cekAndSendMessage(driver)
        
       
    def cekAndSendMessage(self,driver):
        try:
            wa.openMessage(driver)
            msg = wa.getMessage(driver)
            #num = self.getSenderNumber(driver)
            #alname = self.getSenderName(driver)
            #print(num+' - '+alname)
            
            msg  = wa.normalize(msg)
            msgs = list(msg.split(" "))
            
            if msg.find(config.bot_name) >= 0:
                if len(msgs) == 1:
                    list_jawaban = ["iyaaaaaa :-D", "iya, kenapa?", "iya, butuh bantuan? atau cuman rindu :D"]
                    jawaban = random.choice(list_jawaban)
                    wa.typeAndSendMessage(driver,jawaban)
                else:
                    msgreply=reply.message(msg)
                    if msgreply[:2] == 'm:':
                        print(msg)
                    wa.typeAndSendMessage(driver,msgreply)
                

            if "wanda" in msgs and "perkenalkan" in msgs or "kenalan" in msgs:
                self.sendPictureWithoutPhoneNumber()
                self.typeAndSendMessage("Halo, perkenalkan Nama aku wanda, Aku seorang mahasiswi poltekpos, Salam kenal ya")

            if "sidang" in msgs and "wanda" in msgs:
                self.typeAndSendMessage("ok, tunggu sebentar ya :-D")
                getIndex = msgs.index("sidang")
                try:
                    jadwal = prodi.cekJadwalSidang(msgs[getIndex+1])
                    jadwal.pop(0)
                    jadwal.pop(0)

                    if jadwal == "no_pilihan":
                        self.typeAndSendMessage("pilihan salah")
                    else:
                        for i in jadwal:
                            self.typeAndSendMessage("NPM: "+i[0]+", Nama: "+i[1]+", Penguji utama: "+i[2]+", Penguji pendamping: "+i[3]+", Jam: "+i[5]+", Lokasi: "+i[6])
                except:
                    self.typeAndSendMessage("jadwal sidang "+msgs[getIndex+1]+" tidak ada")


            if "bioskop" in msgs:
                self.movieSchedule(msgs)

            if "perhutani" in msgs:
                self.perhutani()

            if "gmaps" in msgs:
                msgs.pop(0)
                desti2 = self.listToString(msgs)
                self.gmaps(desti2)

            if "foto" in msgs:
                sleep(1)
                name = self.getName()
                sleep(1)
                self.retrievePicture()
                sleep(1)
                self.renamePicture(name)
                sleep(1)
                self.sendPictureWithPhoneNumber(msgs[1], name)
                sleep(1)
                self.deletePicture()
                sleep(1)

            if "gambar" in msgs:
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

            if "muka" in msgs:
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

            #formal
            if "selamat" in msgs and "siang" in msgs and "wanda" in msgs:
                self.typeAndSendMessage("iya, selamat siang :-)")
            if "selamat" in msgs and "sore" in msgs and "wanda" in msgs:
                self.typeAndSendMessage("iya, selamat sore :-)")
            if "selamat" in msgs and "malam" in msgs and "wanda" in msgs:
                self.typeAndSendMessage("iya, selamat malam :-)")
            if "selamat" in msgs and "pagi" in msgs and "wanda" in msgs:
                self.typeAndSendMessage("iya, selamat pagi :-)")

            # hiburan
            if "wanda" in msgs and "hibur" in msgs or "hiburan" in msgs:
                self.typeAndSendMessage("Boleh, mau lihat wanda ngedance atau nyanyi?")

            if "wanda" in msgs and "ngedance" in msgs or "dance" in msgs or "nari" in msgs:
                self.typeAndSendMessage("tunggu sebentar ya, wanda rekaman dulu")
                self.sendVideoWithoutPhoneNumber()

            if "wanda" in msgs and "nyanyi" in msgs or "menyanyi" in msgs:
                self.typeAndSendMessage("tunggu sebentar ya, wanda rekaman dulu")
                self.sendVideoWithoutPhoneNumber()

            if "wanda" in msgs and "gaya" in msgs and "imutnya" in msgs:
                self.typeAndSendMessage("bentar ya, rekaman dulu")
                self.sendVideoWithoutPhoneNumber()


        except Exception as e:
            print(e)
            print("errorr..")
            wa.typeAndSendMessage(driver,"Duh maaf program yang diminta lagi rusak nih.. tulisannya : \n _"+str(e)+"_ \n minta tolong dong forwadin pesan diatas ke akang teteh mimin ya... Makasih :) ")

    def listToString(self, message):
        pesan = " "

        return (pesan.join(message))


