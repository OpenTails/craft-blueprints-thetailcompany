# Craft Blueprints for Crumpet

This repository contains the recipes for building Crumpet-android (primarily
for Android, but also for any other of the potential targets you might want to
build it for or on).

To set up Craft, follow the instructions found in the documentation here:
https://community.kde.org/Craft/Android

You will likely want to set up more than one Craft persistent paths, one for
each of the architectures you want to build Crumpet for (so for example arm32
and arm64).

To actually build it, first follow the instructions above to bootstrap a craft
capable build docker on your local system, and then add this repository to
Craft by running:

```
craft --add-blueprint-repository https://github.com/OpenTails/craft-blueprints-thetailcompany.git\|\|main
```

Then you can use the craft command line interface to perform the actual
building and packaging steps.

```
craft crumpet
craft --package crumpet
```
