import psutil
import winsound
from time import sleep
import os
import win32api
from datetime import datetime

clear = lambda: os.system('cls')

def seconds_to_hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

def datetime_formatted(dt):
  return dt.strftime('%H:%M:%S %d/%m/%Y')
#  return dt.strftime('%d/%m/%Y, %H:%M:%S')

PERCENTAGE_THRESHOLD = 20
SECONDS_BETWEEN_CHECKS = 8

DIALOG_TITLE = "LOW BATTERY!"

if __name__ == '__main__':
  while True:
    battery  = psutil.sensors_battery()
    percent  = battery.percent
    secs_left = battery.secsleft
    plugged_in = battery.power_plugged

    messages = [f"Charge = {percent}%", 
                f"Estimated time left = {seconds_to_hours(secs_left)}",
                "Plugged in" if plugged_in else "Not plugged in",
                f"Will alert when battery drops to {PERCENTAGE_THRESHOLD}%"
               ]

    clear()
    for message in messages:
      print(message)
    print(f"Last update: {datetime_formatted(datetime.now())}")

    if (percent < PERCENTAGE_THRESHOLD) and not plugged_in:
      winsound.PlaySound('./sfx/alert.wav', winsound.SND_FILENAME)
      dialog_message = "\n".join(messages)
      win32api.MessageBox(0, dialog_message, DIALOG_TITLE, 0x00001000)
    
    sleep(SECONDS_BETWEEN_CHECKS)