from math import ceil
from app.minimum_gas.data_structures import StopPair

valid_stops = [stop for stop in range(0, 60, 3)]
#print(valid_stops)

def find_first_stop(depth=45):
    half = depth / 2
    stop_index = int(half // 3) + 1
    #print(stop_index)
    return stop_index*3, stop_index

def min_gas_plan(start_depth, target_depth, solve_time):
    target_index = target_depth / 3
    first_stop, first_index = find_first_stop(start_depth)
    if (start_depth - first_stop)%9 == 0:
        travel_time = (start_depth - first_stop)//9
    else:
        travel_time = (start_depth - first_stop)//9 + 1
    plan = [StopPair(start_depth, solve_time), 
            StopPair(first_stop, travel_time + solve_time)]
    if first_stop > target_depth:
        current_index = first_index
        while (current_index > target_index):
            next_index = current_index - 1
            current_index = next_index
            next_stop = valid_stops[next_index]           
            previous_rt = plan[-1].get_time()
            plan.append(StopPair(next_stop, previous_rt + 1))
    plan.append(StopPair(plan[-1].get_depth(), plan[-1].get_time()+1)) #add 1 ' to gas switch depth for gas switch duration
    #print(plan)
    return plan


def min_gas_litres(plan):
    avg_depth = ((plan[0].get_depth() - plan[-1].get_depth()) / 2) + plan[-1].get_depth()
    avg_ata = (avg_depth + 10)*0.1
    litres = plan[-1].get_time() * 60 * avg_ata
    return int(litres)

def min_gas_bar(litres, tank_vol):
    bar = litres / tank_vol
    return int((ceil(bar*0.1)/0.1)) #rounding to tens place ex. 73.xxx bar -> 80 bar
'''
p = min_gas_plan(45, 21, 1)
print(p)
l = min_gas_litres(p)
print(l)
b = min_gas_bar(1290, 24)
print(b)
'''