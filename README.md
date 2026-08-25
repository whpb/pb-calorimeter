# PB Heat Measurement
Written by WB, 25/08/2026.
## Summary
A tool to enable indirect calorimetric measurements on the Polar Bear. 

## Usage
### Running a cycle
Make sure to run the polling script before beginning. To run the program, double click *Run Valve Tests.bat*.

To execute a function, change User Value 1 on the nanodac to the corresponding number. The polling function is latched, so the function will run only once then wait until the value is reset to 0.

Available functions:
| Number | Function                 |
| ---    | ---                      |
| 1      | Calorimetric measurement |

#### Calorimetric measurement

The calorimetric measurement function comprises three steps:

1. Start: take baseline work reading, initiate loop
2. Loop: calculate instantaneous work and rolling energy total based on heater utilisation and plate temperature; these equations reference the data in pb_cooling_capacity.csv
3. End: close results file and produce report detailing work curve (relative to baseline) and total energy added or removed

This function applies the principle of conservation of energy to estimate the energy change caused by a source or sink placed on the plate.

Before starting, the Polar Bear is instructed to hold a control temperature. This provides a stable baseline from which deviations can be measured.

The function is started, and begins performing the following calculation every time step:

    Q_relative = Q_abs - Q_baseline

Where Q_abs is interpolated from the Polar Bear's characteristic cooling power-temperature curve, and Q_baseline is the initial value of Q_abs. All Q values are measured in Watts.

The rolling total energy is also calculated:

    E_t = E_t-1 + Q_relative * t_step

Where E_t-1 is the total energy as calculated in the previous time step, and t_step is the size of the time step in seconds.

TODO: FINISH WRITING THIS!!

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
        └── programmer
             └── "UserInput":   ["controller name", "modbus address"]

*Note that "etc..." indicates an arbitrary number of entries. Ensure "controller name" fields match the controller name exactly.*

#### File handling
By default, files are saved in the format `Documents/PBCal/YYYY-MM-DDThh-mm-ss.csv` (based loosely on ISO 8601).

The available settings are listed below.

| Setting | Code | Notes |
| ---     | ---  | ---   |
| Save file location | `{"SavePath": "C:\path\to\folder\"}` | Paste file path from Windows console to avoid formatting errors |
| Save file name convention | `{"FileName": "results"}` | A date or time value can be specified according to [strftime rules](https://docs.python.org/3/library/datetime.html#format-codes); if a plaintext filename is used, files will be named sequentially rather than timestamped (i.e. NewFile 1, NewFile 2, etc.)
