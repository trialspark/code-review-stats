def days_until_next_business_day(day: int) -> int:
  # If Mon/Tue/Wed/Thur, next day is tomorrow
  if day in list(range(0,4)):
    return 1

  # otherwise, return days until Monday
  return 7 - day

def startofday(arrow_date):
  return arrow_date.replace(hour=10, minute=0, second=0)

def midday(arrow_date):
  return arrow_date.replace(hour=14, minute=0, second=0)

def endofday(arrow_date):
  return arrow_date.replace(hour=18, minute=0, second=0)

def get_due_time(request_time):
  if request_time < midday(request_time):
    return endofday(request_time)

  next_business_day = request_time.shift(
    days=+days_until_next_business_day(request_time.weekday()),
  )
  return midday(next_business_day)