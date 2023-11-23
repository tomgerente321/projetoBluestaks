import random, requests
from bs4 import BeautifulSoup

class MailoAdapter:
    inbox = None
    def __init__(self) -> None:
        self.mail_address = self.gen_random_email()

    def get_res(self):
        url = 'https://tempmailo.com/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Request failed with status code {response.status_code}')
        return response

    def get_req_verify(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find('input', {'name': '__RequestVerificationToken'})['value']

    def get_anti_forgery_cookie(self, cookies):
        return cookies.split(";")[0] + ";"

    def get_emails(self, email):
        res = self.get_res()
        verify_token = self.get_req_verify(res.text)
        anti_forgery_cookie = self.get_anti_forgery_cookie(res.headers['set-cookie'])
        headers = {
            'RequestVerificationToken': verify_token,
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://tempmailo.com',
            'Content-Type': 'application/json;charset=UTF-8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Cookie': anti_forgery_cookie
        }
        data = {'mail': email}
        response = requests.post('https://tempmailo.com/', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def random_string(self, length, chars):
        result = ''
        for i in range(length):
            result += random.choice(chars)
        return result
    
    def gen_random_email(self):
        email_domains = ["mailo.icu"]
        random_name = self.random_string(random.randint(5, 8), 'abcdefghijklmnopqrstuvwxyz')
        email = f"{random_name}@{email_domains[random.randint(0, len(email_domains)-1)]}"
        return email
    
    def getEmailAddress(self):
        return self.mail_address
    
    def getMessages(self):
        messages = self.get_emails(self.mail_address)
        print(messages)
        if len(messages):
            return Inbox(messages[0]['subject'], messages[0]['text'])
        return None
    

class Inbox:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
    
    def __repr__(self) -> str:
        return f"<Mailo; subject='{self.subject}', body='{self.body}'>"