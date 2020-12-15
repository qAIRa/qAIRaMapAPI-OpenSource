import json

def getCompanyTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Company variable "+str(data)+" should be json")

    array = ['company_name','email_group','ruc','address','phone','contact_person']

    for i in range(len(array)):
        if array[i] not in data:
            raise ValueError("No target "+array[i]+" in given json")

def getQhawaxTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Qhawax variable "+str(data)+" should be json") 

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'qhawax_type' not in data:
        raise ValueError("No target qhawax_type in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")

    return str(data['qhawax_name']),str(data['qhawax_type']),\
           str(data['person_in_charge']), str(data['description'])

def getIncaTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Inca variable "+str(data)+" should be json") 

    if 'name' not in data:
        raise ValueError("No target name in given json")
    if 'value_inca' not in data:
        raise ValueError("No target value_inca in given json")

    return str(data['name']).strip(),data['value_inca']

def getStatusOffTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Qhawax status off variable "+str(data)+" should be json") 

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'qhawax_lost_timestamp' not in data:
        raise ValueError("No target qhawax_lost_timestamp in given json")

    return str(data['qhawax_name']).strip(), data['qhawax_lost_timestamp']

def getChangeCalibrationFields(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Calibration json variable "+str(data)+" should be json")

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")

    return str(data['qhawax_name']).strip(), str(data['person_in_charge']), str(data['description'])

def getEndCalibrationFields(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Calibration json variable "+str(data)+" should be json")

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data['qhawax_name']).strip(), str(data['person_in_charge'])

def getInstallationFields(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("qHAWAX Installation variable "+str(data)+" should be json")

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data['qhawax_name']), str(data['person_in_charge'])

def validEndWorkFieldJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("qHAWAX Installation variable "+str(data)+" should be json")

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'end_date' not in data:
        raise ValueError("No target end_date in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data['qhawax_name']), data['end_date'], str(data['person_in_charge'])

def getCompanyTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Company variable "+str(data)+" should be json")

    if 'company_name' not in data:
        raise ValueError("No target company_name in given json")
    if 'email_group' not in data:
        raise ValueError("No target email_group in given json")
    if 'ruc' not in data:
        raise ValueError("No target ruc in given json")
    if 'phone' not in data:
        raise ValueError("No target phone in given json")
    if 'contact_person' not in data:
        raise ValueError("No target contact_person in given json")
    if 'address' not in data:
        raise ValueError("No target address in given json")

def getQhawaxSignalJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Signal variable "+str(data)+" should be json") 

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'timestamp_turn_on_conection' not in data:
        raise ValueError("No target timestamp_turn_on_conection in given json")

    return str(data['qhawax_name']).strip(),str(data['timestamp_turn_on_conection'])