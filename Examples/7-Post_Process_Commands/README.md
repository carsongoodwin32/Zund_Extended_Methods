Post Process Commands:

This demo aims to represent an advanced use of Zund Extended Methods, in a simple controlled environment.
We have only 1 .zcc file in this case.

Files in Demo_ZCC_Files:
GENERIC.zcc has Material "Generic Material" defined

Take a look at the Job Name inside of GENERIC.ZCC, You'll see it to be a string of random numbers and letters.

Take a look at settings.cfg and you'll see a definition for [DEFAULT] only
Take note of the fact that [DEFAULT] has no material file defined, only post_process_command is defined.
post_process_command contains one thing: 
"python.exe .\Examples\5-Post_Process_Commands\postprocess_script.py -FILE=%f_p%"

Go ahead and run the demo, you'll see that the Job Name is now "Hello from ZEM!"

This is useful if you want to do some kind of action unsupported inside of Zund Extended Methods, but you
want to leverage the file loading and validation infrastructure of Zund Extended Methods. You can also use
this in conjunction with other options in Zund Extended Methods to create complex workflows per material.

This isn't limited to just loading python scripts, It can run any command that can be run by a PowerShell
command prompt on your computer. Use %f_p% to inject the full path of the files that has been processed 
into the command string.