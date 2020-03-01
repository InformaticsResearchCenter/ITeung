# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 19:46:39 2020

@author: rolly
"""

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
    def sendVideoWithoutPhoneNumber(self, msgs):
        self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
        sleep(2)

        path = r"C:\Users\rolly\Downloads"

        if "ngedance" in msgs and "wanda" in msgs:
            nameFile = ["wanda.mp4", "ngedance1.mp4", "ngedance2.mp4"]
            namaFile = random.choice(nameFile)
        if "nyanyi" in msgs and "wanda" in msgs:
            namaFile = "nyanyi.mp4"
        if "imutnya" in msgs and "wanda" in msgs and "gaya" in msgs:
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

