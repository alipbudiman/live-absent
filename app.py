from important import *


app = Flask(__name__)
# add mongo client url to config.json, example: mongodb+srv://<username>:<password>@cluster0.asadwq.mongodb.net/?retryWrites=true&w=majority
client = MongoClient(Config().mongodb_url)
user_db = client.user.data
admin_db = client.dataadmin.dataadmin

def datatime():
    jam = pytz.timezone("Asia/Jakarta")
    jamSek = datetime.now(tz=jam)
    date = datetime.strftime(jamSek, "%d-%m-%Y")
    return date

def unique_uuid(nim):
    unique_uuid = uuid.uuid4()
    namespace = uuid.UUID(str(unique_uuid))
    unique_uuid = uuid.uuid5(namespace, nim)
    return str(unique_uuid)

@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/assets/<path:path>',methods=['GET'])
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/editdata',methods=['POST','GET'])
def edit():
    if request.method == 'GET':
        admin = admin_db.find_one({"tag":"admin"})
        if admin["editaccess"]:
            return render_template("edit.html")
        else:
            return redirect("/")
    elif request.method == 'POST':
        nim = request.form.get("nim", type=str)
        prod = request.form.get("prod", type=str)
        if nim and prod:
            find_nim = user_db.find_one({"nim":nim})
            admin = admin_db.find_one({"tag":"admin"})
            if admin["editaccess"] and find_nim is not None:
                user_db.update_one({'nim': nim}, {'$set': {'prod': prod}})
                find_nim = user_db.find_one({"nim":nim})
                if find_nim["prod"] == prod:
                    return jsonify({
                        "code":200,
                        "message":f"success edit prodi menjadi {prod}"
                    })
                else:
                    return jsonify({
                        "code":201,
                        "message":"error, not edited",
                    })
            else:
                return jsonify({
                    "code":400,
                    "message":"Anda tidak memenuhi administrasi untuk mengganti data sertifikat",
                })
        else:
            return jsonify({
                "code":500,
                "message":"bad request",
            })
        

@app.route('/authorize',methods=['POST','GET'])
def authorize():
    get_time = datatime()
    passcode = request.args.get("passcode")
    if passcode:
        admin = admin_db.find_one({"tag":"admin"})
        if admin["passcode"] == passcode and admin["access"]:
            if request.method == 'GET':
                return render_template("authorize.html")
            elif request.method == 'POST':
                nim = request.form.get("nim")
                if nim:
                    find_nim = user_db.find_one({"nim":nim})
                    if admin["lastattend"]:
                        if find_nim is not None:
                            last_attend = get_time+"(last attend)"
                            if last_attend not in list(find_nim["attendance"]):
                                user_db.update_one({'nim': nim}, {'$push': {'attendance': last_attend}})
                                find_nim = user_db.find_one({"nim":nim})
                                del find_nim["_id"]
                                if last_attend in list(find_nim["attendance"]):
                                    return jsonify({
                                        "code":200,
                                        "return":{
                                            "message":f"success attendance {get_time}",
                                            "data":find_nim,
                                        }
                                    })
                        else:
                            return jsonify({
                                "code":201,
                                "return":{
                                    "message":f"nim {nim} tidak ditemukan, kamu tidak bisa melakukan last attendance"
                                }
                            })
                    if find_nim is not None:
                        if get_time not in list(find_nim["attendance"]):
                            user_db.update_one({'nim': nim}, {'$push': {'attendance': get_time}})
                            find_nim = user_db.find_one({"nim":nim})
                            del find_nim["_id"]
                            if get_time in list(find_nim["attendance"]):
                                return jsonify({
                                    "code":200,
                                    "return":{
                                        "message":f"success attendance {get_time}",
                                        "data":find_nim,
                                    }
                                })
                            else:
                                return jsonify({
                                    "code":401,
                                    "return":{
                                        "message":"internal server error, coba lagi",
                                    }
                                })
                        else:
                            return jsonify({
                                "code":201,
                                "return":{
                                    "message":f"nim {nim} sudah melakukan absent"
                                }
                            })
                    else:
                        return jsonify({
                        "code":202,
                            "return":{
                                "message":"Masuk form pendaftaran"
                            }
                        })
                else:
                    return jsonify({
                        "code":500,
                        "return":{
                            "message":"bad requests"
                        }
                    })
        else:
            if request.method == 'GET':
                return redirect("/?status=notallowed")
            elif request.method == 'POST':
                return jsonify({
                    "code":400,
                    "return":{
                        "message":"not allowed"
                    }
                })
    else:
        if request.method == 'GET':
            return redirect("/")
        elif request.method == 'POST':
            return jsonify({
                "code":500,
                "return":{
                    "message":"bad requests"
                }
            })

@app.route('/daftar', methods=['POST','GET'])
def daftar():
    passcode = request.args.get("passcode")
    admin = admin_db.find_one({"tag":"admin"})
    if admin["passcode"] == passcode and admin["access"]:
        if request.method == 'GET':
            return render_template("daftar.html")
        elif request.method == 'POST':
            get_time = datatime()
            nim = request.form.get("nim", type=str)
            nama = request.form.get("nama", type=str)
            bp = request.form.get("bp", type=str)
            prod = request.form.get("prod", type=str)
            tanggapan = request.form.get("tanggapan", type=str)
            setuju = request.form.get("setuju", type=bool)
            if nim and nama and bp and prod and tanggapan and setuju and prod in ['infa','si','bd','mr','dkv']:
                if admin["access"]:
                    find_nim = user_db.find_one({"nim":nim})
                    if find_nim is not None and get_time in list(find_nim["attendance"]):
                        return jsonify({
                            "code":201,
                            "return":{
                                "message":f"nim: {nim} sudah terdaftar"
                            }
                        })
                    else:
                       data_register = {
                        "nama":nama,
                        "nim":nim,
                        "prod":prod,
                        "tanggapan":tanggapan,
                        "setuju":setuju,
                        "uuid":unique_uuid(nim),
                        "attendance":[
                            get_time,
                        ]
                    }
                    user_db.insert_one(data_register) 
                    find_nim = user_db.find_one(data_register)
                    del find_nim['_id']
                    if find_nim is not None:
                        return jsonify({
                            "code":200,
                            "return":{
                                "message":f"success attendance {get_time}",
                                "data":find_nim
                            }
                        })
                            
                else:
                    return jsonify({
                        "code":400,
                        "return":{
                            "message":"not allowed"
                        }
                    })
            else:
                return jsonify({
                    "code":500,
                    "return":{
                        "message":"bad requests"
                    }
                })
    else:
        if request.method == 'GET':
            return redirect("/")
        elif request.method == 'POST':
            return jsonify({
                "code":400,
                "return":{
                    "message":"not allowed"
                }
            })

@app.route('/success', methods=['GET'])
def success():
    protocol_id = request.args.get("protocol_id")
    if protocol_id:
        find_uuid = user_db.find_one({"uuid":protocol_id})
        if find_uuid is not None:
            return render_template("success.html", nama=find_uuid["nama"], nim=find_uuid["nim"],uuid=protocol_id)
        else:
            return render_template("404.html")
    else:
        return jsonify({
            "code":500,
            "return":{
                "message":"bad requests"
            }
        })

@app.route('/check', methods=['GET'])
def check():
    protocol_id = request.args.get("protocol_id")
    if protocol_id:
        find_uuid = user_db.find_one({"uuid":protocol_id})
        if find_uuid:
            return render_template("check.html", nama=find_uuid["nama"], nim=find_uuid["nim"],listdata=find_uuid["attendance"])
        else:
            return render_template("check.html", nama="Not Found", nim="Not Found",uuid="Not Found")
    else:
        return render_template("check.html", nama="Not Found", nim="Not Found",uuid="Not Found")

if __name__ == "__main__":
    app.run(debug=False, port=5005)