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

def checkPasswordLength(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        raise exceptions.PasswordTooShortError(password)

def checkValidLocation(location):
    if not isinstance(location, Location):
        raise exceptions.LocationInvalidError(location)
    
def checkValidCompany(company):
    if not isinstance(company, Company):
        raise exceptions.CompanyInvalidError(company)
    
def checkValidEmailGroup(email_group):
    if email_group in BANNED_EMAIL_GROUPS:
        raise exceptions.EmailGroupBannedError(email_group)

class Location(object):
    def __init__(self, lat, lon):
        if not isinstance(lat, int) and not isinstance(lat, float):
            raise TypeError(lat)
        if not isinstance(lon, int) and not isinstance(lon, float):
            raise TypeError(lon)
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '%s(lat=%f, lon=%f)' % (
            self.__class__.__name__, self.lat, self.lon)

    @property
    def serialize(self):
        return {'lat': self.lat, 'lon': self.lon}
