from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

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

# 處理登入
@app.post("/signin", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(None), password: str = Form(None)):
    # 如果用戶未輸入用戶名或密碼，導向錯誤頁面&錯誤訊息
    if username is None or password is None:
        error_message = "請輸入帳號、密碼"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    
    # 用戶名和密碼正確
    if username == "test" and password == "test":
        # 導向成功頁面
        request.session['username'] = username  # 將用戶名存儲到 session 中
        return RedirectResponse(url="/member", status_code=303)
        
    else:
        # 用戶名和密碼錯誤，導向錯誤頁面&錯誤訊息
        error_message = "帳號、或密碼輸入錯誤"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    
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
async def success_page(request: Request):
    if checkLogin(request):
        # 導向會員頁
        return templates.TemplateResponse("success.html", {"request": request})
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
