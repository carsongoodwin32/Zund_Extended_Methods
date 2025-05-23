Simple Demo:

This demo aims to represent one of the most simple use cases of Zund Extended Methods.
We have 2 .zcc files that have different materials defined and will be treated differently.

Files in Demo_ZCC_Files:
FELT.zcc has Material "FELT PANEL" defined
GENERIC.zcc has Material "Generic Material" defined

Take a look at settings.cfg and you'll see a definition for 
[FELT PANEL] , but not Generic Material.

You'll also see a definition for [COMMON] (of which both "FELT PANEL" and "Generic Material" will run with)
and one for [DEFAULT] (of which only "Generic Material" will run with, due to not having a specific definition)

Files in Extended_Methods:
default.xml will be used for the [DEFAULT] case
common.xml will be used for the [COMMON] case
felt.xml will be used for the [FELT] case

If you look inside these files, you'll see each one has a unique Method to add to the files it runs on.

Go ahead and run the demo, you'll see that the files stay mostly the same, 
but with the methods from the .xml files appended to the bottom.

This is useful if you want to define more methods than Zund Cut Center allows you to save by default.