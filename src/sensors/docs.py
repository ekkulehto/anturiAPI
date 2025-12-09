# =================================================================================
#    GET ALL SENSORS
# =================================================================================

GET_ALL_SENSORS_SUMMARY = 'List all sensors'
GET_ALL_SENSORS_DESCRIPTION = '''
- Return all sensors registered in the system.
- Include basic information and the segment each sensor belongs to.
- Intended for general overview and management of all sensors.
'''
GET_ALL_SENSORS_STATUS_FILTER_DESCRIPTION = 'Filter sensors by their current status. If omitted, sensors in all statuses are included.'

# =================================================================================
#    CREATE NEW SENSOR
# =================================================================================

CREATE_SENSOR_SUMMARY = 'Create a new sensor'
CREATE_SENSOR_DESCRIPTION = '''
- Register a new sensor in the system.
- Assign the sensor to an existing segment.
- The sensor is created with status NORMAL by default.
'''

# =================================================================================
#    GET SENSOR BY ID
# =================================================================================

GET_SENSOR_BY_ID_SUMMARY = 'Get a sensor by ID'
GET_SENSOR_BY_ID_DESCRIPTION = '''
- Fetch a single sensor by its unique ID.
- Include sensor details, and the segment it belongs to.
'''

# =================================================================================
#    UPDATE SENSOR BY ID
# =================================================================================

UPDATE_SENSOR_BY_ID_SUMMARY = 'Update a sensor by ID'
UPDATE_SENSOR_BY_ID_DESCRIPTION = '''
- Update basic fields of an existing sensor, such as its name.
- Optionally change the segment the sensor belongs to.
- Only the fields provided in the request body are updated.
'''

# =================================================================================
#    DELETE SENSOR BY ID
# =================================================================================

DELETE_SENSOR_BY_ID_SUMMARY = 'Delete a sensor by ID'
DELETE_SENSOR_BY_ID_DESCRIPTION = '''
- Delete a sensor from the system by its unique ID.
- Also remove all measurements and status history associated with this sensor.
- Return only the HTTP status code, without a response body.
'''