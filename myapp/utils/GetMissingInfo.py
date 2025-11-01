from flask import Request
from typing import Dict, Tuple, Any, List

def get_missing_info(
    request:Request,
    datakey:List[str],
    nullAbleValues:List[str],
) -> Tuple[Dict[str, Any], int]:
    data = {}
    missingInfo = []
    for requiredData in datakey:
        value = request.form.get(requiredData, None) if requiredData not in ["photo", "photos"] else request.files.get(requiredData, None)
        if ((value == "" or value is None) and (requiredData not in nullAbleValues)):
            missingInfo.append(requiredData)
        else:
            data[requiredData] = value

    if missingInfo:
        return {
                "Type":                "InputError",
                "content":             "Complete all the inputs",
                "MissingInformation":  missingInfo
            }, 400
    return data, 200