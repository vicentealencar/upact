def is_day_in_recurrence(recurrence_string, day):
    recurrence = rrule.rrulestr(RecurringEvent().parse(recurrence_string))
    return (recurrence[0].date() - day.date()).days == 0

def is_time_in_interval(begin_str, end_str, time):
    begin_time = parse(begin_str).time()
    end_time = parse(end_str).time()

    return begin_time <= time and time < end_time

