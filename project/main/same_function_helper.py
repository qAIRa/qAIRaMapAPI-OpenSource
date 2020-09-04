from project import app, db
from project.database.models import  Qhawax, QhawaxInstallationHistory, EcaNoise, Company
import project.main.util_helper as util_helper

session = db.session

""" Helper functions to check one parameter"""

def qhawaxExistBasedOnID(qhawax_id):
    """ Helper function to check if qHAWAX id exist """
    if(type(qhawax_id) not in [int]):
        raise TypeError("qHAWAX id should be int")

    qhawax_list = session.query(Qhawax.name).filter_by(id=qhawax_id).all()
    if(qhawax_list == []):
        return False
    return True

def qhawaxExistBasedOnName(qhawax_name):
    """ Helper function to check if qHAWAX name exist """
    if(isinstance(qhawax_name, str) is not True):  
        raise TypeError("qHAWAX name "+str(qhawax_name)+" should be string")

    qhawax_list = session.query(Qhawax.name).filter_by(name=qhawax_name).all()
    if(qhawax_list == []):
        return False
    return True
        
def qhawaxInstallationExistBasedOnID(installation_id):
    """ Helper function to check if qHAWAX Installation ID exist """
    if(type(installation_id) not in [int]):
        raise TypeError("qHAWAX installation ID "+str(installation_id)+" should be int")

    installation_date_zone = session.query(QhawaxInstallationHistory.installation_date_zone).\
                                     filter_by(id= installation_id).all()
    if(installation_date_zone == []):
        return False
    return True

def areaExistBasedOnID(eca_noise_id):
    """ Helper function to check if Area ID exist """
    if(type(eca_noise_id) not in [int]):
        raise TypeError("Eca noise ID "+str(eca_noise_id) +"should be int")
    area_name = session.query(EcaNoise.area_name).\
                        filter_by(id=eca_noise_id).all()
    if(area_name == []):
        return False
    return True

def companyExistBasedOnName(company_name):
    """ Helper function to check if company name exist """
    if(isinstance(company_name, str) is not True):  
        raise TypeError("Company name "+str(company_name)+" should be string")

    company_list = session.query(Company.name).filter_by(name=company_name).all()
    if(company_list == []):
        return False
    return True

def companyExistBasedOnRUC(ruc):
    """ Helper function to check if company name exist """
    if(isinstance(ruc, str) is not True):  
        raise TypeError("RUC"+str(ruc)+" should be string")

    company_list = session.query(Company.ruc).filter_by(ruc=ruc).all()
    if(company_list == []):
        return False
    return True

""" Helper functions to get one field """

def getQhawaxID(qhawax_name):
    """ Helper function to get qHAWAX ID base on qHAWAX name """
    if(qhawaxExistBasedOnName(qhawax_name)):
        return int(session.query(Qhawax.id).filter_by(name= qhawax_name).first()[0])
    return None

def getInstallationId(qhawax_id):
    """ Helper function to get qHAWAX Installation ID base on qHAWAX ID """
    if(qhawaxExistBasedOnID(qhawax_id)):
        installation_id= session.query(QhawaxInstallationHistory.id).\
                                 filter_by(qhawax_id=qhawax_id).\
                                 filter(QhawaxInstallationHistory.end_date_zone == None). \
                                 all()
        if(installation_id == []):
            return None

        return session.query(QhawaxInstallationHistory.id).\
                       filter_by(qhawax_id=qhawax_id). \
                       filter(QhawaxInstallationHistory.end_date_zone == None). \
                       order_by(QhawaxInstallationHistory.installation_date_zone.desc()).first()[0]
    return None

def getQhawaxName(qhawax_id):
    """ Helper function to get qHAWAX name base on qHAWAX ID """
    if(qhawaxExistBasedOnID(qhawax_id)):
        return session.query(Qhawax.name).filter_by(id =qhawax_id).first()[0]
    return None

def getInstallationIdBaseName(qhawax_name):

    """ Helper function to get qHAWAX Installation ID  
        qHAWAX name could be exist in qHAWAX table, 
        but it could not exist in qHAWAX Installation table """

    if(qhawaxExistBasedOnName(qhawax_name)):
        qhawax_id = getQhawaxID(qhawax_name)
        installation_id = getInstallationId(qhawax_id)
        return installation_id
    return None

def getMainIncaQhawaxTable(qhawax_id):
    """ Helper function to get qHAWAX Main Inca based on qHAWAX ID """
    if(qhawaxExistBasedOnID(qhawax_id)):
        return session.query(Qhawax.main_inca).filter_by(id=qhawax_id).first()[0]
    return None

