import win32api


class KEY:
    LEFT_MOUSE = 0x01
    RIGHT_MOUSE = 0x01
    BACKSPACE = 0x08
    TAB = 0x09
    CLEAR = 0x0C
    ENTER = 0x0D
    SHIFT = 0x10
    CTRL = 0x11
    ALT = 0x12
    PAUSE = 0x13
    CAPS_LOCK = 0x14
    ESC = 0x1B
    SPACEBAR = 0x20
    PAGE_UP = 0x21
    PAGE_DOWN = 0x22
    END = 0x23
    HOME = 0x24
    LEFT_ARROW = 0x25
    UP_ARROW = 0x26
    RIGHT_ARROW = 0x27
    DOWN_ARROW = 0x28
    SELECT = 0x29
    PRINT = 0x2A
    EXECUTE = 0x2B
    PRINT_SCREEN = 0x2C
    INS = 0x2D
    DEL = 0x2E
    HELP = 0x2F
    ZERO = 0x30
    ONE = 0x31
    TWO = 0x32
    THREE = 0x33
    FOUR = 0x34
    FIVE = 0x35
    SIX = 0x36
    SEVEN = 0x37
    EIGHT = 0x38
    NINE = 0x39
    A = 0x41
    B = 0x42
    C = 0x43
    D = 0x44
    E = 0x45
    F = 0x46
    G = 0x47
    H = 0x48
    I = 0x49
    J = 0x4A
    K = 0x4B
    L = 0x4C
    M = 0x4D
    N = 0x4E
    O = 0x4F
    P = 0x50
    Q = 0x51
    R = 0x52
    S = 0x53
    T = 0x54
    U = 0x55
    V = 0x56
    W = 0x57
    X = 0x58
    Y = 0x59
    Z = 0x5A
    NUMPAD_0 = 0x60
    NUMPAD_1 = 0x61
    NUMPAD_2 = 0x62
    NUMPAD_3 = 0x63
    NUMPAD_4 = 0x64
    NUMPAD_5 = 0x65
    NUMPAD_6 = 0x66
    NUMPAD_7 = 0x67
    NUMPAD_8 = 0x68
    NUMPAD_9 = 0x69
    MULTIPLY_KEY = 0x6A
    ADD_KEY = 0x6B
    SEPARATOR_KEY = 0x6C
    SUBTRACT_KEY = 0x6D
    DECIMAL_KEY = 0x6E
    DIVIDE_KEY = 0x6F
    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    F5 = 0x74
    F6 = 0x75
    F7 = 0x76
    F8 = 0x77
    F9 = 0x78
    F10 = 0x79
    F11 = 0x7A
    F12 = 0x7B
    F13 = 0x7C
    F14 = 0x7D
    F15 = 0x7E
    F16 = 0x7F
    F17 = 0x80
    F18 = 0x81
    F19 = 0x82
    F20 = 0x83
    F21 = 0x84
    F22 = 0x85
    F23 = 0x86
    F24 = 0x87
    NUM_LOCK = 0x90
    SCROLL_LOCK = 0x91
    LEFT_SHIFT = 0xA0
    RIGHT_SHIFT = 0xA1
    LEFT_CONTROL = 0xA2
    RIGHT_CONTROL = 0xA3
    LEFT_MENU = 0xA4
    RIGHT_MENU = 0xA5
    BROWSER_BACK = 0xA6
    BROWSER_FORWARD = 0xA7
    BROWSER_REFRESH = 0xA8
    BROWSER_STOP = 0xA9
    BROWSER_SEARCH = 0xAA
    BROWSER_FAVORITES = 0xAB
    BROWSER_START_AND_HOME = 0xAC
    VOLUME_MUTE = 0xAD
    VOLUME_DOWN = 0xAE
    VOLUME_UP = 0xAF
    NEXT_TRACK = 0xB0
    PREVIOUS_TRACK = 0xB1
    STOP_MEDIA = 0xB2
    PLAY_PAUSE_MEDIA = 0xB3
    START_MAIL = 0xB4
    SELECT_MEDIA = 0xB5
    START_APPLICATION_1 = 0xB6
    START_APPLICATION_2 = 0xB7
    ATTN_KEY = 0xF6
    CRSEL_KEY = 0xF7
    EXSEL_KEY = 0xF8
    PLAY_KEY = 0xFA
    ZOOM_KEY = 0xFB
    CLEAR_KEY = 0xFE
    PLUS = 0xBB
    COMMA = 0xBC
    MINUS = 0xBD
    DOT = 0xBE
    SLASH = 0xBF
    GRAVE = 0xC0
    SEMICOLON = 0xBA
    BRACKET_OPEN = 0xDB
    BACKSLASH = 0xDC
    BRACKET_CLOSE = 0xDD
    APOSTROPH = 0xDE
    ACUTE = 0xC0


class System:
    @staticmethod
    def getMousePosition():
        return win32api.GetCursorPos()

    @staticmethod
    def getKeyState(key):
        return win32api.GetKeyState(key)

    @staticmethod
    def keyPressed(key):
        return win32api.GetKeyState(key) < 0

    @staticmethod
    def keyReleased(key):
        return win32api.GetKeyState(key) >= 0


class Key:
    def __init__(self, key=None):
        self.keys = []

        self.__iadd__(key)

    def __iadd__(self, other):
        if other is not None:
            if isinstance(other, list):
                for key in other:
                    self.keys.append(key)
            else:
                self.keys.append(other)
        return self

    def isPressed(self):
        for key in self.keys:
            if not System.keyPressed(key):
                return False
        return True
