import project.database.exceptions as exceptions
from project.database.models import Company

MIN_PASSWORD_LENGTH = 8
#BANNED_EMAIL_GROUPS = ['gmail.com', 'hotmail.com']
BANNED_EMAIL_GROUPS = ['hotmail.com']
def getEmailGroup(email):
    # Slice email and get everything after the '@' symbol
    return email[email.find('@')+1:]

def checkEmailIsFromCompany(email, name, email_group):
    if getEmailGroup(email) != email_group:
        raise exceptions.EmailNotFromCompanyError(name, email)

def checkValidLocation(location):
    if not isinstance(location, Location):
        raise exceptions.LocationInvalidError(location)
    
def checkValidCompany(company):
    if not isinstance(company, Company):
        raise exceptions.CompanyInvalidError(company)
    
def checkValidEmailGroup(email_group):
    if email_group in BANNED_EMAIL_GROUPS:
        raise exceptions.EmailGroupBannedError(email_group)
