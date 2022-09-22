#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response

#def ga4gh( request ):
def ga4gh():
    async def wrapper( request ):
        LOG.debug( 'Running a GET "ga4gh" request' )
        return await json_response( request, ga4gh_service_info_v10() )
    return wrapper

def ga4gh_service_info_v10():
    return {
        'id': config.beacon_id,
        'name': config.beacon_name,
        'type': {
            'group': config.ga4gh_service_type_group,
            'artifact': config.ga4gh_service_type_artifact,
            'version': config.ga4gh_service_type_version
        },
        'description': config.description,
        'organization': {
            'name': config.org_name,
            'url': config.org_welcome_url
        },
        'contactUrl': config.org_contact_url,
        'documentationUrl': config.documentation_url,
        'createDateTime': config.create_datetime,
        'updateDateTime': config.update_datetime,
        'environment': config.environment,
        'version': config.version,
        'url': config.service_url,
    }