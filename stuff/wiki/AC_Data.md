## ACData

The `ac_data.py` modules wraps the shared memory into more logical components like car, driver, tyres, ... .
 
### Car

| Property | Description |
| :--- | :--- |
| abs |  |
| class_position | todo |
| damage |  |
| drs |  |
| drs_available |  |
| drs_enabled |  |
| ers_heat_charging |  |
| ers_max_J |  |
| ers_power_count |  |
| ers_power_level |  |
| ers_recovery_level |  |
| fuel |  |
| gear |  |
| has_drs |  |
| has_ers |  |
| has_ideal_line |  |
| has_kers |  |
| has_penalty | todo |
| has_mandatory_pit_stop | todo |
| has_mandatory_pit_stop_done |  |
| is_ers_charging |  |
| is_in_pit |  |
| is_in_pit_line |  |
| is_pit_limiter_on |  |
| is_ai_controlled |  |
| kers_current |  |
| kers_input |  |
| kers_charging |  |
| kers_max_J |  |
| location |  |
| model |  |
| max_fuel |  |
| max_rpm |  |
| position |  |
| rpm |  |
| skin |  |
| speed |  |
| tc |  |
| velocity |  |


### Driver

| Property | Description |
| :--- | :--- |
| firstname |  |
| full_name |  |
| lastname |  |
| name_abbreviation |  |
| nick |  |


### Environment

| Property | Description |
| :--- | :--- |
| air_temperature |  |
| surface_grip |  |
| road_temperature |  |
| track_configuration |  |
| track_name |  |
| track_length |  |
| wind_direction |  |
| wind_speed |  |


### Session

| Property | Description |
| :--- | :--- |
| damage_rate |  |
| flag |  |
| flag_name |  |
| fuel_rate |  |
| has_auto_blip |  |
| has_auto_clutch |  |
| has_reversed_grid |  |
| has_stability_control |  |
| has_tyre_blankets |  |
| is_time_raced |  |
| laps |  |
| name | The name of the session. Can be any of ['Unknown', 'Practice', 'Qualifying', 'Race', 'Hotlap', 'Time Attack', 'Drift', 'Drag'] |
| number_of_drivers |  |
| number_of_sessions |  |
| pit_window_start |  |
| pit_window_end |  |
| session | The id of the session. Can be any of [-1, 0, 1, 2, 3, 4, 5, 6] |
| status |  |
| status_name |  |
| time_left |  |
| tyre_rate |  |


### Timing

| Property | Description |
| :--- | :--- |
| current_lap_time |  |
| current_sector_index |  |
| lap |  |


### Tyres

| Property | Description |
| :--- | :--- |
| angular_speed |  |
| brake_temperature |  |
| camber |  |
| center_temperature |  |
| compound |  |
| compound_name |  |
| compound_symbol |  |
| contact_point |  |
| contact_normal |  |
| contact_heading |  |
| core_temperature |  |
| dirt_level |  |
| inner_temperature |  |
| load |  |
| max_suspension_travel |  |
| outer_temperature |  |
| pressure |  |
| slip |  |
| suspension_travel |  |
| wear |  |
