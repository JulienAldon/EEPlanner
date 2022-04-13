import re

INTRA_LINK = r'intra\.epitech\.eu'

def execRegex(regex, string):
    """Check if regex match in string

    :params regex: A regex
    :type regex: str
    :params string: A string to match the *regex*
    :returns: A boolean, True if *regex* is found in *string* False otherwise
    :rtype: bool
    """
    matches = re.finditer(regex, string, re.MULTILINE)
    for match in matches:
        if match:
            return True
    return False

def check_autologin(autologin):
    """Check Autologin format
    
    :param autologin: An Epitech Intranet autologin url (found under the administration tab on the Epitech intranet) 
    :type autologin: str
    :returns: A correctly formated autologin url if the format is correct, False otherwise
    :rtype: str
    """
    if execRegex(r'^http://', autologin):
        autologin = autologin.replace('http', 'https')
    if execRegex(rf'^{INTRA_LINK}/auth-[0-9a-fA-F]+$', autologin):
        autologin = 'https://' + autologin
        return autologin
    elif execRegex(r'^auth-[0-9a-fA-F]+$', autologin):
        return f'https://intra.epitech.eu/' + autologin
    elif execRegex(rf'^https://{INTRA_LINK}/auth-[0-9a-fA-F]+$', autologin):
        return autologin
    return False

def check_hour_format(hour):
    """Check hour format
    :param hour: Hour format (HH-MM-SS)
    :returns: A boolean, True if the format is correct, False otherwise
    """
    if not execRegex(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$', hour):
        return False
    return True

def check_activity_format(activity):
    """Check intranet activity format

    :param activity:
    """
    reg = r'^/module/[0-9]+/[A-Z-0-9]+/LYN-[0-9-]+/acti-[0-9]+/$'
    if execRegex(reg, activity):
        return True
    return False