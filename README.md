# python-komoot-gpx-creator

## Getting started

1. Create your env file, by renaming ``.env.example`` to e.g. ``.env`` and fill in the variables.
2. load the env file into your environment, by executing
```
source .env
```
3. Specify the output folder in ``src/config.py`` by defining the variable ``output_folder``
4. Add gps-coordinates, that shall not be in any trip    
5. Run the application by executing
```
python src/main.py
```