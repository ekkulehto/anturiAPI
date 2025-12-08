# =================================================================================
#    GET SENSOR STATUS HISTORY BY ID
# =================================================================================

GET_SENSOR_STATUS_HISTORY_BY_ID_SUMMARY = 'Get sensor status history by ID'
GET_SENSOR_STATUS_HISTORY_BY_ID_DESCRIPTION = '''
- Return the status change history for a given sensor.
- Include timestamps for each status change.
- Useful for analysing how often and when the sensor has been in ERROR state.
'''
GET_SENSOR_STATUS_HISTORY_BY_ID_FILTER_DESCRIPTION = 'Optionally restrict results to a single status value. If omitted, all recorded status changes are included.'

# =================================================================================
#    CHANGE SENSOR STATUS BY ID
# =================================================================================

CHANGE_SENSOR_STATUS_BY_ID_SUMMARY = 'Change sensor status by ID'
CHANGE_SENSOR_STATUS_BY_ID_DESCRIPTION = '''
- Change the current status of a sensor.
- Record each status change in the sensor status history with a timestamp.
- Intended for external systems or operators to control sensor state.
'''
