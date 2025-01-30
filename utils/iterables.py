
def replace(obj_to_replace, objects):
    for index, obj in enumerate(objects):
        if obj['id'] == obj_to_replace['id']:
            objects[index] = obj_to_replace
            break  