import datetime
day  = datetime.date.today().isoformat()
formate_date = day.split('-')
day = datetime.date(int(formate_date[0]),int(formate_date[1]),int(formate_date[2])).weekday()
print(day)