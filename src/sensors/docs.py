GET_ALL_SENSORS_SUMMARY = 'List all sensors'
GET_ALL_SENSORS_DESCRIPTION = (
    'Return all sensors registered in the system. '
    'Optionally filter the result by the current status of the sensor.'
)
GET_ALL_SENSORS_STATUS_FILTER_DESCRIPTION = (
    'Filter sensors by their current status. '
    'If omitted, all sensors are returned.'
)

CREATE_SENSOR_SUMMARY = 'Create a new sensor'
CREATE_SENSOR_DESCRIPTION = (
    'Register a new sensor in the system and assign it to an existing segment. '
    'The sensor is created with status NORMAL by default.'
)

GET_SENSOR_BY_ID_SUMMARY = 'Get a sensor with its measurements'
GET_SENSOR_BY_ID_DESCRIPTION = (
    'Fetch a single sensor by its unique ID, including its basic information and measurements. '
    'Measurements can be filtered by limit and time range (since/until).'
)

UPDATE_SENSOR_BY_ID_SUMMARY = 'Update a sensor by ID'
UPDATE_SENSOR_BY_ID_DESCRIPTION = (
    'Update basic fields of an existing sensor, such as its name or the segment it belongs to. '
    'Only the fields provided in the request body are updated.'
)

DELETE_SENSOR_BY_ID_SUMMARY = 'Delete a sensor by ID'
DELETE_SENSOR_BY_ID_DESCRIPTION = (
    'Delete a sensor from the system by its unique ID. '
    'Depending on the database configuration, this may also remove its measurements.'
)

GET_SENSOR_STATUS_HISTORY_BY_ID_SUMMARY = 'Get sensor status history'
GET_SENSOR_STATUS_HISTORY_BY_ID_DESCRIPTION = (
    'Return the status change history for a given sensor, including timestamps. '
    'This can be used, for example, to build a chart of error occurrences over time.'
)
GET_SENSOR_STATUS_HISTORY_BY_ID_FILTER_DESCRIPTION = (
    'Optional filter for status history entries. '
    'If omitted, all status changes are returned.'
)

CHANGE_SENSOR_STATUS_SUMMARY = 'Change sensor status'
CHANGE_SENSOR_STATUS_DESCRIPTION = (
    'Change the current status of a sensor. '
    'Each status change is recorded in the sensor status history with a timestamp.'
)
