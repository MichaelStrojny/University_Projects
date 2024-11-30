def initialize():
    global health_points, run_time, interest, hedons, current_time, last_exercise, star_activity, star_awarded_time1, star_awarded_time2, star_awarded_time3

    health_points = 0
    hedons = 0
    current_time = 120   # initialized to value > 120 so that (current_time - last_exercise < 120) is True when last_exercise = 0
    last_exercise = 0
    run_time = 0
    star_activity = ''
    star_awarded_time1 = 0    # time when most recent star was awarded.
    star_awarded_time2 = 0
    star_awarded_time3 = 0    # times when 3rd most recent star was awarded
    interest = True    # false when the user gains 3+ stars in under 2 hours. When false, can't be changed back to true, and stars become useless for entire simulation

def get_cur_hedons():
    return hedons

def get_cur_health():
    return health_points

def offer_star(activity):
    global star_activity, star_awarded_time3, star_awarded_time2, star_awarded_time1, current_time, interest

    if activity.lower() == "resting":
      return None   #cant give stars for resting

    star_activity = activity.lower()
    star_awarded_time3 = star_awarded_time2     # update times that 1st 2nd and 3rd most recent stars were awarded
    star_awarded_time2 = star_awarded_time1
    star_awarded_time1 = current_time

    if interest and star_awarded_time3 != 0:     # ensures that 3 stars have been given before letting code modify interest variable
        interest = (star_awarded_time1 - star_awarded_time3) > 120    #  if statement makes it so once interest = False, it cant be modified (stays false)

def star_can_be_taken(activity):
    if star_activity == activity and star_awarded_time1 == current_time and interest:
        return True
    return False

def tired():
    return current_time - last_exercise < 120      # returning a condition like (current_time - last_exercise < 120) returns True if da condition is true

def most_fun_activity_minute():
    if star_can_be_taken(star_activity):
        return star_activity
    if tired():
        return 'resting'
    return 'running'      # or textbook too since both give 1 pt

def perform_activity(activity, minutes):
    global star_activity, hedons, health_points, last_exercise, current_time, run_time

    activity = activity.lower()     # ignore .lower() .... just makes program more user friendly

    if star_can_be_taken(activity):
        if minutes < 10:
            hedons += 3*minutes
        else:
            hedons += 30     # 3*10

    if activity == 'running':

        if minutes <= 160 and minutes <= (180 - run_time):
            health_points += 3*(minutes)
        elif run_time <= 180:
            health_points += 3*(180-run_time) + (minutes-180+run_time)
        else:
            health_points += minutes

        if not tired():
            if minutes < 10:
                hedons += 2*minutes
            else:
                hedons += 20 - 2*(minutes-10)    # if minutes > 10, then that means in first 10 minutes , 10*2 hedons given , and for left over minutes after 10, 2 hedons taken away per minute
        else:
            hedons -= 2*minutes

    elif activity == 'textbooks':

        health_points += 2*minutes

        if not tired():
            if minutes < 20:
                hedons += minutes
            else:
                hedons += 60 - 2*minutes
        else:
            hedons -= 2*minutes

    #resting is useless so it does not have a loop. if you rest, current time simply increases by minutes

    current_time += minutes

    if activity == 'running' or activity == 'textbooks':
        last_exercise = current_time
    if activity == 'running':
       run_time += minutes
    if activity != 'running':
       run_time = 0    #sets the "culumative time user spent running without break" to 0

if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)
    print(get_cur_health())            # 90 = 30 * 3
    print(most_fun_activity_minute())  #resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute())  # running
    perform_activity("textbooks", 30)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 170)
    print(get_cur_health())
    print(get_cur_hedons())