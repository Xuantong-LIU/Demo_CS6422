import config


# check user 是否具有release的权限
def check_user_and_cpu(items_list, user, relasenum):
    for item in items_list:
        if item["username"] == user and item["realCPU"] == relasenum:
            return item
    return False


# request operation
def process_request(user, request_cpu):
    config.remaining_cpu
    allocated_cpu_single = request_cpu

    # 判断当前模式, 确定实际分配给user的cpu
    if config.overbooking == True:
        allocated_cpu_single *= config.fraction_value

    # 当前不在overbooking 但执行完request有可能进入
    else:
        # if request_cpu + config.allocated_cpu < config.alarm_rate:
        #     allocated_cpu_single = request_cpu # 其实啥也没做 ===

        # 不处于overbooking mode 但是有一种临界情况：下一次进入overbooking(这里讨论两种情况)
        if config.allocated_cpu + allocated_cpu_single >= config.alarm_rate:
            allocated_cpu_single *= config.fraction_value
            config.overbooking = True

    # 判断当前剩余资源是否足够分配
    if config.remaining_cpu < allocated_cpu_single:  # 不足
        return (f"ERR --> OUT OF RESORUCE: {user} request for {request_cpu} CPU, remaing CPU is {config.remaining_cpu}\n", True)

    # 基于此次分配结果，对overbooking mode进行更新
    # refresh_overbooking_request(allocated_cpu_single)

    # 进行分配
    config.remaining_cpu -= allocated_cpu_single
    config.allocated_cpu += allocated_cpu_single

    # 记录userX 此次的request
    item = {"username": user, "realCPU": request_cpu,
            "allocatedCPU": allocated_cpu_single}
    config.items_list.append(item)

    # 返回分配成功结果
    return (f"OP --> {user} request for {request_cpu} CPU, CPU allocated: {allocated_cpu_single}, Overbooking: {config.overbooking}\n", False)


#  release operation
def process_release(user, release_cpu):
    item = check_user_and_cpu(config.items_list, user, release_cpu)

    # 判断该用户是否符合release条件
    if not item:
        return (f"ERR --> Fail TO RELEASE: {user} haven't requested for CPU successfully OR the number is not equal\n", True)

    else:

        # 在list中获取实际的cpu数量(overbooking = true)
        if item["realCPU"] != item["allocatedCPU"]:
            release_cpu *= config.fraction_value
            if config.allocated_cpu - release_cpu <= config.low_usage_rate:
                config.overbooking = False

        # overbooking = false
        # release_cpu = release_cpu

        # 进行release 操作
        # 修改 remaincpu value
        config.remaining_cpu += release_cpu
        config.allocated_cpu -= release_cpu

        # 将这组数据从list中移除
        config.items_list.remove(item)

        # 返回release 成功结果
        return (f"OP --> {user} released CPU: {release_cpu}\n", False)
