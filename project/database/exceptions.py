class CompanyInvalidError(TypeError):
    pass

class LocationInvalidError(TypeError):
    pass

class EmailGroupBannedError(ValueError):
    pass

class EmailNotFromCompanyError(ValueError):
    pass

class PasswordTooShortError(ValueError):
    pass
