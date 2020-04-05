valid_stops = [stop for stop in range(0, 60, 3)]
#print(valid_stops)

def find_first_stop(depth=43):
    half = depth / 2
    stop_index = int(half // 3) + 1
    #print(stop_index)
    return stop_index*3, stop_index

def min_gas_plan(start_depth, target_depth, solve_time):
    target_index = target_depth / 3
    first_stop, first_index = find_first_stop(start_depth)
    #plan = [[start_depth, 1],
    #        [first_stop, 1],
    #]
    plan = [[start_depth, solve_time], 
            [first_stop, ((start_depth - first_stop ) // 9) + solve_time + 1]]
    if first_stop > target_depth:
        current_index = first_index
        while (current_index > target_index):
            next_index = current_index - 1
            current_index = next_index
            next_stop = valid_stops[next_index]           
            previous_rt = plan[-1][1]
            plan.append([next_stop, previous_rt + 1])
    plan.append([plan[-1][0], plan[-1][1]+1]) #add 1 ' to gas switch depth for gas switch duration
    print(plan)
    return plan




#find_first_stop()

min_gas_plan(45, 21, 1)
