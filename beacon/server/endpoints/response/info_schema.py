#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from server.config import config

LOG = logging.getLogger(__name__)


def ga4gh_service_info_v10(row, authorized_datasets=None):
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

def build_beacon_response(data, qparams_converted, func_response_type, authorized_datasets=[]):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams_converted, func_response_type),
        'response': build_response(data, qparams_converted, func_response_type, authorized_datasets)
    }
    return beacon_response


def build_meta(qparams, func_response_type):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    meta = {
        'beaconId': config.beacon_id,
        'apiVersion': config.api_version,
        'receivedRequest': build_received_request(qparams),
        'returnedSchemas': [qparams.requestedSchema[0]]
    }
    return meta


def build_received_request(qparams):
    """"Fills the `receivedRequest` part with the request data"""

    request = {
        'meta': {
            'requestedSchemas' : [qparams.requestedSchema[0]],
            'apiVersion' : qparams.apiVersion,
        },
    }

    return request


def build_response(data, qparams, func, authorized_datasets=[]):
    """"Fills the `response` part with the correct format in `results`"""

    response = {
            'results': func(data, qparams, authorized_datasets),
            'info': None,
            'name': config.beacon_name
            # 'resultsHandover': None, # build_results_handover
            # 'beaconHandover': None, # build_beacon_handover
        }

    # build_error(qparams)

    return response


def build_service_info_response(datasets, qparams, authorized_datasets=[]):
    """"Fills the `results` part with the format for ServiceInfo"""

    func = qparams.requestedSchema[1]

    return func(datasets, authorized_datasets)


def build_dataset_info_response(data, qparams, authorized_datasets=[]):
    """"Fills the `results` part with the format for Dataset"""

    func = qparams.requestedSchema[1]
    return [func(row, authorized_datasets) for row in data]
