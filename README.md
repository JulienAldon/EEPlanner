# EEPlanner
Event planner for epitech intranet.
The purpose of this tool is to create repeating events under a given activity.

![How does it look ?](assets/img.png "Example")

## Install (globaly)
You must have pipenv installed before executing the makefile
```
make install
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