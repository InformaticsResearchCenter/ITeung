def fetchOneMode(data, cursor):
    if data != None:
        fields = map(lambda x: x[0], cursor.description)
        result = dict(zip(fields, data))
    else:
        result = None
    return result

def fetchAllMode(data, cursor):
    if data != ():
        desc = cursor.description
        column_names = [col[0] for col in desc]
        result = [dict(zip(column_names, row))
                for row in data]
        return result
    else:
        return None