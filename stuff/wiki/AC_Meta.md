## ACMeta

The `ac_meta.py` modules extends the ACData by more properties that are not available through the shared memory.
Most of the information is computed during runtime. Since not all cars have the same properties, some of the functions
may not return useful data.
 
### Car

| Property | Description |
| :--- | :--- |
| badge |  |
| brand |  |
| class_name |  |
| name |  |
| rpm_min |  |
| rpm_max |  |
| rpm_damage |  |
| type |  |


### Driver

| Property | Description |
| :--- | :--- |
|  |  |


### Environment

| Property | Description |
| :--- | :--- |
| track_length |  |


### Session

| Property | Description |
| :--- | :--- |
|  |  |


### Timing

| Property | Description |
| :--- | :--- |
|  |  |


### Tyres

| Property | Description |
| :--- | :--- |
| ideal_pressure | A function that requires the name of the compound as string and a boolean that indicates if the front or rear pressure is demanded. |
| ideal_temperature | A function that requires the name of the compound as string and a boolean that indicates if the front or rear temperature is demanded. |
| ideal_brake_temperature | A function that requires a boolean that indicates if the front or rear brake temperature is demanded. |
