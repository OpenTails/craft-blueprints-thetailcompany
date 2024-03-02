import info

class subinfo(info.infoclass):
    # This defines the basic information about your software package (both the basic
    # metainformation like human readable names, where the source comes from, and
    # what other blueprints it depends on).
    def setTargets(self):
        # The human-readable name of the main binary
        self.displayName = "Crumpet"
        # A description of the entire package
        self.description = "Control application for The Tail Company's animatronic gear"
        # The project's webpage (if you're unsure for a KDE project, just use this one)
        self.webpage = "https://www.thetailcompany.com/"
        # You can set various targets. By convention, call your primary one "master"
        # and then give the git URL for the project. If you need to specify a branch,
        # you can do so by adding a pipe and the name of the branch (or indeed tag)
        # to the line
        self.svnTargets["master"] = "https://github.com/OpenTails/CRUMPET-Android.git"
        # You can also point at a local clone the repository, if you are doing some test work
        # and building packages regularly.
        # self.svnTargets["master"] = "/mnt/project|kde/qt5.15"
        # You can have multiple targets, each with a unique name.
        # To select a specific commit (or tag) add TWO pipes and the commit hash or tag name
        # to the line
        #self.svnTargets["somecommit"] = "https://invent.kde.org/category/projectname.git||commithash"
        # The default target is what Craft will use to build your package if it is not
        # told anything else (by either the command line, or another blueprint which
        # depends on yours).
        self.defaultTarget = "master"
    def setDependencies( self ):
        # Defines the blueprints this blueprint depends on, and which target (default is what
        # was defined above, and is usually what you would write, except in highly specific
        # cases). These are the directories inside the blueprints directory which contain
        # the blueprint for the thing this blueprint depends on.
        # A buildDependencies entry is something required for actually building the
        # software in this blueprint
        # extra-cmake-modules is needed to pull in a bunch of stuff for building android packages
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/pkg-config"] = "default"
        self.buildDependencies["virtual/base"] = None
        # If there are compiler specific things to consider, either a library you need
        # for a specific compiler and not for others, you can use CraftCore.compiler to
        # make such checks.
        if CraftCore.compiler.isAndroid:
            self.buildDependencies["libs/libintl-lite"] = None # for ki18n
        else:
            self.runtimeDependencies["libs/gettext"] = None # for ki18n
        if CraftCore.compiler.isMinGW:
            self.runtimeDependencies["libs/runtime"] = None #mingw-based builds need this
        self.runtimeDependencies["libs/openssl"] = None
        # a runtimeDependencies entry is something which must also be installed for the
        # software to function (and which will also then be included in any package you
        # build using Craft)
        self.runtimeDependencies["libs/qt6/qtconnectivity"] = "default" # For QtBluetooth
        self.runtimeDependencies["libs/qt6/qtgraphicaleffects"] = "default"
        self.runtimeDependencies["libs/qt6/qtmultimedia"] = "default"
        self.runtimeDependencies["libs/qt6/qtquickcontrols"] = "default" # For the file picker dialog
        self.runtimeDependencies["libs/qt6/qtquickcontrols2"] = "default"
        self.runtimeDependencies["libs/qt6/qtremoteobjects"] = "default"
        self.runtimeDependencies["libs/qt6/qtsensors"] = "default"
        self.runtimeDependencies["libs/qt6/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt6/qttranslations"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None


from Package.CMakePackageBase import * # The package base

class Package(CMakePackageBase):
    # This defines which build system your blueprint should use. In this case, we are
    # using the CMake package base, but there are a lot of options for specific use cases,
    # such as Meson, Perl, QMake, and Binary ones. See 
    # https://invent.kde.org/packaging/craft/-/tree/master/bin/Package
    # for details on which package base options are available. For KDE projects, however
    # you will almost certainly be using CMake, and the others are commonly more useful
    # for when you are creating blueprints for new dependencies.
    def __init__( self ):
        # Always remember to just initialize the package base like so
        CMakePackageBase.__init__( self )
        # If you have tests set up to build by default, for example, you might want to
        # disable those for Craft builds (usually, in KDE, those tests are more useful
        # for the CI system, and less useful for Craft, which is more useful for creating
        # installer packages and the like, not for automated testing purposes). You can
        # do this by setting the following option.
        CMakePackageBase.buildTests = False
        # Build things static - this is basically already done in cmake, but if we don't
        # also set it explicitly here, things we don't want get added to the cmake call
        self.subinfo.options.dynamic.buildStatic = True
        # Make sure we also pull submodules
        self.subinfo.options.fetch.checkoutSubmodules = True
        # Add in a bunch of compiler options we need for this whole thing to build properly
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += " -DANDROID_LINK_EXTRA_LIBRARIES=ON"


    def createPackage(self):
        # Usually you will not need this entry, but in case your main executable is
        # called something else than the blueprint's name, you can set that here.
        # This allows Craft to pass this information to tools which build packages,
        # such as the one which builds appimages, which will then be able to work
        # on the correct executable.
        self.defines["crumpet"] = "digitail"
        # For Windows, similarly to above, if your application is called something
        # other than your blueprint's name, you can explicitly pass in an icon from
        # somewhere on the Craft filesystem. Here we pick out an ico file from inside
        # the 
        #self.defines["icon"] = os.path.join(self.sourceDir(), "digitail.ico")
        # For Windows, you can define a set of shortcuts by setting the shortcuts define with
        # multiple values, such as below:
        self.defines["shortcuts"] = [{"name" : self.subinfo.displayName, "target":"bin/digitail.exe"}]
        # If you have files that get installed automatically, but which you know are
        # in fact not needed for the application to run (this will sometimes be the
        # case for example for building Windows packages, where you don't need some
        # of the things installed by some dependencies), you can list those files
        # in a list in some file, which is a list of regular expressions which will
        # be interpreted on a per-line basis, and any file which is matched by any line
        # will not be included in the package.
        #self.blacklist_file.append(os.path.join(self.packageDir(), "blocklist.txt"))
        # Alternatively, you can add a direct filter on specific files by adding
        # lines like this one (which will cause Craft to not package any executable
        # file that is outside the two directories at the start, and is not named
        # one of the four names in the second paranthesis).
        self.addExecutableFilter(r"(bin|libexec)/(?!(digitail|update-mime-database)).*")

        # You can add packages that should be ignored for packaging purposes. This is
        # in many ways similar to adding a buildDependencies entry, but only ignores
        # this specific package (which can be handy if other things pull in a package
        # that your software doesn't need when publishing).
        self.ignoredPackages.append("dev-utils/sed")

        # In some cases, you need to do things depending on specific conditions,
        # such as building on anything that is not Linus, where you might wish to
        # not ship dbus. You can do this like so:
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        # Finally, just call the packager itself to get the package actually created.
        return super().createPackage()
