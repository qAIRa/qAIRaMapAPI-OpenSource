import json

def getCompanyTargetofJson(data):
    data = checkDictionaryVariable(data)
    array = ['company_name','email_group','ruc','address','phone','contact_person']

    for i in range(len(array)):
        if array[i] not in data:
            raise ValueError("No target "+array[i]+" in given json")

def getQhawaxTargetofJson(data):
    data = checkDictionaryVariable(data)

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
    data = checkDictionaryVariable(data) 

    if 'name' not in data:
        raise ValueError("No target name in given json")
    if 'value_inca' not in data:
        raise ValueError("No target value_inca in given json")

    return str(data['name']).strip(),int(data['value_inca'])

def getStatusOffTargetofJson(data):
    data = checkDictionaryVariable(data) 

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'qhawax_lost_timestamp' not in data:
        raise ValueError("No target qhawax_lost_timestamp in given json")

    return str(data['qhawax_name']).strip(), data['qhawax_lost_timestamp']

def getChangeCalibrationFields(data):
    data = checkDictionaryVariable(data)

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data['qhawax_name']).strip(), str(data['person_in_charge'])

def getEndCalibrationFields(data):
    data = checkDictionaryVariable(data)

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data['qhawax_name']).strip(), str(data['person_in_charge'])

def getInstallationFields(data):
    data = checkDictionaryVariable(data)

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data['qhawax_name']), str(data['person_in_charge'])

def validEndWorkFieldJson(data):
    data = checkDictionaryVariable(data)
    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'end_date' not in data:
        raise ValueError("No target end_date in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data['qhawax_name']), data['end_date'], str(data['person_in_charge'])

def getQhawaxSignalJson(data):
    data = checkDictionaryVariable(data)

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'timestamp_turn_on_conection' not in data:
        raise ValueError("No target timestamp_turn_on_conection in given json")

    return str(data['qhawax_name']).strip(),str(data['timestamp_turn_on_conection'])

def checkIntegerVariable(variable):
    if(type(variable) not in [int]):
        raise TypeError("Variable "+str(variable)+" should be int")
    return variable

def checkStringVariable(variable):
    if(isinstance(variable, str) is not True):  
        raise TypeError("Variable "+str(variable)+" should be string")
    return variable

def checkFloatVariable(variable):
    if(type(variable) not in [float]):
        raise TypeError("Variable "+str(variable)+" should be float")
    return variable

def checkDictionaryVariable(variable):
    if(isinstance(variable, dict) is not True):
        raise TypeError("Variable "+str(variable)+" should be Json")
    return variable