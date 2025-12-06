# =================================================================================
#    GET ALL MEASUREMENTS
# =================================================================================

GET_ALL_MEASUREMENTS_SUMMARY = 'List all measurements'
GET_ALL_MEASUREMENTS_DESCRIPTION = '''
- Return all measurements stored in the system for all sensors.
- Include the sensor identifier for each measurement.
- Mainly intended for debugging, testing, or simple data views.
'''
GET_ALL_MEASUREMENTS_TYPE_FILTER_DESCRIPTION = 'Optionally restrict results to a single measurement type. If omitted, measurements of all types are included.'

# =================================================================================
#    CREATE NEW MEASUREMENT
# =================================================================================

CREATE_MEASUREMENT_SUMMARY = 'Create a new measurement'
CREATE_MEASUREMENT_DESCRIPTION = '''
- Store a single measurement sent by a sensor.
- Use the sensor ID to link the measurement to an existing sensor.
- Provide the measurement payload with value, unit, and type.
- The timestamp can be sent explicitly; if omitted, it is generated automatically by the server.
'''

# =================================================================================
#    GET MEASUREMENT BY ID
# =================================================================================

GET_MEASUREMENT_BY_ID_SUMMARY = 'Get a measurement by ID'
GET_MEASUREMENT_BY_ID_DESCRIPTION = '''
- Fetch a single measurement using its unique ID.
- Return the measurement values and metadata.
- Include the identifier of the sensor that produced the measurement.
'''

# =================================================================================
#    DELETE MEASUREMENT BY ID
# =================================================================================

DELETE_MEASUREMENT_BY_ID_SUMMARY = 'Delete a measurement by ID'
DELETE_MEASUREMENT_BY_ID_DESCRIPTION = '''
- Delete a single measurement using its unique ID.
- Permanently remove the measurement from the database.
- Return only the HTTP status code, without a response body.
'''
