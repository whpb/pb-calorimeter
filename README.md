# PB Heat Measurement
Written by WB, 25/08/2026.
## Summary
A tool to enable indirect calorimetric measurements on the Polar Bear. 

## Usage
### Starting the program
Make sure to run the polling script before beginning. To start, double click *App.bat*.

This opens a menu with the following options:

| Option          | Use it when                                                                                                                                             |
| ---             | ---                                                                                                                                                     |
| Testing mode    | The rig is to run unattended. Waits for User Value 1 and records each run to its own results file. No report is produced; re-analyse the file afterwards. |
| Force run       | You are at the machine. Recording starts straight away and stops when you press *Stop and analyse*, which then asks you to select the zones and produces a report. |
| Re-analyse data | You want a report from a results file you already have, or want to re-cut the zones on one.                                                              |
| Quit            | Close the program.                                                                                                                                       |

While a run or a re-analysis is in progress, the screen shows its output as it happens. *Back to menu* ends it; anything already recorded is kept. Only one option can run at a time.

When a report is produced, a panel appears with links to each of the files it generated.

*Run.bat* and *Reanalyse.bat* start testing mode and re-analysis directly, without the menu.

### Running a cycle
With testing mode active, change User Value 1 on the nanodac to the corresponding number. The polling function is latched, so the function will run only once then wait until the value is reset to 0.

Available functions:
| Number | Function                 |
| ---    | ---                      |
| 1      | Calorimetric measurement |
| 2      | Stop the program         |

Recording continues for as long as User Value 1 is held at 1, and ends when it changes. Set it back to 1 to record another run; each run is written to its own file.

Force run does not use User Value 1 at all. It never writes to the controller.

#### Calorimetric measurement

This software applies the principle of conservation of energy to estimate the energy change caused by a source or sink placed on the plate.

Before starting, the Polar Bear is instructed to hold a control temperature. This provides a stable baseline from which deviations can be measured. Choose a control temperature above about -29 C; below this the cooling curve flattens and a small temperature error costs a large error in power.

The measurement comprises three steps:

1. Start: initiate loop
2. Loop: record plate temp, master temp, and heater utilisation
3. End: close results file. In force run and re-analysis, select the zones and produce a report; in testing mode, stop here.

Every time step, the instantaneous heat flow is calculated and written to a timestamped row in the results file:

    Q_abs = Q_cool - Q_heater

Where Q_cool is interpolated from the Polar Bear's characteristic cooling power-temperature curve at the current plate temperature, and Q_heater is the power the heater is actually using. These equations reference the data in pb_cooling_capacity.csv. All Q values are measured in Watts.

The remaining values cannot be calculated until the baseline is known, so they are worked out after the run:

    Q_relative = Q_abs - Q_baseline
    E_t = E_t-1 + Q_relative * t_step

Where Q_baseline is Q_abs averaged over a zone selected by the user, E_t-1 is the total energy as calculated in the previous time step, and t_step is the measured interval between the two samples in seconds.

##### Selecting the zones

When a force run or a re-analysis finishes, a window opens showing two plots on a shared time axis:

- **Net power (Q_abs)**, on which the **baseline zone** is selected. The plate must be unloaded for the whole of this zone.
- **Master probe temperature**, on which the **experiment zone** is selected. This is the period over which the energy is totalled. If no master probe reading is available, plate temperature is shown instead.

Drag across either plot to set that zone, then close the window to accept. Both zones start with a sensible default, so closing the window without dragging still gives a valid answer.

There is a slow oscillation on the power reading, with a period of roughly 90 to 120 seconds. Cut the baseline zone over a whole number of these cycles, or its average will sit off-centre and every reading will be biased by the same amount. The report gives the standard deviation of the zone so this can be judged, and a warning is printed if the spread looks too wide.

Keep the two zones close together. Baseline subtraction cancels conditions as they were in the baseline zone, so if ambient conditions drift between the two zones the change is wrongly attributed to the source.

##### The report

The report includes:

- Work curve: Q_relative and both temperatures against time, with the selected zones shaded
- Total energy change
- Baseline zone statistics

Total energy is the headline figure. The cooling curve describes the machine at equilibrium, so an instantaneous Q_relative is only meaningful once the plate has settled; the energy total is unaffected because the transient errors largely cancel.

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
             ├── "UserInput":   ["controller name", "modbus address"]
             ├── "PlateTemp":   ["controller name", "modbus address"]
             ├── "HeaterUtil":  ["controller name", "modbus address"]
             └── "MasterTemp":  ["controller name", "modbus address"]

*Note that "etc..." indicates an arbitrary number of entries. Ensure "controller name" fields match the controller name exactly.*

"MasterTemp" is the sample probe. Its address may be set to `null` if no probe is fitted; the column is then left blank and plate temperature is used in its place when selecting the experiment zone.

#### File handling
By default, files are saved in the format `Documents/PBCal/YYYY-MM-DDThh-mm-ss.csv` (based loosely on ISO 8601).

Each run writes its own results file. A report adds files of the same name alongside it: the work curve (`.png`), the report itself (`.pdf`), and the data and template it was built from (`.json` and `.typ`). Re-analysing a file writes a new set named `<original name> reanalysis 1`, leaving the original untouched.

Console output for each session is also saved, under `logs`.

The available settings are listed below.

| Setting | Code | Notes |
| ---     | ---  | ---   |
| Save file location | `{"SavePath": "C:\path\to\folder\"}` | Paste file path from Windows console to avoid formatting errors |
| Save file name convention | `{"FileName": "results"}` | A date or time value can be specified according to [strftime rules](https://docs.python.org/3/library/datetime.html#format-codes); if a plaintext filename is used, files will be named sequentially rather than timestamped (i.e. NewFile 1, NewFile 2, etc.)