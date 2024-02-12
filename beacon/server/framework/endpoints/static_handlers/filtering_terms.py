#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response

ejp_spec_filters = [{
        "id": "NCIT_C28421",
        "label": "Sex. Permitted values: NCIT_C16576, NCIT_C20197, NCIT_C124294, NCIT_C17998",
        "type": "alphanumeric"
      },
      {
        "id": "A single value or an array of orphanet terms.",
        "label": "Disease or disorder",
        "type": "ontology"
      },
      {
        "id": "A single value or an array of HPO terms.",
        "label": "Phenotype",
        "type": "ontology"
      },
      {
        "id": "data_2295",
        "label": "Causative genes. Permitted values: any HGNC gene symbol",
        "type": "alphanumeric"
      },
      {
        "id": "NCIT_C83164",
        "label": "Age this year",
        "type": "numeric"
      },
      {
        "id": "NCIT_C124353",
        "label": "Symptom Onset",
        "type": "numeric"
      },
      {
        "id": "NCIT_C156420",
        "label": "Age at diagnosis",
        "type": "numeric"
      },
      {
        "id": "Available Materials",
        "label": "Available materials",
        "type": "alphanumeric"
      }
]
# def filtering_terms(request):    
def filtering_terms():
    async def wrapper( request ):
        rsp = {
            'meta': {
                'beaconId':	config.beacon_id,
                'apiVersion': config.api_version,
                'responseType': 'filteringTerm',
                'returnedSchemas': [ {
                    'entityType': 'filteringTerm',
                    'schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/definitions/FilteringTerm'
                } ],
            },
            'response': {
                #'filteringTerms': config.filters_out,
                'filteringTerms': ejp_spec_filters
            }
        }
        return await json_response( request, rsp )
    return wrapper

