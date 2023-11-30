# parsing each lines of the txt file
def read_cmds_to_objects(path):
    objects_array = []

    with open(path, 'r') as file:
        for line in file:
            parts = line.strip().split()

            if len(parts) == 4 and parts[3].lower() == "cpu":
                obj = {
                    "name": parts[0],
                    "operation": parts[1],
                    "number": int(parts[2])
                }
                objects_array.append(obj)

    return objects_array
