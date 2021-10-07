import json


def getCompanyTargetofJson(data):
    data = checkVariable_helper(data, dict)
    array = [
        "company_name",
        "email_group",
        "ruc",
        "address",
        "phone",
        "contact_person",
    ]

    for i in range(len(array)):
        if array[i] not in data:
            raise ValueError("No target " + array[i] + " in given json")


def getQhawaxTargetofJson(data):
    data = checkVariable_helper(data, dict)

    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")
    if "qhawax_type" not in data:
        raise ValueError("No target qhawax_type in given json")
    if "person_in_charge" not in data:
        raise ValueError("No target person_in_charge in given json")
    if "description" not in data:
        raise ValueError("No target description in given json")

    return (
        str(data["qhawax_name"]),
        str(data["qhawax_type"]),
        str(data["person_in_charge"]),
        str(data["description"]),
    )


def getIncaTargetofJson(data):
    data = checkVariable_helper(data, dict)

    if "name" not in data:
        raise ValueError("No target name in given json")
    if "value_inca" not in data:
        raise ValueError("No target value_inca in given json")

    return str(data["name"]).strip(), int(data["value_inca"])


def getStatusOffTargetofJson(data):
    data = checkVariable_helper(data, dict)

    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")

    return str(data["qhawax_name"]).strip()


def getChangeCalibrationFields(data):
    data = checkVariable_helper(data, dict)

    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")
    if "person_in_charge" not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data["qhawax_name"]).strip(), str(data["person_in_charge"])


def getEndCalibrationFields(data):
    data = checkVariable_helper(data, dict)

    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")
    if "person_in_charge" not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data["qhawax_name"]).strip(), str(data["person_in_charge"])


def getInstallationFields(data):
    data = checkVariable_helper(data, dict)

    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")
    if "person_in_charge" not in data:
        raise ValueError("No target person_in_charge in given json")

    return str(data["qhawax_name"]), str(data["person_in_charge"])


def validEndWorkFieldJson(data):
    data = checkVariable_helper(data, dict)
    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")
    if "end_date" not in data:
        raise ValueError("No target end_date in given json")
    if "person_in_charge" not in data:
        raise ValueError("No target person_in_charge in given json")

    return (
        str(data["qhawax_name"]),
        data["end_date"],
        str(data["person_in_charge"]),
    )


def getQhawaxSignalJson(data):
    data = checkVariable_helper(data, dict)

    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")
    if "timestamp_turn_on_conection" not in data:
        raise ValueError("No target timestamp_turn_on_conection in given json")

    return str(data["qhawax_name"]).strip(), str(
        data["timestamp_turn_on_conection"]
    )


def checkVariable_helper(variable, type):
    """
    helper function for checking the five types of variables: list, dictionary, string, integer, float

    Parametres: 
    variable: variable to check
    type: list / dict / str / int / float

    """
    if isinstance(variable, type) is not True:
        raise TypeError(f"Variable {str(variable)} should be {str(type)}")
    return variable


def getJsonOfTakeOff(data):
    data = checkVariable_helper(data, dict)
    if "flight_start" not in data:
        raise ValueError("No target flight_start in given json")
    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")

    return data["flight_start"], str(data["qhawax_name"])


def getJsonOfLanding(data):
    data = checkVariable_helper(data, dict)
    if "flight_end" not in data:
        raise ValueError("No target flight_end in given json")
    if "qhawax_name" not in data:
        raise ValueError("No target qhawax_name in given json")
    if "flight_detail" not in data:
        raise ValueError("No target flight_detail in given json")
    if "location" not in data:
        raise ValueError("No target location in given json")

    return (
        data["flight_end"],
        str(data["qhawax_name"]),
        str(data["flight_detail"]),
        data["location"],
    )
