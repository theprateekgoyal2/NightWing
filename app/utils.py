from flask_mail import Message
import re
import phonenumbers
from flask_jwt_extended import decode_token
from phonenumbers import country_code_for_region
from app.extensions import mail
from app.models.auth import User
 
def send_email_to_user(email, message):
    
    recipients = [email]

    # Creating the message
    msg = Message("Hello there!", sender = "djangoprojekts@gmail.com", recipients=recipients)
    msg.body = message
    mail.send(msg)
    return "Email sent"

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
    if (re.fullmatch(regex, email)):
        return True
    return False

def validate_number(phoneNum):
    my_string_number = phoneNum
    my_number = phonenumbers.parse(my_string_number)
    return phonenumbers.is_valid_number(my_number)

def abbreviationFunc(name: str, year: int) -> str:
    name = name.strip()
    list = name.split()
    resString = f'{year}-'
    if len(list) != 1:
        for item in list:
            if item in ["and", "or", "&"]:
                continue
            resString += item[0].capitalize()
    else:
        resString += name
    
    return resString

def generate_filename(code: str, totalItems: int) -> str:
    if totalItems<10:
        name = f'{code}:00{totalItems+1}'
    else:
        name = f'{code}:0{totalItems+1}'

    return name

def sanitize_category(name: str) -> str:
    res = name.capitalize()
    res = res.replace(" ", "")
    res = res.strip()
    if res.strip()[-1] == ".":
        res = res[:-1]

    return res

def sanitize_name(name: str) -> str:
    list = name.split()
    resString = ""
    for item in list:
        resString += f'{item.capitalize()} '
    
    resString = resString.strip()
    if resString.strip()[-1] == ".":
        resString = resString[:-1]
    return resString

def sanitize_subProd(name: str) -> str:
    res = name.capitalize()
    res = res.strip()
    if res in ["Polaroids", "Polaroid"]:
        res = "Polaroids"
    elif res in ["Posters", "Poster"]:
        res = "Posters"
    return res


def get_user_id(token):
    data = decode_token(token)
    current_user = User.query.filter_by(public_id=data['sub']).first()
    return current_user.id if current_user else None