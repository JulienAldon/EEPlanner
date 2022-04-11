# EpitechEventPlanner
Event planner for epitech intranet

## Support
### Current activity `W-ADM-007/LYN-0-1/acti-505014`
### Current promotions 
- wac1
- wac2
- msc1 (intra msc4)
- msc2 (intra msc5)
- premsc (intra msc3)

## Content
- Command Line Interface ([__main__.py](./src/__main__.py))
- GUI interface using pyGTK ([interface.py](./src/interface.py))
- Documentation [Reference](https://julienaldon.github.io/EpitechEventPlanner/index.html#document-modules)
- Tests ([tests.py](./src/tests.py))

### CLI 
A Command Line Interface allow the user to quickly add events to an activity
See section usage for more info.
```sh
pipenv run python src
```

### GUI Interface 
The application comes with an interface made with pyGTK
```sh
pipenv run python interface.py
```

#### Build Interface
The application can be built by using the following command
```sh
pipenv run python setup.py
```

#### Tests
The application have some basic unit tests using python unittest
```sh
pipenv run python tests.py
```

# Install dependency
For maintainability reason the project comes with a `pipenv` file describing all the dependency and their version
```sh
pipenv install
```

# CLI exemple usage
```sh
pipenv run pyton . --promotion wac1 "2022-01-17" "2022-01-18"
```

```sh
Usage: 
create_sign_sessions.py [-h] --promotion promotion [--events [events ...]] [dates in %Y-%m-%d ...]

Select promotions and dates or events

Positional arguments:
  dates in %Y-%m-%d

Optional arguments:
  -h, --help            show this help message and exit
  --promotion promotion, -p promotion
  --events [events ...]
```

The script must be executed with dates first (to create the events)
The created events must be printed on the standard output.
You can use this list to add some more promotions to the given events with `--events` flag.
