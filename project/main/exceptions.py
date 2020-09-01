import json

def getCompanyTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Company variable "+str(data)+" should be json")

    if 'company_name' not in data:
        raise ValueError("No target company_name in given json")
    if 'email_group' not in data:
        raise ValueError("No target email_group in given json")
    if 'ruc' not in data:
        raise ValueError("No target ruc in given json")
    if 'address' not in data:
        raise ValueError("No target address in given json")
    if 'phone' not in data:
        raise ValueError("No target phone in given json")
    if 'contact_person' not in data:
        raise ValueError("No target contact_person in given json")

def getOffsetTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Offset variable "+str(data)+" should be json")

    if 'product_id' not in data:
        raise ValueError("No target product_id in given json")
    if 'offsets' not in data:
        raise ValueError("No target offsets in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

def getControlledOffsetTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Company variable "+str(data)+" should be json") 

    if 'product_id' not in data:
        raise ValueError("No target product_id in given json")
    if 'controlled_offsets' not in data:
        raise ValueError("No target controlled_offsets in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

def getNonControlledOffsetTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Offset variable "+str(data)+" should be json") 

    if 'product_id' not in data:
        raise ValueError("No target product_id in given json")
    if 'non_controlled_offsets' not in data:
        raise ValueError("No target non_controlled_offsets in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

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

def getIncaTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Inca variable "+str(data)+" should be json") 

    if 'name' not in data:
        raise ValueError("No target name in given json")
    if 'value_inca' not in data:
        raise ValueError("No target value_inca in given json")


def getStatusOffTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Qhawax status off variable "+str(data)+" should be json") 

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'qhawax_lost_timestamp' not in data:
        raise ValueError("No target qhawax_lost_timestamp in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")

def getStatusOnTargetofJson(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Qhawax status on variable "+str(data)+" should be json") 

    if 'qhawax_name' not in data:
        raise ValueError("No target qhawax_name in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")
