import re
def validate_rg(rg: str):
    pattern = r"^\d{1,2}\.?\d{3}\.?\d{3}-?[\dXx]$"
    if not re.match(pattern, rg):
        return False
    return True