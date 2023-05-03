# EEPlanner
Event planner for epitech intranet.
The purpose of this tool is to create repeating events under a given activity.

![How does it look ?](assets/img.png "Example")

## Install 
### Debian
A complete debian build system is available in the repository.

You can get the .deb packages in releases section

```
sudo dpkg -i eeplanner_<version>_amd64.deb
```

### Archlinux
A PKGBUILD file is available in the repository, you can build it.

```
makepkg -si
sudo pacman -U <package_created>.pkg.tar.zst
```

### (globaly using pip)
You must have pipenv installed before executing the makefile
```
sudo make install
```

Running without sudo will not install correctly

## Uninstall
```
sudo make uninstall
```

## Install (for dev)
```
pipenv install
pipenv run python eeplanner
```

# Functionnalities
With this program you can :

- Planify recurent sessions inside an activity
    - Customize activity.
    - Customize hours.
    - Customize day.
- Register students to all planified sessions.
- Register students to specific sessions (under the `Sessions` panel) sessions previously planified.

> Due to technical restrictions you have to planify sessions before registering students however you can use the `Sessions` panel to register students to already planified sessions.