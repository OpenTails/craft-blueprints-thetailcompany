# Craft Blueprints for Crumpet

This repository contains the recipes for building Crumpet-android (primarily
for Android, but also for any other of the potential targets you might want to
build it for or on).

To actually build it, first follow the instructions to bootstrap a craft
capable build docker on your local system, and then add this repository to Craft
by running:

```
craft --add-blueprint-repository https://github.com/MasterTailer/craft-blueprints-thetailcompany.git
```

Then you can use the craft command line interface to perform the actual
building and packaging steps.
