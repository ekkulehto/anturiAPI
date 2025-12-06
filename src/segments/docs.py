# =================================================================================
#    GET ALL SEGMENTS
# =================================================================================

GET_ALL_SEGMENTS_SUMMARY = 'List all segments'
GET_ALL_SEGMENTS_DESCRIPTION = (
    'Return all segments defined in the system. '
    'A segment may have zero or more sensors attached to it.'
)

# =================================================================================
#    CREATE NEW SEGMENT
# =================================================================================

CREATE_SEGMENT_SUMMARY = 'Create a new segment'
CREATE_SEGMENT_DESCRIPTION = (
    'Create a new segment in the factory layout. '
    'Segments are logical or physical areas to which sensors can be assigned.'
)

# =================================================================================
#    GET SEGMENT BY ID
# =================================================================================

GET_SEGMENT_BY_ID_SUMMARY = 'Get a segment by ID'
GET_SEGMENT_BY_ID_DESCRIPTION = (
    'Return a segment with its sensors and their measurements. '
    'By default, only the latest measurement per sensor is included, but this can be '
    'customised using query parameters (limit, measurement type, and time range).'
)

# =================================================================================
#    UPDATE SEGMENT BY ID
# =================================================================================

UPDATE_SEGMENT_BY_ID_SUMMARY = 'Update a segment by ID'
UPDATE_SEGMENT_BY_ID_DESCRIPTION = (
    'Update basic information for an existing segment, such as its name. '
    'This operation does not directly modify the sensors assigned to the segment.'
)

# =================================================================================
#    DELETE SEGMENT BY ID
# =================================================================================

DELETE_SEGMENT_BY_ID_SUMMARY = 'Delete a segment by ID'
DELETE_SEGMENT_BY_ID_DESCRIPTION = (
    'Delete a segment by its unique ID. '
    'A segment can only be deleted if it has no sensors assigned to it. '
    'If the segment still contains sensors, the operation should fail with an error response. '
    'Does not return any content, only the HTTP status code.'
)
