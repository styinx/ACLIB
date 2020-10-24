## Widget classes

### ACWidget

| Attribute | Description | 
| :--- | :--- | 
| ```python background: bool = False``` | Defines whether the background of the widget is drawn. |
| ```python background_color: Color = Color(0.0, 0.0, 0.0, 0.0)``` | Holds the background color. If the alpha value is > 0 `background` is set to True otherwise to False. |
| ```python background_texture: str = ''``` | Holds the path to a texture that is drawn in the background. If the texture is not empty `background` is set to True otherwise to False. |
| ```python border: bool = False``` | Defines whether the border of the widget is drawn. |
| ```python border_color: Color = Color(0.0, 0.0, 0.0, 0.0)``` | Holds the border color. If the alpha value is > 0 `border` is set to True otherwise to False. |
| ```python child: ACWidget = None``` | Holds the child widget. |
| ```python id: int = -1``` | Holds the id of the widget. | 
| ```python position: Point = Point(0, 0)``` | Holds the position of the widget. |
| ```python size: Size = Size(0, 0)``` | Holds the size of the widget. | 
| ```python visible: bool = True``` | Defines whether the widget is visible. |
| | |
| **Private Function** | **Description** |
| ```python _on_id()``` | |
| ```python _on_parent_changed()``` | |
| ```python _on_position_changed()``` | |
| ```python _on_size_changed()``` | |
| ```python _on_visibility_changed()``` | |
| ```python _event_changed(event: str, widget: ACWidget)``` | **Static** function that will return a unique function that will fire the event when it is called from the widget. |
| **Public Function** | **Description** |
| | |
