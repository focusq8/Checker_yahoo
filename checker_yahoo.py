import requests
import requests.exceptions
from bs4 import BeautifulSoup 
from concurrent.futures import ThreadPoolExecutor 

Availabe = []

def validator(one_email):
    try:
        email_no_at = one_email.split('@')[0]
        url = 'https://login.yahoo.com/account/create'
        req = requests.Session()
        get_requests = req.get(url,timeout=30).text
        get_form = BeautifulSoup(get_requests,'html.parser').find('form')
        get_action = get_form['action']
        get_input = get_form.findAll('input')

        data_email = {
            "browser-fp-data":"",
            "specId":"yidreg",
            "cacheStored":"",
            "crumb":get_input[3]['value'],
            "acrumb":get_input[4]['value'],
            "sessionIndex":get_input[5]['value'],
            "done":"https%3A%2F%2Fwww.yahoo.com",
            "googleIdToken":"",
            "authCode":"",
            "attrSetIndex":"0",
            "tos0":"oath_freereg%7Cid%7Cid-ID",
            "firstName":"Yutix",
            "lastName":"Yutixcode",
            "yid":email_no_at,
            "password":"Salems1990",
            "shortCountryCode":"ID",
            "phone":"82321062760",
            "mm":"1",
            "dd":"1",
            "yyyy":"1990",
            "freeformGender":"",
            "signup":""}
        post_requests = req.post(get_action,data=data_email,timeout=30).text
        get_message = BeautifulSoup(post_requests,'html.parser').find('div',{'class':'oneid-error-message'})
        
        if get_message != None:
            print(f'UnAvailabe {one_email}')
        else:
            print(f'Availabe {one_email}')
            Availabe.append(one_email)
            
    except requests.exceptions.ReadTimeout:
        print(f'[....] {one_email} | error waitting')
    except requests.exceptions.ConnectionError:
        print(f'[....] {one_email} | error connecting')

def multi(path):
    
    with open(path,'r') as mail:
        with ThreadPoolExecutor(max_workers=20) as threading:
            lines = mail.readlines()
            for line in lines:
                threading.submit(validator,line.strip())
    print(f'\nAvailabe:{len(Availabe)}')
    print(f"Save file as:'Availabe.txt'")
    for maill in Availabe:
        with open('Availabe.txt','a') as vulnsave:
            vulnsave.write(f'{maill}\n')
    
if __name__=='__main__':
    choose = input("""
1. check one email

2. check list emails


Choose number please: """)
    if choose == '1':
        
        validator(input("Enter your email: "))

    elif choose == '2':
        multi(input("Enter your file list: "))
    else:
        exit(f'\nexit')