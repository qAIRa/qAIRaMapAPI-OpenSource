from project import app, db
from project.database.models import  Qhawax, QhawaxInstallationHistory, EcaNoise, Company
import project.main.util_helper as util_helper
import project.main.exceptions as exceptions

session = db.session

""" Helper functions to check one parameter"""
def qhawaxExistBasedOnID(qhawax_id):
    """ Helper function to check if qHAWAX id exist """
    qhawax_id = exceptions.checkIntegerVariable(qhawax_id)
    qhawax_list = session.query(Qhawax.name).filter_by(id=qhawax_id).all()
    if(qhawax_list == []):
        return False
    return True

def qhawaxExistBasedOnName(qhawax_name):
    """ Helper function that checks if qHAWAX name exist """
    qhawax_name = exceptions.checkStringVariable(qhawax_name)
    qhawax_list = session.query(Qhawax.name).filter_by(name=qhawax_name).all()
    if(qhawax_list == []):
        return False
    return True

def qhawaxInstallationExistBasedOnID(installation_id):
    """ Helper function to check if qHAWAX Installation ID exist """
    installation_id = exceptions.checkIntegerVariable(installation_id)
    installation_date_zone = session.query(QhawaxInstallationHistory.installation_date_zone).\
                                     filter_by(id= installation_id).all()
    if(installation_date_zone == []):
        return False
    return True

def areaExistBasedOnID(eca_noise_id):
    """ Helper function to check if Area ID exist """
    eca_noise_id = exceptions.checkIntegerVariable(eca_noise_id)
    area_name = session.query(EcaNoise.area_name).\
                        filter_by(id=eca_noise_id).all()
    if(area_name == []):
        return False
    return True

def companyExistBasedOnName(company_name):
    """ Helper function to check if company name exist """
    company_name = exceptions.checkStringVariable(company_name)
    company_list = session.query(Company.name).filter_by(name=company_name).all()
    if(company_list == []):
        return False
    return True

def companyExistBasedOnRUC(ruc):
    """ Helper function to check if company name exist """
    ruc = exceptions.checkStringVariable(ruc)
    company_list = session.query(Company.ruc).filter_by(ruc=ruc).all()
    if(company_list == []):
        return False
    return True

""" Helper functions to get one field """

def getQhawaxID(qhawax_name):
    """ Helper function to get qHAWAX ID based on qHAWAX name """
    if(qhawaxExistBasedOnName(qhawax_name)):
        return int(session.query(Qhawax.id).filter_by(name= qhawax_name).first()[0])
    return None

def getInstallationId(qhawax_id):
    """ Helper function that gets qHAWAX Installation ID base on qHAWAX ID """
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
    """ Helper function that gets qHAWAX Installation ID based on qHAWAX name """
    if(qhawaxExistBasedOnName(qhawax_name)):
        qhawax_id = getQhawaxID(qhawax_name)
        return getInstallationId(qhawax_id)
    return None

def getMainIncaQhawaxTable(qhawax_name):
    """ Helper function to get qHAWAX Main Inca based on qHAWAX name """
    if(qhawaxExistBasedOnName(qhawax_name)):
        return session.query(Qhawax.main_inca).filter_by(name=qhawax_name).first()[0]
    return None

def getQhawaxMode(qhawax_name):
    """ Get qHAWAX mode based on name """
    if(qhawaxExistBasedOnName(qhawax_name)):
        return session.query(Qhawax.mode).filter_by(name=qhawax_name).first()[0]
    return None

def getTimeQhawaxHistory(qhawax_name):
    fields = (QhawaxInstallationHistory.last_time_physically_turn_on_zone,
              QhawaxInstallationHistory.last_registration_time_zone)

    installation_id = getInstallationIdBaseName(qhawax_name)

    if(installation_id is not None):
        values= session.query(*fields).filter(QhawaxInstallationHistory.id == installation_id).first()
        if (values!=None):
            return {'last_time_on': values[0], 'last_time_registration': values[1]}
    return None

def getQhawaxStatus(qhawax_name):
    if(qhawaxExistBasedOnName(qhawax_name)):
        return session.query(Qhawax.state).filter_by(name=qhawax_name).one()[0]
    return None

def getComercialName(qhawax_name):
    """ Helper Processed Measurement function to get qHAWAX comercial name """
    qhawax_installation_id = getInstallationIdBaseName(qhawax_name)
    if(qhawax_installation_id!= None):
        return session.query(QhawaxInstallationHistory.comercial_name).filter_by(id=qhawax_installation_id).one()[0]
    return qhawax_name

def getQhawaxOnLoop(qhawax_name):
    if(qhawaxExistBasedOnName(qhawax_name)):
        return session.query(Qhawax.on_loop).filter_by(name=qhawax_name).one()[0]
    return None

def qhawaxQueryUpdateFilterByQhawaxName(json, qhawax_name):
    if(qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values=json)
        session.commit()

def qhawaxQueryUpdateFilterByQhawaxId(json, qhawax_id):
    if(qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(id=qhawax_id).update(values=json)
        session.commit()

def qhawaxInstallationQueryUpdate(json, qhawax_name):
    installation_id=getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values=json)
        session.commit()
