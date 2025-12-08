# =================================================================================
#    GET ALL SEGMENTS
# =================================================================================

GET_ALL_SEGMENTS_SUMMARY = 'List all segments'
GET_ALL_SEGMENTS_DESCRIPTION = '''
- Return all segments defined in the system.
- Include basic information about each segment.
- A segment may have zero or more sensors attached to it.
'''

# =================================================================================
#    CREATE NEW SEGMENT
# =================================================================================

CREATE_SEGMENT_SUMMARY = 'Create a new segment'
CREATE_SEGMENT_DESCRIPTION = '''
- Create a new segment in the factory layout.
- Use segments to represent logical or physical areas in the hall.
- Sensors can be assigned to segments after they have been created.
'''

# =================================================================================
#    GET SEGMENT BY ID
# =================================================================================

GET_SEGMENT_BY_ID_SUMMARY = 'Get a segment by ID'
GET_SEGMENT_BY_ID_DESCRIPTION = '''
- Return a single segment using its unique ID.
- Optionally filter segment's sensors by their current status
- Include all sensors that belong to the segment.
- For each sensor, include it's latest measurement if any.
- Intended for viewing the state of one physical area at a glance.
'''

# =================================================================================
#    UPDATE SEGMENT BY ID
# =================================================================================

UPDATE_SEGMENT_BY_ID_SUMMARY = 'Update a segment by ID'
UPDATE_SEGMENT_BY_ID_DESCRIPTION = '''
- Update basic information for an existing segment, such as its name.
- Do not directly modify the sensors assigned to the segment.
- Sensors can be moved between segments using the sensor endpoints.
'''

# =================================================================================
#    DELETE SEGMENT BY ID
# =================================================================================

DELETE_SEGMENT_BY_ID_SUMMARY = 'Delete a segment by ID'
DELETE_SEGMENT_BY_ID_DESCRIPTION = '''
- Delete a segment by its unique ID.
- A segment can only be deleted if it has no sensors assigned to it.
- If the segment still contains sensors, the operation will fail with an error response.
- Return only the HTTP status code, without a response body.
'''
