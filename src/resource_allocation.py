import config


# check if user has the permission to release
def check_user_and_cpu(items_list, user, relasenum):
    for item in items_list:
        if item["username"] == user and item["realCPU"] == relasenum:
            return item
    return False


# request operation
def process_request(user, request_cpu):
    config.remaining_cpu
    allocated_cpu_single = request_cpu

    # determine the current mode
    if config.overbooking == True:
        allocated_cpu_single *= config.fraction_value

    # not in overbooking, but after this request maybe enter
    else:
        if config.allocated_cpu + allocated_cpu_single >= config.alarm_rate:
            allocated_cpu_single *= config.fraction_value
            config.overbooking = True

    # whether the reamining CPU is enough
    if config.remaining_cpu < allocated_cpu_single:  # not enough
        return (f"ERR --> OUT OF RESORUCE: {user} request for {request_cpu} CPU, remaing CPU is {config.remaining_cpu}\n", True)

    # start the allocation
    config.remaining_cpu -= allocated_cpu_single
    config.allocated_cpu += allocated_cpu_single

    # record userX's request
    item = {"username": user, "realCPU": request_cpu,
            "allocatedCPU": allocated_cpu_single}
    config.items_list.append(item)

    # return the successful info of this release
    return (f"OP --> {user} request for {request_cpu} CPU, CPU allocated: {allocated_cpu_single}, Overbooking: {config.overbooking}\n", False)


#  release operation
def process_release(user, release_cpu):
    item = check_user_and_cpu(config.items_list, user, release_cpu)

    # check whether the user satisfy the requeiremnet of release
    if not item:
        return (f"ERR --> Fail TO RELEASE: {user} haven't requested for CPU successfully OR the number is not equal\n", True)

    else:

        # get the num of realcpu from list(overbooking = true)
        if item["realCPU"] != item["allocatedCPU"]:
            release_cpu *= config.fraction_value
            if config.allocated_cpu - release_cpu <= config.low_usage_rate:
                config.overbooking = False

        config.remaining_cpu += release_cpu
        config.allocated_cpu -= release_cpu

        config.items_list.remove(item)

        # return result
        return (f"OP --> {user} released CPU: {release_cpu}\n", False)
