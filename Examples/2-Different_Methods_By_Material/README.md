Different Methods:

This demo aims to represent a slightly more advanced use case of Zund Extended Methods.
We now have 3 .zcc files that have different materials defined and will be treated differently.

Files in Demo_ZCC_Files:
1inchFELT.zcc has Material '1" FELT PANEL' defined
2inchFELT.zcc has Material '2" FELT PANEL' defined
GENERIC.zcc has Material "Generic Material" defined

Take a look at settings.cfg and you'll see a definition for 
[1" FELT PANEL] , and [2" FELT PANEL] , but not Generic Material.

You'll also see a definition for [COMMON] (of which '1" FELT PANEL' '2" FELT PANEL' and "Generic Material" will run
with)
and one for [DEFAULT] (of which only "Generic Material" will run with, due to not having a specific definition)

Files in Extended_Methods:
default.xml will be used for the [DEFAULT] case
common.xml will be used for the [COMMON] case
1inchfelt.xml will be used for the [1" FELT PANEL] case
2inchfelt.xml will be used for the [2" FELT PANEL] case

If you look inside these files, you'll see each one has a unique Method to add to the files it runs on.

Go ahead and run the demo, you'll see that the files stay mostly the same, 
but with the methods from the .xml files appended to the bottom.

This is useful if you want to define more methods than Zund Cut Center allows you to save by default,
and also have more than one material you'd like to do that for. These extra materials are not constrained
by what you've defined as extra for any other material. Whatever you define in the .xml for the case that
runs on that material gets inserted into that file.