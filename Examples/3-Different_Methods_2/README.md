Different Methods 2:

This demo aims to represent a slightly more advanced use case of Zund Extended Methods.
We now have 3 .zcc files that have different materials defined and will be treated differently.

Files in Demo_ZCC_Files:
1inchFELT.zcc has Material '1" FELT PANEL' defined
2inchFELT.zcc has Material '2" FELT PANEL' defined
GENERIC.zcc has Material "Generic Material" defined

Take a look at settings.cfg and you'll see a definition for 
[1" FELT PANEL] , and [2" FELT PANEL] , but not Generic Material.

You'll also see a definition for [UNCOMMON] (of which only '1" FELT PANEL' '2" FELT PANEL' will run
with)
one for [DEFAULT] (of which only "Generic Material" will run with, due to not having a specific definition)

Files in Extended_Methods:
uncommon.xml will be used for the [UNCOMMON] case
1inchfelt.xml will be used for the [1" FELT PANEL] case
2inchfelt.xml will be used for the [2" FELT PANEL] case

If you look inside these files, you'll see each one has a unique Method to add to the files it runs on.

Go ahead and run the demo, you'll see that the files stay mostly the same, 
but with the methods from the .xml files appended to the bottom.

This functionality is useful if you have files that you want to remain completely untouched if they're not recognized.
Using Common in this scenario would have processed and changed GENERIC.zcc. We still get the benefits of being able to
use common code between 1" FELT PANEL and 2" FELT PANEL, but we get to keep that contained to only things that have
material definitions.