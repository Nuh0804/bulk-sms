import requests
class SMSUtils:
    KANNEL_URL = "http://127.0.0.1:14000/cgi-bin/sendsms"
    USERNAME = "foo"
    PASSWORD = "bar"

    @classmethod
    def send_sms(cls, phone, message):
        try:
            payload = {
                "username": cls.USERNAME,
                "password": cls.PASSWORD,
                "to": phone,
                "text": message,
                "from": "KILAKONA",
                "smsc": "KilaKona",
                "dlr-mask" : 31
            }

            return requests.get(cls.KANNEL_URL, params=payload)
            
        except Exception as e:
            print(e)
            return