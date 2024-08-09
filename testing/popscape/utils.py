def check_id(id):
    return '' if id=='id' else id

def generate_category_params(id):
    return {"id": id}

def check_sid(id):
    return '' if id=='sid' else id

def generate_subcategory_params(sid):
    return {"sid": sid}