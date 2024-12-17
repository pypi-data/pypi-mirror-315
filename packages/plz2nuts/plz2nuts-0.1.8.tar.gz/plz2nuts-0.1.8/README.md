# Plz-To-NUTS
This is a tool to convert a German Postleitzahl (zip code) to the coresponding NUTS IDs.
It takes 1-5 digits of the zip code as an input.

## Installation
To install the tool, use the following command:
```
pip install plz2nuts
```

## Usage
To use the tool, follow these steps:
1. **Command Line Interface (CLI):** You can use the tool from the command line by running:
   ```sh
   plz2nuts --help
   ```
   This will display the available options and how to use them.

2. **Basic Usage:** To convert a Postleitzahl to a NUTS ID, use:
   ```sh
   plz2nuts <postleitzahl>
   ```
   Replace `<postleitzahl>` with the actual Postleitzahl you want to convert.

3. **Import in Python:** You can also import the tool in your Python code to get a NUTS ID for a plz:
   ```python
   from plz_to_nuts import convert_plz_to_nuts
   convert_plz_to_nuts('10')
   ```


## License
This project is licensed under the AGPL-3.0-or-later license. See LICENSES/AGPL-3.0-or-later.txt for details.
