## Style Customization

It is now possible to change the appearance of an app by changing the contents of an `.ini` file.
If you only want to change the style of elements inside a specific app or to a specific class create a `.ini` file in the style directory of ACLIB.

Here is an example how the file names and structure should look like:
```
C:/Users/<your_name>/Documents/Assetto Corsa/ACLIB/
|- config/
|- metadata/
|- style/
  |- <your_app>.ini
  |- <your_widget_class>.ini
  |- ACLIB_Comparator.ini            <- This is only applied to elements in ACLIB_Comparator
  |- ACLIB_Time.ini                  <- This is only applied to elements in ACLIB_Time
  |- ACLabel.ini                     <- This is applied to ALL objects of type ACLabel
```

Example configuration for ACLIB_Comparator in the file `ACLIB_Comparator.ini`:
```ini
[CR_Header]
background_color = ui.color.RED ; Header Background Color ;

[CR_Icon]
background_color = ui.color.LIGHTGRAY ; Icon Background Color (Button without text) ;

[CR_Button]
background_color = ui.color.LIGHTGRAY ; Button Background Color (Button with text) ;

[CR_Name]
background_color = ui.color.Color(0.0, 0.0, 0.0, 1.0) ; Label Background Color ;
```

Note that the config file is type aware and will automatically import the module name.
The objects `RED`, `BLACK`, ... as well as the class `Color` are defined in the file `ui/color.py`.
You can use any class in the config file as long as you use the correct module path starting from the base module `source`.
Sections in the config file (`CR_Name`) represent the name of the class.
All objects of class `CR_Name` will have a black background.

Example configuration for ACLabel in the file `ACLabel.ini`:
```ini
[DEFAULT]
border_color = ui.color.RED ; Label Border Color ;
```

If this file does exist in the `style/` directory all objects of `ACLabel` will have a red border.