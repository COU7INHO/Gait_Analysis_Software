travel_distance = int(input("How long is your commute?\n>> "))

avg_speed = int(input("What will be the average speed?\n>> "))

travel_time = travel_distance / avg_speed

print(round(travel_time * 60, 1))
