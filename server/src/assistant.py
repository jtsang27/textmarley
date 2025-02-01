import time
from datetime import datetime

time_str1 = "10:00 AM"
time_str2 = "12:00 PM"

dt1 = datetime.strptime(time_str1, "%I:%M %p")
dt2 = datetime.strptime(time_str2, "%I:%M %p")

print(dt1)
print(dt2)

print("17:32" == time.strftime("%H:%M"))

