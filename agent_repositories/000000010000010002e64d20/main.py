import os
result = "main result"
of.open_dataset()
log_message("message from print_globals", "info")
pause(4)
print("ONE TIME IN " + str(os.getpid()))