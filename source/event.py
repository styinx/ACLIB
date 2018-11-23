class GUI_EVENT:
    ON_POSITION_CHANGED = 0
    ON_SIZE_CHANGED = 1
    ON_CHILD_CHANGED = 2
    ON_PARENT_CHANGED = 3
    ON_VISIBILITY_CHANGED = 4
    ON_CLICK = 5
    ON_TEXT_CHANGED = 6
    ON_CONFIG_CHANGED = 7


class LIB_EVENT:
    ON_LAP_CHANGED = 0
    ON_SECTOR_CHANGED = 1
    ON_MINISECTOR_CHANGED = 2
    ON_KM_CHANGED = 3
    ON_POSITION_CHANGED = 4
    ON_POSITION_GAINED = 5
    ON_POSITION_LOST = 6
    ON_FLAG_CHANGED = 7
    ON_PIT_ENTERED = 8
    ON_PIT_LEFT = 9


# class EventDispatcher:
#     events = {}
#
#     def addEvent(self, name, event):
#         EventDispatcher.events[name] = event
#
#     def dispatchEvent(self, name):
#         EventDispatcher.events[name]()
