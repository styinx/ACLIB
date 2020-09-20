ID = 0


def text_id():
    global ID
    ID += 1
    return ID


# AC
LAP_ACR = text_id()
LAPS_ACR = text_id()
MINUTE_ACR = text_id()
MINUTES_ACR = text_id()
KM_ACR = text_id()
KPH_ACR = text_id()

# logs, errors, exceptions
LOG_DB_CREATE = text_id()
LOG_DB_EXECUTE = text_id()
EXCEPTION_DB_CREATE = text_id()
EXCEPTION_DB_COMMIT = text_id()

TEXTS = {
    # AC
    LAP_ACR:     'LAP',
    LAPS_ACR:    'LAPS',
    MINUTE_ACR:  'MINUTE',
    MINUTES_ACR: 'MINUTES',
    KM_ACR:      'KM',
    KPH_ACR:     'KM/H',
    # logs, errors, exceptions
    LOG_DB_CREATE: 'Create/Open DB at \'{}\'',
    LOG_DB_EXECUTE: 'Execute \'{}\'',
    EXCEPTION_DB_CREATE: 'Could not establish DB connection to \'{}\'. \n{}',
    EXCEPTION_DB_COMMIT: 'Exception while executing \'{}\'. \n{}'
}


def text(text_id):
    return TEXTS[text_id]
