Overwrite Methods:

This demo aims to represent an advanced use of Zund Extended Methods, in a simple controlled environment.
We have only 1 .zcc file in this case.

Files in Demo_ZCC_Files:
GENERIC.zcc has Material "Generic Material" defined

Take a look at settings.cfg and you'll see a definition for [DEFAULT] only
Take note of the fact that [DEFAULT] has no material file defined, only delete_layers is defined.
delete_layers contains two things: "#meta-data" and "none". 
Any outlines under the Geometry tag in GENERIC.zcc will be removed from the file.

Go ahead and run the demo, you'll see that GENERIC.zcc is cleaner, without all the metadata inside of it.

This is useful if you have unnecessary data in your files (in this case, unneeded metadata) that you'd like
to clean. This is generally not the only step that is done on files, usually used in conjunction with other
actions, but it's helpful to show all of these actions in isolation so you can understand how they can be
chained to form more complex workflows.