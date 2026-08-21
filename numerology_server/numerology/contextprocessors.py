import os

def context_processor(request):
    username=os.getlogin() if hasattr(os, 'getlogin') else 'Manian'
    #Make first character upper case
    username=username[0].upper() + username[1:] if username else "Manian"
    lastname=username[0].upper() if username else "M"

    configuration_dict = {
        'username': username,
        'lastname': lastname
    }
    
    return configuration_dict
