import json
import os
import time

import arrow

# This class defines pseudo-constant values similar to a Java interface.
# The other classes in this project should use these magic/constant values.
#
# Chris Joakim, Microsoft

class Constants(object):

    FLAG_ARG_CAPTURE          = '--capture'
    FLAG_ARG_VERBOSE          = '--verbose'
    FLAG_ARG_USE_AZURE_REDIS  = '--use-azure-redis'
    FLAG_ARG_USE_LOCAL_REDIS  = '--use-local-redis'
    FLAG_ARG_NO_TRANSFORM     = '--no-transform'
    FLAG_ARG_SCAN_DOCS        = '--scan-docs'
    FLAG_ARG_POST_PROCESS_IDS = '--post-process'

    REQUEST_CHARGE_HEADER     = 'x-ms-request-charge'
    ACTIVITY_ID_HEADER        = 'x-ms-activity-id'
