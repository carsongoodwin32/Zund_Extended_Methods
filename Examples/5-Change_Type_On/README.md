Change Type on:

This demo aims to represent an advanced use of Zund Extended Methods, in a simple controlled environment.
We have only 1 .zcc file in this case.

Files in Demo_ZCC_Files:
GENERIC.zcc has Material "Generic Material" defined

Take a look at settings.cfg and you'll see a definition for [DEFAULT] only
Take note of the fact that [DEFAULT] has no material file defined, only change_type_on is defined.
change_type_on contains one thing: "{none}"
Any Outlines under the Geometry tag in GENERIC.zcc containing a Method with type equal to "{none}" will be changed.

Go ahead and run the demo, you'll see that GENERIC.zcc has no more {none} types in its Geometry methods.
They've been replaced with the most likely pick from the method file, based on the Geometry methods "Name" field.

For example:

This Outline in the Geometry Tag:
```<Outline GroupId="2">
    <MoveTo X="10.000000" Y="1465.500000"/>
    <ArcTo Y2="1465.500000" X1="458.500000" Y1="1914.000000" X2="907.000000"/>
    <ArcTo Y2="1465.500000" X1="458.500000" Y1="1017.000000" X2="10.000000"/>
    <Method Type="{none}" Name="PERIMETER"/>
</Outline>```

Could map to this contained in a materials .xml file:
```<Method Type="Thru-cut" Color="ff0000" CustomOrdered="true" AllowReverseDirection="false" Name="PERIMITER">
</Method>```

To become:
```<Outline GroupId="2">
    <MoveTo X="10.000000" Y="1465.500000"/>
    <ArcTo Y2="1465.500000" X1="458.500000" Y1="1914.000000" X2="907.000000"/>
    <ArcTo Y2="1465.500000" X1="458.500000" Y1="1017.000000" X2="10.000000"/>
    <Method Type="Thru-cut" Name="PERIMETER"/>
</Outline>```

It matches based off the .zccs Outlines Method Name field to the .xmls Methods name field

This is useful if you have other software outputting .zcc files that cannot/will not sync with the types already 
inside your Zund Cut Center, or you're using more methods (or variations of methods) than can be saved inside of
Zund Cut Center.