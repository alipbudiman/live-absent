from important import *

app = Flask(__name__)
# add mongo client url to config.json, example: mongodb+srv://<username>:<password>@cluster0.asadwq.mongodb.net/?retryWrites=true&w=majority
client = MongoClient(Config().mongodb_url)
user_db = client.user.data
admin_db = client.dataadmin.dataadmin

# add attenden day 1, day 2 and last attenden
date_attend = ("03-03-2024", "04-03-2024","05-03-2024(last attend)")

def spamdb(num):
    data = []
    for x in range(int(num)):
        data.append({
            "nama":x,
            "nim":x,
            "prod":x,
            "tanggapan":x,
            "setuju":True,
            "uuid":x,
            "attendance":[
                x,
            ]
        })
    user_db.insert_many(data)

def datatime():
    jam = pytz.timezone("Asia/Jakarta")
    jamSek = datetime.now(tz=jam)
    date = datetime.strftime(jamSek, "%d-%m-%Y")
    return date

def find_attend(attends, date):
    for attend in attends:
        if date in attend:
            return True
    return False

def export_data(data):
    df = pd.DataFrame(data)
    df.to_excel('assets/doc/data_mahasiswa_upgrading.xlsx', index=False)
    return True

def add_spacing(total_space, text):
    spaces = " "*total_space
    return  spaces.join(txt for txt in text)

def creating_cert(no, nama, nim, prod):
    img_cert = "assets/img/sertifikat.png"
    # Buka gambar sertifikat
    sertifikat = Image.open(img_cert)
    # Inisialisasi objek ImageDraw untuk menambahkan teks ke gambar
    draw = ImageDraw.Draw(sertifikat)
    image = Image.open(img_cert)

    # Definisikan teks pertama
    if len(str(no)) == 1:no = f"0{no}"
    teks_pertama = add_spacing(0,f"Nomor : {no}/PANPEL/BEM.META-U/X/2023")
    ukuran_font_pertama = 29
    posisi_x_pertama = int(8.46 * 85.30)  # 1 cm = 118.11 piksel
    posisi_y_pertama = int(3.2 * 114.11)
    font1 = ImageFont.truetype("assets/font/FontsFree-Net-Poppins-Medium.ttf", ukuran_font_pertama)

    # Definisikan teks kedua
    teks_kedua = nama

    ukuran_font_kedua = 80
    # posisi_x_kedua = int(5.50 * 120.00)
    # posisi_y_kedua = int(9.38 * 67.00)
    font2 = ImageFont.truetype("assets/font/SourceSerifPro-Semibold.ttf", ukuran_font_kedua)

    # auto center text 2
    image_width, image_height = image.size
    text_width, text_height = draw.textsize(teks_kedua, font=font2)

    posisi_x_kedua = (image_width - text_width) / 2
    posisi_y_kedua = ((image_height - text_height) / 2) - 30

    # Definisikan teks ketiga
    teks_ketiga = f"NIM : {nim}"
    ukuran_font_ketiga = 40
    # posisi_x_ketiga = int(11.99 * 118.11)
    # posisi_y_ketiga = int(10.92 * 118.11)
    font3 = ImageFont.truetype("assets/font/FontsFree-Net-Poppins-Medium.ttf", ukuran_font_ketiga)

    # auto center text 3
    image_width, image_height = image.size
    text_width, text_height = draw.textsize(teks_ketiga, font=font3)

    posisi_x_ketiga = ((image_width - text_width) / 2)
    posisi_y_ketiga = ((image_height - text_height) / 2) + 47

    # Definisikan teks keempat
    teks_keempat = f"Program Studi {prod}"
    ukuran_font_keempat = 29
    # posisi_x_ketiga = int(11.99 * 118.11)
    # posisi_y_ketiga = int(10.92 * 118.11)
    font4 = ImageFont.truetype("assets/font/FontsFree-Net-Poppins-Medium.ttf", ukuran_font_keempat)

    # auto center text 3
    image_width, image_height = image.size
    text_width, text_height = draw.textsize(teks_keempat, font=font4)

    posisi_x_keempat = ((image_width - text_width) / 2)
    posisi_y_keempat = ((image_height - text_height) / 2) + 100

    # Tambahkan teks pertama ke gambar
    draw.text((posisi_x_pertama, posisi_y_pertama), teks_pertama, fill="black", font=font1)

    # Tambahkan teks kedua ke gambar
    draw.text((posisi_x_kedua, posisi_y_kedua), teks_kedua, fill="orange", font=font2)

    # Tambahkan teks ketiga ke gambar
    draw.text((posisi_x_ketiga, posisi_y_ketiga), teks_ketiga, fill="orange", font=font3)

    # Tambahkan teks keempat ke gambar
    draw.text((posisi_x_keempat, posisi_y_keempat), teks_keempat, fill="black", font=font4)

    # Simpan gambar yang telah diperbarui
    sertifikat.save(f"assets/doc/cert/SERTIFIKAT UPGRADING_{nama}_{nim}.png")

    # Tutup gambar sertifikat
    sertifikat.close()

@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/assets/<path:path>',methods=['GET'])
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/', methods=["GET"])
def index():
    return redirect('/checkall')

@app.route(f'/checkall', methods=['GET'])
def checkall():
    admin = admin_db.find_one({"tag":"admin"})
    if admin["access"]:status = "OPEN"
    else:status = "CLOSE"
    if admin["consolelock"]:consolelock = "LOCK"
    else:consolelock = "UNLOCK"
    if admin["lastattend"]:lastattend = "ACTIVE"
    else:lastattend = "DEACTIVE"
    return render_template("checkall.html",passcode=admin["passcode"],status=status,date=datatime(),consolelock=consolelock,lastattend=lastattend)

@app.route(f'/checkall/load', methods=['GET'])
def checkall_load():
    data_all = user_db.find({"setuju":True})
    grab_collect = []
    for i,x in enumerate(list(data_all)):
        att1 = find_attend(x["attendance"], date_attend[0])
        if att1 == True:
            att1 = date_attend[0]
        else:
            att1 = "Not Attendance"
        att2 = find_attend(x["attendance"], date_attend[1])
        if att2 == True:
            att2 = date_attend[1]
        else:
            att2 = "Not Attendance"
        att3 = find_attend(x["attendance"], date_attend[2])
        if att3 == True:
            att3 = date_attend[2]
        else:
            att3 = "Not Attendance"
        grab_collect.append(f'{i+1}|{x["nama"]} ({x["nim"]})|{att1}|{att2}|{att3}')
    return render_template("checkallload.html", listdata=grab_collect)

@app.route('/checkall/change', methods=['POST'])
def checkall_change():
    passcode = request.form.get("passcode")
    access = request.form.get("access")
    commands = request.form.get("commands")
    consolelock = request.form.get("consolelock")
    lastattend = request.form.get("lastattend")
    if passcode != "":admin_db.update_one({'tag': "admin"}, {'$set': {'passcode': passcode}})
    if access != "":
        if access == "1":admin_db.update_one({'tag': "admin"}, {'$set': {'access': True}})
        else:admin_db.update_one({'tag': "admin"}, {'$set': {'access': False}})
    if lastattend != "":
        if lastattend == "1":admin_db.update_one({'tag': "admin"}, {'$set': {'lastattend': True}})
        else:admin_db.update_one({'tag': "admin"}, {'$set': {'lastattend': False}})
    if consolelock != "":
        if consolelock == "1":admin_db.update_one({'tag': "admin"}, {'$set': {'consolelock': True}})
        else:admin_db.update_one({'tag': "admin"}, {'$set': {'consolelock': False}})
    if commands != "":
        admin = admin_db.find_one({"tag":"admin"})
        if admin["consolelock"]:
            return jsonify({
                "code":201,
                "message":"console lock is on"
            }),200
        else:
            if commands.lower().startswith("/del "):user_db.delete_many({"nim":commands[len("/del "):]})
            elif commands.lower().startswith("/upname "):user_db.update_one({'nim': str(commands[len("/upname "):]).split("|")[0]}, {'$set': {'nama': str(commands[len("upname "):]).split("|")[1]}})
            elif commands.lower().startswith("/upnim "):user_db.update_one({'nim': str(commands[len("/upnim "):]).split("|")[0]}, {'$set': {'nim': str(commands[len("upnim "):]).split("|")[1]}})
            elif commands.lower().startswith("/spam "):spamdb(str(commands[len("/spam "):]))
            elif commands.lower() == "/clear all data":user_db.delete_many({"setuju":True})
            elif commands.lower() == "/ping":
                admin_db.update_one({'tag': "admin"}, {'$set': {'consolelock': True}})
                return jsonify({
                    "code":202,
                    "message":"Pong!!"
                }),200
            else:
                return jsonify({
                    "code":202,
                    "message":"Command not found!!"
                }),200
    return jsonify({
        "code":200
    }),200

@app.route('/checkall/passcode', methods=['GET'])
def checkall_passcode():
    return render_template("passcode.html", passcode=admin_db.find_one({"tag":"admin"})["passcode"])

@app.route('/checkall/import', methods=['POST'])
def checkall_import():
    data_all = user_db.find({"setuju":True})
    grab_collector = []
    for data in list(data_all):
        if data["prod"] == "infa":prodi = "INFORMATIKA"
        elif data["prod"] == "si":prodi = "SISTEM INFORMASI"
        elif data["prod"] == "bd":prodi = "BISNIS DIGITAL"
        elif data["prod"] == "mr":prodi = "MANAGEMENT RETAIL"
        elif data["prod"] == "dkv":prodi = "DESAIN KOMUNIKASI VISUAL"
        att1 = find_attend(data["attendance"], date_attend[0])
        if att1 == True:
            att1 = date_attend[0]
        else:
            att1 = "Not Attendance"
        att2 = find_attend(data["attendance"], date_attend[1])
        if att2 == True:
            att2 = date_attend[1]
        else:
            att2 = "Not Attendance"
        att3 = find_attend(data["attendance"], date_attend[2])
        if att3 == True:
            att3 = date_attend[2]
        else:
            att3 = "Not Attendance"
        collect = {
            "NAMA":str(data["nama"]).upper(),
            "NIM":data["nim"],
            "ANGKATAN":"20"+str(data["nim"])[:2],
            "PRODI":prodi,
            "TANGGAPAN":data["tanggapan"],
            "ATTEND 1":att1,
            "ATTEND 2":att2,
            "LAST ATTEND":att3,
        }
        grab_collector.append(collect)
    export_data(grab_collector)
    return jsonify({
        "code":201,
        "message":"success export data, please check folder"
    })

@app.route('/checkall/cert', methods=['POST'])
def checkall_cert():
    data_all = user_db.find({"setuju":True})
    for i, data in enumerate(list(data_all)):
        if data["prod"] == "infa":prodi = "INFORMATIKA"
        elif data["prod"] == "si":prodi = "SISTEM INFORMASI"
        elif data["prod"] == "bd":prodi = "BISNIS DIGITAL"
        elif data["prod"] == "mr":prodi = "MANAGEMENT RETAIL"
        elif data["prod"] == "dkv":prodi = "DESAIN KOMUNIKASI VISUAL"
        att1 = find_attend(data["attendance"], date_attend[0])
        att2 = find_attend(data["attendance"], date_attend[1])
        att3 = find_attend(data["attendance"], date_attend[2])
        if att1 and att2 and att3:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                executor.submit(creating_cert(i+1, str(data["nama"]).upper(),data["nim"],prodi.title()))
    return jsonify({
        "code":201,
        "message":"success create cert, please check folder"
    })

if __name__ == "__main__":
    app.run(debug=False, port=5010)