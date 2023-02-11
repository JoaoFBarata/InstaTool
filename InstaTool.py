import requests
import json
import os
import asyncio
from playwright.async_api import async_playwright
import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD, Font
# import traceback
from PIL import ImageTk, Image
from io import BytesIO
import re
from cryptography.fernet import Fernet
import nest_asyncio
nest_asyncio.apply()

url = f"https://www.instagram.com/graphql/query/"

key = b'QlZXMiataxwOS9uQkvx9VmccvjUdrb__6c-O1frxgbw='
fernet = Fernet(key)

os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'

followingList = []
followingListId = []
followingListPic = []

followerList = []
followerListId = []
followerListPic = []

usersDetected = []
usersDetectedPic = []
usersDetectedId = []

async def getUsername(user_id, cookies):
    url = "https://i.instagram.com/api/v1/users/" + user_id + "/info/"
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920"}
    res = requests.get(url, headers=headers, cookies=cookies)
    return str(res.json()['user']['username'])

def unfollowUser(user_id, cookies, button):
    url = "https://www.instagram.com/api/v1/web/friendships/" + str(user_id) + "/unfollow/"
    # headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920"}
    headers = {
        "Referer": "https://www.instagram.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": cookies['csrftoken']
    }
    res = requests.post(url, headers=headers, cookies=cookies)
    # print(user_id)
    # print(cookies)
    # print(res.text)
    button.config(text='UNFOLLOWED', state='disabled', style='')
    return

async def Center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def signOut(app):
    app.quit()
    app.destroy()
    
    try:
        os.remove('./cookies.json')
    except:
        try:
            with open('./cookies.json', 'w') as f:
                f.write('')
        except:
            return
    return
    

def getList(list_type, nxt, user_id, cookies):
    if(nxt != None):
        variables = {
            "id": user_id,
            "first": 50,
            "after": nxt
        }
    else:
        variables = {
            "id": user_id,
            "first": 50,
            "after": None
        }
    
    if list_type == "followers":
        query_hash = "37479f2b8209594dde7facb0d904896a"
    elif list_type == "following":
        query_hash = "58712303d941c6855d4e888c5f0cd22f"
    else:
        SyntaxError('Invalid List Type Provided. Possible Options: followers or following.')

    headers = {
        "Referer": "https://www.instagram.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "X-Requested-With": "XMLHttpRequest"
    }

    url_final = (url + '?query_hash=' + query_hash + '&variables=' + json.dumps(variables))
    res = requests.get(url_final, headers, cookies=cookies)
    return json.loads(res.text)

async def get50follower(pg, user_id, cookies):
    followers = getList("followers", pg, user_id, cookies)['data']['user']['edge_followed_by']
    followers_info = followers['page_info']
    followers = followers['edges']

    for follower in followers:
        follower_name = follower['node']['username']
        follower_id = follower['node']['id']
        follower_profile_pic = follower['node']['profile_pic_url']
        
        followerList.append(follower_name)
        followerListId.append(follower_id)
        followerListPic.append(follower_profile_pic)
        
        # print(follower_name)


    # print(len(followerList))
    
    if not followers_info["has_next_page"]:
        return 0
    pg = followers_info["end_cursor"]
    await get50follower(pg, user_id, cookies)
    
async def get50following(pg1, user_id, cookies):
    followings = getList("following", pg1, user_id, cookies)['data']['user']['edge_follow']
    followings_info = followings['page_info']
    followings = followings['edges']
    
    for following in followings:
        following_name = following['node']['username']
        following_id = following['node']['id']
        following_profile_pic = following['node']['profile_pic_url']
        
        followingList.append(following_name)
        followingListId.append(following_id)
        followingListPic.append(following_profile_pic)
        
        # print(following_name)
        
    # print(len(followingList))
    
    if not followings_info["has_next_page"]:
        return 0
    pg1 = followings_info["end_cursor"]
    await get50following(pg1, user_id, cookies)
    
async def startProcessing(user_id, cookies):
    await get50follower(None, user_id, cookies)
    # print(len(followerList))
    await get50following(None, user_id, cookies)
    # print(len(followingList))

    for fllwng in followingList:
        if fllwng not in followerList:
            # print(fllwng)
            usersDetected.append(fllwng)
    
    for fllwngId in followingListId:
        if fllwngId not in followerListId:
            # print(fllwngId)
            usersDetectedId.append(fllwngId)
    
    for fllwngPic in followingListPic:
        newfollowerListPic = []
        for i in followerListPic:
            newfollowerListPic.append(re.sub('&_nc_ht=.*','',i))
            
        if re.sub('&_nc_ht=.*','',fllwngPic) not in newfollowerListPic:
            # print('HEYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY        ' + str(json.dumps(newfollowerListPic)))
            # print(fllwngPic)
            usersDetectedPic.append(fllwngPic)
            
    username = await getUsername(user_id, cookies)

    app = tk.Tk()

    app.geometry("500x430")
    app.iconbitmap(default='Instagram.ico')
    app.title('Lista de Contas - Análise - Boas Festas - João F. B.')

    app.tk.call("source", "azure.tcl")
    app.tk.call("set_theme", "dark")

    app_frame = ttk.Frame(app)
    app_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(app_frame)
    canvas.pack(fill='both', expand=True)

    big_frame = ttk.Frame(canvas)

    scroll = ttk.Scrollbar(canvas, orient='vertical', command=canvas.yview)
    scroll.pack(fill='y', side='right')

    canvas.configure(yscrollcommand=scroll.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    canvas.create_window((0,0), window=big_frame, anchor='nw')

    bold25 = Font(app, size=15, weight=BOLD)

    frame=tk.Frame(big_frame)
    label = ttk.Label(frame, text="Conta: " + username)
    buttonSignOut = ttk.Button(frame, text="Sign Out", command=lambda app=app: signOut(app))
    label1 = ttk.Label(big_frame, text="Número de Seguidores: " + str(len(followerList)), width=60)
    label2 = ttk.Label(big_frame, text="Número de contas que Segues: " + str(len(followingList)))
    label3 = ttk.Label(big_frame, text="Número de contas que não te seguem de volta: " + str(len(usersDetected)))
    label4 = ttk.Label(big_frame, font=bold25, text="CONTAS DESCOBERTAS:")
    
    frame.pack(fill='x')
    label.pack(pady=(20,5), padx=(30,0), side="left")
    buttonSignOut.pack(pady=(20,0), side="right")
    label1.pack(pady=5, padx=(30,0), anchor="w")
    label2.pack(pady=5, padx=(30,0), anchor="w")
    label3.pack(pady=(5,40), padx=(30,0), anchor="w")
    label4.pack(pady=5, padx=(30,0), anchor="w")
    
    images = []
    
    for usersPic in enumerate(usersDetectedPic):
        res = requests.get(usersPic[1])
        
        img = Image.open(BytesIO(res.content))
        img = img.resize((75,75))
        img = ImageTk.PhotoImage(img)
        
        images.append(img)

    for users in enumerate(usersDetected):
        img = images[users[0]]
        
        frame1 = tk.Frame(big_frame)
        
        sep = ttk.Separator(frame1, orient='horizontal')
        label5 = ttk.Label(frame1, image=img, text='    ' +str(users[1]), font=bold25, compound=tk.LEFT)
        button = ttk.Button(frame1, text="UNFOLLOW", style="Accent.TButton")
        button.config(command=lambda buttono=button, user=usersDetectedId[users[0]]: unfollowUser(user, cookies, buttono))
        sep1 = ttk.Separator(frame1, orient='horizontal')
        
        frame1.pack(fill='x', padx=(30,0))
        sep.pack(fill="x", pady=10, side="top")
        sep1.pack(fill='x', pady=10, side="bottom")
        label5.pack(side="left")
        button.pack(side="right")
        
    if (len(usersDetected) == 0):
        frame1 = tk.Frame(big_frame)
        
        sep = ttk.Separator(frame1, orient='horizontal')
        label5 = ttk.Label(frame1, text='Nenhuma Conta Encontrada!')
        sep1 = ttk.Separator(frame1, orient='horizontal')
        
        frame1.pack(fill='x', padx=(30,0))
        sep.pack(fill="x", pady=10, side="top")
        sep1.pack(fill='x', pady=10, side="bottom")
        label5.pack()
    
    await Center(app)
    app.mainloop()
    app.after(1, lambda: app.focus_force())

async def redr(page, brwContext, playwright, browser):
    if (len(await page.query_selector_all("#splash-screen")) > 0):
        # print('Logged into Instagram: ' + page.url)
        cookies = await brwContext.cookies('https://instagram.com')
        # print('Final Instagram Cookies: ' + str(cookies))
        await writeCookiesToDisk(cookies)
        
        await playwright.stop()
        # print('GOOOOOOOOOOO')
        await checkCookies('updated')
        await browser.close()
    else:
        # print('Redirected somewhere else ' + page.url)
        return 0
    return 0

async def closedPage(brwContext, playwright, browser):
    cookies = await brwContext.cookies('https://instagram.com')
    # print('Final Instagram Cookies: ' + str(cookies))
    await writeCookiesToDisk(cookies)
    await browser.close()

    await playwright.stop()

async def stuckinLoopOrMFA(page, brwContext, playwright, browser):
    if('https://www.instagram.com/accounts/login/two_factor' in page.url):
        return
    elif (page.url == 'https://www.instagram.com/#reactivated'):
        cookies = await brwContext.cookies('https://instagram.com')
        # print('Final Instagram Cookies (Reactivated Account): ' + str(cookies))
        await writeCookiesToDisk(cookies)


        await playwright.stop()
        
        await checkCookies('updated')
        await browser.close()
    
async def writeCookiesToDisk(cookies):
    with open('./cookies.json', 'wb') as f:
        f.write(fernet.encrypt(bytes(str(cookies).replace('"', '\\"').replace("'", "\"").replace('False', '"False"').replace('True', '"True"'), encoding='utf-8')))
   
def Confirm(res, app, cookie):
    if (res == 'yes'):
        # print('Destroying window')
        app.quit()
        app.destroy()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(main())
        loop.close()
    elif (res == 'no'):
        # print('Destroying window')
        app.quit()
        # print('start processing...')
        user_id = cookie['ds_user_id']
        cookies = cookie
        app.quit()
        app.destroy()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(startProcessing(user_id, cookies))
        loop.close()
        
async def guiConfirm(cookie, user_id):
    app = tk.Tk()

    app.geometry("355x170")
    app.iconbitmap(default='Instagram.ico')
    app.title('Alterar Conta Instagram?')

    big_frame = ttk.Frame(app)
    big_frame.pack(fill="both", expand=True, padx=40, pady=20)

    app.tk.call("source", "azure.tcl")
    app.tk.call("set_theme", "dark")
    
    label = ttk.Label(big_frame, text="Pretende alterar a conta instagram a analisar?")
    label1 = ttk.Label(big_frame, text="Conta Atual: " + await getUsername(user_id, cookie))
    button = ttk.Button(big_frame, text="Sim", style='Accent.TButton', command=lambda: Confirm('yes', app, cookie))
    button1 = ttk.Button(big_frame, text="Não", command=lambda: Confirm('no', app, cookie))
    label.pack(pady=5)
    label1.pack(pady=5)
    button.pack(side="left", padx=20, pady=15)
    button1.pack(side="right", padx=20, pady=15)

    app.eval('tk::PlaceWindow . center')

    app.mainloop()
    app.after(1, lambda: app.focus_force())

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        brwContext = await browser.new_context()
        page = await brwContext.new_page()
        await page.goto("https://www.instagram.com/")
        # cookies = await brwContext.cookies('https://instagram.com')
        # print('Initial Instagram Cookies: ' + str(cookies))
        await page.bring_to_front()
        try:
            cookieAgreement = page.locator("._a9_0")
            # print(cookieAgreement)
            await cookieAgreement.click()
        except:
            # print('Could not find cookie agreement popup, either due to class change or to the user having already accepted it')
            cookieAgreement = ''
            
        page.on("framenavigated", lambda exec: redr(page, brwContext, playwright, browser) if not(page.url == 'https://www.instagram.com/#reactivated' or 'https://www.instagram.com/accounts/login/two_factor' in page.url) else stuckinLoopOrMFA(page, brwContext, playwright, browser))
        page.on("close", lambda exec: closedPage(brwContext, playwright, browser))
        await asyncio.sleep(500)
        
async def testLogin(cookie, updated):
    # print('HERE')
    try:
        url = f"https://www.instagram.com/graphql/query/"
        variables = {
            "id": cookie['ds_user_id'],
            "first": 5,
            "after": None
        }
        query_hash = "58712303d941c6855d4e888c5f0cd22f"
        headers = {
            "Referer": "https://www.instagram.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "X-Requested-With": "XMLHttpRequest"
        }
        url_final = (url + '?query_hash=' + query_hash + '&variables=' + json.dumps(variables))
        res = requests.get(url_final, headers, cookies=cookie)
        result = json.loads(res.text)['data']['user']['edge_follow']
        # print(result)
        if (result['count'] != 0 and result['edges'] == []):
            # print('Authentication not successful')
            await main()
        else:
            # print('Authentication Successful')
            if(updated != 'updated'):
                await guiConfirm(cookie, cookie['ds_user_id'])
                return
                
            # print('start processing')
            user_id = cookie['ds_user_id']
            cookies = cookie
            await startProcessing(user_id, cookies)
    except Exception as f:
        # print(f)
        # print(traceback.format_exc())
        await main()
    
        
async def checkCookies(updated):
    # print('HEY THERE')
    if not(os.path.exists('./cookies.json')):
        # print('File does not exist')
        await main()
    else:
        f = open('./cookies.json', 'r')
        output = f.read()
        
        if(output != ''):
            f1 = open('./cookies.json', 'rb')
            output = f1.read()
            output = fernet.decrypt(output)
        
        if (output == ''):
            # print('Empty file')
            await main()
            return
        else:
            output = json.loads(output)
            cookie = {}
            
            for i in output:      
                names = i['name']
                values = i['value']

                cookie[names] = values
            
            # print(cookie)
            await testLogin(cookie, updated)
        
asyncio.run(checkCookies(''))
