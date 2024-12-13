import requests

def try_login(username, password):
    url = 'https://i.instagram.com/api/v1/accounts/login/'
    headers = {
        "User-Agent": "Instagram 100.0.0.17.129 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 161478664)",
        "Accept-Language": "en-US",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "i.instagram.com",
        "Connection": "keep-alive"
    }
    payload = {
        'username': username,
        'password': password,
        'device_id': 'android-1b8d3f3e091d4f4e',
        'login_attempt_count': '0'
    }

    
    response = requests.post(url, headers=headers, data=payload)

    
    if response.status_code == 200:
        
        cookies = response.cookies
        session_id = cookies.get('sessionid')

        
        if session_id:
            print(f"تم تسجيل الدخول بنجاح. SessionID الخاص بك: {session_id}")
            return session_id
        else:
            print("لم يتم العثور على SessionID في ملفات تعريف الارتباط.")
            return None
    else:
        
        print(f"فشل تسجيل الدخول. رمز الحالة: {response.status_code}")
        try:
            error_message = response.json().get('message', 'خطأ غير معروف')
            print(f"الرسالة: {error_message}")
        except ValueError:
            print("لا يمكن تحليل استجابة الخطأ.")
        return None
