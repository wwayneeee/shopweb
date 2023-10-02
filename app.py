#初始化 flask 伺服器
from flask import *
# 載入 Application 物件，靜態檔案處理設定
app=Flask(
    __name__,
    static_folder = "public",
    static_url_path = "/"
)
# 設定 Session 密鑰
app.secret_key = "any string but secret"

# 初始化連線資料庫
import pymongo
client = pymongo.MongoClient("mongodb+srv://wayne:wayne123@mycluster.p6yq4gq.mongodb.net/?retryWrites=true&w=majority")
db = client.member_system
print("資料庫連線成功")
def get_db():
    return db

from member import *

# 首頁
@app.route("/")
def index():
    collection=db.product
    result=collection.find({
        "$and":[
            {"productcategory":"clothes"}
        ]
    })
    productvalue=[]
    for value in result:
        productvalue.append(str(value["productvalue"]))
    return render_template("index.html",productvalue=productvalue)

# 註冊頁面
@app.route("/register")
def register():
    return render_template("register.html")
# 註冊功能路由，檢查帳密重複及寫入資料庫
@app.route("/signup", methods=["POST"])
def signup():
    # 從前端接收資料
    username=request.form["username"]
    email=request.form["email"]
    password=request.form["password"]
    print(username, password, email)

    if username=="" or email=="" or password=="":
        return redirect("/error?msg=表格不得空白")
    
    result=membersystem(username,email,password)
    
    if result.signup():
        return redirect("/error?msg=信箱已被註冊")

    return redirect("/login")

# 登入頁面
@app.route("/login")
def login():
    if "username" in session:
        return redirect(url_for("member"))
    else:
        return render_template("login.html")
# 登入功能路由，檢查登入帳密
@app.route("/signin", methods=["POST"])
def signin():
    # 取得資料
    email=request.form["email"]
    password=request.form["password"]

    result = membersystem("",email,password)
    
    # 找不到資料，導向到錯誤頁面
    if not result.signin():
        return redirect("/error?msg=帳號或密碼錯誤")
    # 登入成功，在 Session 中紀錄會員資訊，導向會員頁面
    session["username"]=result.signin()["username"]
    return redirect("/")

# 會員系統頁面
@app.route("/member")
def member():
    if "username" in session:
        return render_template("member.html")
    else:
        return redirect("/login")        

# 登出功能路由
@app.route("/signout")
def signout():
    # 清除 Session 資料
    del session["username"]
    return redirect("/login")

# 更改密碼頁面
@app.route("/updatepw")
def pwupdate():
    if "username" in session:
        return render_template("updatepw.html")
    else:
        flash("請先登入")
        return redirect("/login")
# 更改密碼功能路由
@app.route("/changepw", methods=["POST"])
def changepw():
    email=request.form["email"]
    oldpassword=request.form["oldpassword"]
    newpassword=request.form["newpassword"]

    result=membersystem("",email,oldpassword)

    #找不到此帳密
    if result.changepw(newpassword) == "-1":
        return redirect("/error?msg=帳號或密碼錯誤")
    
    # 把新密碼傳到函式
    result.changepw(newpassword)

    del session["username"]
    return redirect("/login")

# 錯誤頁面
@app.route("/error")
def error():
    msg = request.args.get("msg","發生錯誤")
    return render_template("error.html", msg=msg)


# 啟動伺服器在 Port 3000
app.run(port=3000)