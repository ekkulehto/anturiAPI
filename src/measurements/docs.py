# =================================================================================
#    GET ALL MEASUREMENTS
# =================================================================================

GET_SENSOR_MEASUREMENTS_BY_ID_SUMMARY = 'List sensor measurements by ID'
GET_SENSOR_MEASUREMENTS_BY_ID_DESCRIPTION = '''
- Fetch a single sensor by its unique ID.
- Include sensor details, the segment it belongs to, and its measurements.
'''

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
