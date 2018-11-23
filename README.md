# ACLIB

_Assetto Corsa App Library_

## Features

- Assetto Corsa GUI
- Extensible Widget Collection
- ~~Overhead detection~~
- ~~SQLite3 Database Connection~~
- GUI Events / ACLIB Events
- Realtime App Configuration 

## Install

- **1**
  - Either: Download the repository
  - Or: ```git clone https://github.com/styinx/ACLIB```

- **optional**
  - remove the folder /images and README.md

- **2**
  - extract the folders /apps and /contents into the location where you have Assetto Corsa installed (usually ```C:\Program Files (x86)\Steam\steamapps\common\assettocorsa```)

- **3**
  - run Assetto Corsa
  - enable ACLIB in the settings


## Features in Detail

**Assetto Corsa GUI**:

- Composite Model wrapped around AC GUI elements
- Layout Elements (grid, box, ...)

---

**Widget Collection**:

- GUI Widgets (progress bar, ...)
- Car Widgets (tyres, shift indicators, fuel, ...)

---

**~~Overhead Detection~~**:

- ~~Based on the systems performance the apps used with ACLIB can suspend/resume expensive calculations.~~
---

**~~SQLite3 Database~~**:

- ~~useful to store cross sessions or other more complex data~~

---

**GUI Events / ACLIB Events**:

- Ingame events can trigger custom functions
- Examples: Position change, Lap change, ...

---

**Realtime App Configuration**:

- apps can be styled with configuration
- changes are applied in real time without reloading
- enables app customization without altering code

---

### Issues

## Apps with ACLIB