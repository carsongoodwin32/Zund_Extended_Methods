# Zund_Extended_Methods

A Python application to take in .zcc files and apply a standard list of extended methods (even bypassing the limits of ZCC and friends)

This also stands as a reference for how I would build a professional, self-contained, production ready, maintainable Python application.

## Description

Zund Cut Center only allows you to have 3 different variations of methods mapped for any one material. This program allows you to go much further beyond that, allowing you to set as many kinds of methods (kinds of cuts, variations of settings of cuts, etc) that will be mapped without any intervention from the person doing the cutting.

This program was developed for SABIN and released freely to those who will benefit from it.

## Getting Started

### Dependencies

* Windows 10 version 1809 (includes LTSC 2019) or higher (Untested on lower versions, may work)
* Python 3.9 or higher if using Manual Install (Untested on lower versions, may work)

### Installing

Grab the latest release from the sidebar relating to what you're looking to do

* The ZEM-x.x-Windows-Service.zip is for those looking to deploy onto their Zund Machines with an already tested settings.cfg file
* The source code download is for all others, developing, making changes, testing, etc.

### Using ZEM-x.x-Windows-Service

* Under construction

### Running, Developing, or Testing ZEM from Source

In an effort to keep this program as accessible as possible, there are two methods of installation.

#### Automatic installation (Does not require Python to be preinstalled, or any Python knowledge)

This method will download a Python 3.9 installation, set up a virtual environment, and activate it for you.

1. Double click the Automated_install.bat file (You may need to right click and Run as Admin if things fail).

2. If Windows Defender Smart Screen pops up, click "More Info" and "Run anyway".

3. If you get a Security Warning, type "R" and then Enter.

4. Wait for installation to complete.

5. When installation completes you should be inside of your virtual environment.

6. You can now type the command 'python ZEM.py' (without the quotes) and press enter to run ZEM with your settings.cfg that sits next to it in the folder structure, or type 'execute_demo.bat' to run any of the examples.

7. If you quit, you can rerun Automated_install.bat to get back into your virtual environment.

#### Manual Installation 

```
there will be code here
```

### Packaging a custom Windows-Service version

* Under construction
```
there might be code here?
```

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the 0BSD License - see the LICENSE.md file for details
