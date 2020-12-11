import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper
from project import app, db
from project.database.models import Qhawax, EcaNoise, QhawaxInstallationHistory, \
                                    Company, ProcessedMeasurement, ValidProcessedMeasurement
session = db.session

columns_qhawax = (Qhawax.name, Qhawax.mode,Qhawax.state,Qhawax.qhawax_type,Qhawax.main_inca, 
                  QhawaxInstallationHistory.id, QhawaxInstallationHistory.qhawax_id,
                  QhawaxInstallationHistory.eca_noise_id, QhawaxInstallationHistory.comercial_name, 
                  QhawaxInstallationHistory.lat, QhawaxInstallationHistory.lon, EcaNoise.area_name)

def queryQhawaxModeCustomer():
    """ Get qHAWAX list in mode Customer and state ON """
    return session.query(*columns_qhawax).\
                   join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                   join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                   group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                   filter(Qhawax.mode =="Cliente", \
                          Qhawax.state =="ON", \
                          QhawaxInstallationHistory.end_date_zone == None).order_by(Qhawax.id).all()

def queryGetAreas():
    """ Helper Eca Noise function to list all zones  """
    fields = (EcaNoise.id, EcaNoise.area_name)
    areas = session.query(*fields).all()
    return None if (areas is []) else session.query(*fields).order_by(EcaNoise.id.desc()).all()

def queryGetEcaNoise(eca_noise_id):
    """ Helper Eca Noise function to get zone description """
    fields = (EcaNoise.id, EcaNoise.area_name, EcaNoise.max_daytime_limit, \
              EcaNoise.max_night_limit)
    if(same_helper.areaExistBasedOnID(eca_noise_id)):
        return session.query(*fields).filter_by(id= eca_noise_id).first()
    return None

def getInstallationDate(qhawax_id):
    """ Helper qHAWAX function to get Installation Date """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id is not None):
        return session.query(QhawaxInstallationHistory.installation_date_zone).\
                       filter(QhawaxInstallationHistory.id == installation_id).first()[0]
    return None

def getFirstTimestampValidProcessed(qhawax_id):
    """ Helper qHAWAX Installation function to get first timestamp of Valid Processed  """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id is not None):
        first_timestamp =session.query(ValidProcessedMeasurement.timestamp_zone). \
                                 filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                 order_by(ValidProcessedMeasurement.timestamp_zone.asc()).first()
        return None if (first_timestamp==None) else first_timestamp[0]
    return None

def isItFieldQhawax(qhawax_name):
    """Check qhawax in field """
    return True if (same_helper.getInstallationIdBaseName(qhawax_name)is not None) else False

def getLatestTimeInProcessedMeasurement(qhawax_name):
    """ Helper qHAWAX function to get latest timestamp in UTC 00 from Processed Measurement """

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        processed_measurement_timestamp=""
        qhawax_time = session.query(ProcessedMeasurement.timestamp_zone).\
                              filter_by(qhawax_id=qhawax_id).first()
        if(qhawax_time!=None):
            processed_measurement_timestamp = session.query(ProcessedMeasurement.timestamp_zone).\
                                                      filter_by(qhawax_id=qhawax_id).\
                                                      order_by(ProcessedMeasurement.id.desc()).\
                                                      first().timestamp_zone
        return processed_measurement_timestamp
    return None

def queryQhawaxInFieldInPublicMode():
    """ Get list of qHAWAXs in field in public mode """
    return session.query(*columns_qhawax).\
                   join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                   join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                   group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                   filter(QhawaxInstallationHistory.is_public == 'si'). \
                   filter(QhawaxInstallationHistory.end_date_zone == None). \
                   order_by(Qhawax.id).all() 

def getNoiseData(qhawax_name):
    """Helper Processed Measurement function to get Noise Area Description"""
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        eca_noise_id = session.query(QhawaxInstallationHistory.eca_noise_id).\
                               filter_by(id=installation_id).first()
        return session.query(EcaNoise.area_name).filter_by(id=eca_noise_id).first()[0]
    return None

def getHoursDifference(qhawax_id):
    """Helper Processed Measurement function to get minutes difference
      between last_registration_time and last_time_physically_turn_on """
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        values = session.query(QhawaxInstallationHistory.last_time_physically_turn_on_zone, \
                               QhawaxInstallationHistory.last_registration_time_zone).\
                         filter(QhawaxInstallationHistory.qhawax_id == qhawax_id).first()
        if(values!=None):
            if (values[0]!=None and values[1]!=None):
                minutes_difference = int((values[0] - values[1]).total_seconds() / 60)
                return minutes_difference, values[0]
    return None, None

def getMainIncaQhawax(name):
    installation_id=same_helper.getInstallationIdBaseName(name)
    if(installation_id is not None):
      qhawax_list = session.query(QhawaxInstallationHistory.main_inca).filter_by(id=installation_id).all()
      if(qhawax_list == []):
          return None
      return session.query(QhawaxInstallationHistory.main_inca).filter_by(id=installation_id).one()[0]
    return None

def getLastValuesOfQhawax(qH_name):
    if(isItFieldQhawax(qH_name) == True):
        mode = "Cliente"
        description="Se cambió a modo cliente"
        main_inca = 0
    else:
        mode = "Stand By"
        description="Se cambió a modo stand by"
        main_inca = -1

    return mode, description, main_inca
