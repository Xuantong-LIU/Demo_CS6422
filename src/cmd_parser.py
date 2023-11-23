
def read_cmds_to_objects(path):
    objects_array = []

    with open(path, 'r') as file:
        for line in file:
            # 移除每行的前后空白字符，并以空格分割
            parts = line.strip().split()

            # 确保行格式正确
            if len(parts) == 4 and parts[3].lower() == "cpu":
                obj = {
                    "name": parts[0],
                    "operation": parts[1],
                    "number": int(parts[2])  # 将数字字符串转换为整数
                }
                objects_array.append(obj)

    return objects_array
