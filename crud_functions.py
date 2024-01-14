import shelve


def retrieve_db(db_file, unique_key):
    temp = {}
    temp_list = []
    db = shelve.open(db_file, 'r')
    try:
        temp = db[unique_key]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    for key in temp:
        value = temp.get(key)
        temp_list.append(value)
    db.close()
    return temp_list


def extracting(my_db, db_key, id):  # function for deleting and taking out the deleted value
    form_dict = {}
    db = shelve.open(my_db, 'w')
    form_dict = db[db_key]
    if form_dict:
        item = form_dict.pop(id)
        db[db_key] = form_dict
        db.close()
        return item
    return form_dict



