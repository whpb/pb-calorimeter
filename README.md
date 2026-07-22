# Valve Tests 2
Written by WB, 22/07/2026.
## Summary
This repository is intended to replace the various scripts written by HL for the 7.9mm valve test rig. It comprises a polling script, which listens for user inputs via the nanodac, and a number of functions for automating the test procedure.

## Usage
### Testing valves
Make sure to run the polling script before beginning a test. 

To execute a function, change User Value 1 on the nanodac to the corresponding number. The polling function is latched, so the function will run only once then wait until the value is reset to 0.

Available functions:
| Number | Function                        |
| ---    | ---                             |
| 1      | Test & record cracking pressure |

### Settings
To change the program settings, open the file `settings.json` in a text editor.

#### Controller & MODBUS addresses
Hardware addresses are stored in the following structure:

    addresses
    ├── controllers
    │   ├── "name A": "xxx.xxx.xxx.xxx:xxxxx"
    │   ├── "name B": "xxx.xxx.xxx.xxx:xxxxx"
    │   └── etc...
    └── modbus
        ├── programmer
        │   ├── "UserInput":   ["controller name", "modbus address"]
        │   ├── "TempSensor":  ["controller name", "modbus address"]
        │   └── "RampControl": ["controller name", "modbus address"]
        └── pressure
            ├── "ColNameA": ["controller name", "modbus address"]
            ├── "ColNameB": ["controller name", "modbus address"]
            └── etc...

*Note that "etc..." indicates an arbitrary number of entries. Ensure "controller name" fields match the controller name exactly.*

#### File handling
By default, files are saved in the format `Documents/ValveTests2/YYYY-MM-DDThh-mm-ss.csv` (based roughly on ISO 8601).

The available settings are listed below.

| Setting | Code | Notes |
| ---     | ---  | ---   |
| Save file location | `{"SavePath": "C:\path\to\folder\"}` | Paste file path from Windows console to avoid formatting errors |
| Save file name convention | `{"FileName": "results"}` | A date or time value can be specified according to [strftime rules](https://docs.python.org/3/library/datetime.html#format-codes); if a plaintext filename is used, files will be named sequentially rather than timestamped (i.e. NewFile 1, NewFile 2, etc.)
