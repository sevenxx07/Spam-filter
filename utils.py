def read_classification_from_file(file_name):
    try:
        with open(file_name, 'r', encoding="utf-8") as file,\
            open(file_name, 'a', encoding='utf-8') as fwrite:
            content = file.read()
    except FileNotFoundError:
        print('File not found')
        return
    array = content.strip().split()
    values = []
    for item in array:
        if item == 'OK' or item == 'SPAM':
            values.append(item)
            array.remove(item)
    dictionary = {}
    for i in range(len(array)):
        dictionary[array[i]] = values[i]
 
    return dictionary
