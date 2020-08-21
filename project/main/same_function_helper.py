import datetime
import dateutil
import dateutil.parser
import time
from project import app, db, socketio
from project.database.models import  Qhawax, QhawaxInstallationHistory, EcaNoise
import project.main.util_helper as util_helper

session = db.session

def verifyIfQhawaxExistBaseOnID(qhawax_id):
    if(type(qhawax_id) not in [int]):
        raise TypeError("The qHAWAX id should be int")
    qhawax_list = session.query(Qhawax.name).filter_by(id=qhawax_id).all()
    if(qhawax_list == []):
        raise TypeError("The qHAWAX ID "+str(qhawax_id)+" has not been found")
    return True

def verifyIfQhawaxInstallationExistBaseOnID(installation_id):
    if(type(installation_id) not in [int]):
        raise TypeError("The qHAWAX installation ID "+str(installation_id)+" should be int")
    installation_date_zone = session.query(QhawaxInstallationHistory.installation_date_zone).\
                                     filter_by(id= installation_id).all()
    if(installation_date_zone == []):
        raise TypeError("The qHAWAX installation ID "+str(installation_id)+" has not been found")
    return True

def verifyIfAreaExistBaseOnID(eca_noise_id):
    if(type(eca_noise_id) not in [int]):
        raise TypeError("The ID "+str(eca_noise_id) +"should be int")
    area_name = session.query(EcaNoise.area_name).\
                        filter_by(id=eca_noise_id).all()
    if(area_name == []):
        raise TypeError("The area ID " + str(eca_noise_id)+" has not been found")
    return True

def getQhawaxID(qhawax_name):
    """
    Helper function to get qHAWAX ID base on qHAWAX name

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        qhawax_list = session.query(Qhawax.id).filter_by(name= qhawax_name).all()
        if(qhawax_list == []):
            raise TypeError("The qHAWAX name "+str(qhawax_name)+" has not been found")
        qhawax_id = session.query(Qhawax.id).filter_by(name= qhawax_name).first()[0]
        return qhawax_id
    else:
        raise TypeError("The qHAWAX name "+str(qhawax_name)+" should be string")

def getQhawaxName(qhawax_id):
    """
    Helper function to get qHAWAX name base on qHAWAX ID

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(verifyIfQhawaxExistBaseOnID(qhawax_id)==True):
        return session.query(Qhawax.name).filter_by(id =qhawax_id).first()[0]


def getInstallationId(qhawax_id):
    if(type(qhawax_id) not in [int]):
        raise TypeError("The qHAWAX id "+str(qhawax_id)+" should be int")
    installation_id= session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date_zone == None). \
                                    order_by(QhawaxInstallationHistory.installation_date_zone.desc()).all()
    if(installation_id == []):
        return None

    return session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date_zone == None). \
                                    order_by(QhawaxInstallationHistory.installation_date_zone.desc()).first()[0]

def getInstallationIdBaseName(qhawax_name):
    qhawax_id = getQhawaxID(qhawax_name)
    installation_id = getInstallationId(qhawax_id)
    return installation_id

def getMainIncaQhawaxTable(qhawax_id):
    """
    Get qHAWAX Main Inca

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(verifyIfQhawaxExistBaseOnID(qhawax_id)==True):
        return session.query(Qhawax.main_inca).filter_by(id=qhawax_id).first()[0]

