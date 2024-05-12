from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector


app = FastAPI()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123qwe", 
  database="website"  
)

# 創建靜態文件，指定目錄
app.mount("/css", StaticFiles(directory="css"), name="css")

# 創建 Jinja2Templates，會在文件目錄templates中尋找模板文件
templates = Jinja2Templates(directory="templates")

# 加入 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="secret")


# 首頁路由("/")處理GET請求，回應為HTMLResponse，返回HTML内容
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # 開啟並讀取位於 "templates/home-page.html" 的範本文件
    with open("templates/home-page.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    # 傳回 HTMLResponse，內容為讀取的 HTML 檔案內容，狀態碼為 200（表示成功）
    return HTMLResponse(content=html_content, status_code=200)

# 註冊
@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, name: str = Form(None), username: str = Form(None), password: str = Form(None)):
    # 檢查用戶是否已存在
    mycursor = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s"
    val = (username,)
    mycursor.execute(sql, val)

    result = mycursor.fetchall()

    # 檢查用戶是否已存在
    if result:
        message = "重複的帳號，請選擇其他帳號"
        return RedirectResponse(url=f"/error?message={message}", status_code=303) 
           
    # 將新用戶插入資料庫
    sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    val = (name, username, password)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # 註冊成功，導向到首頁
    return RedirectResponse(url="/?message=註冊完成", status_code=303, headers={"Location": "/"})


# 處理登入
@app.post("/signin", response_class=HTMLResponse)
async def signin(request: Request, username: str = Form(None), password: str = Form(None)):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM member WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(sql, val)

    result = mycursor.fetchall()

    # 檢查
    if len(result) > 0:
        # 登入成功
        request.session['username'] = username
        return RedirectResponse(url="/member", status_code=303)
    else:
        # 登入失敗
        message = "帳號或密碼輸入錯誤"
        return templates.TemplateResponse("error.html", {"request": request, "message": message})

    
@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

# 檢查登入
def checkLogin(request: Request):
    session = request.session
    if session.get('username'):
        return True #已登入
    else:
        return False #未登入


@app.get("/member", response_class=HTMLResponse)
async def member_page(request: Request):
    if checkLogin(request):
        # 從會話中獲取用戶名
        username = request.session.get('username')
      
      # 查詢資料庫，獲取用戶名對應的名字
        mycursor = mydb.cursor()
        sql = "SELECT name FROM member WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        
        if result:
            name = result[0]
        # 導向會員頁
        else:
            name = None

        # 查詢留言
        mycursor = mydb.cursor()
        sql = "SELECT member.name, message.content, message.time FROM member INNER JOIN message ON member.id = message.member_id ORDER BY message.time DESC"
        mycursor.execute(sql)
        message_result = mycursor.fetchall()

        # 整理留言成字典的列表，以便在 HTML 中顯示
        message = [{"name": message[0], "content": message[1], "created_at": message[2]} for message in message_result]


        return templates.TemplateResponse("member-page.html", {"request": request, "name": name, "message": message})


    else:
        # 未登入，導向首頁
        return RedirectResponse(url="/")

# 處理登出
@app.get("/signout")
async def signout(request: Request):
    # 清除 session 中的用戶名
    request.session.pop('username', None)
    # 重定向到首頁
    return RedirectResponse(url="/")


# 獲取作者ID
def get_member_id(username):
    mycursor = mydb.cursor()
    sql = "SELECT id FROM member WHERE username = %s"
    val = (username,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return result[0]
    else:
        return None

@app.post("/createMessage")
async def create_message(request: Request, content: str = Form(...)):
    username = request.session.get('username')

    author_id = get_member_id(username)

    mycursor = mydb.cursor()
    sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    val = (author_id, content,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # 會員頁
    return RedirectResponse(url="/member", status_code=303)

