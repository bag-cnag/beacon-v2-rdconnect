#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response

ejp_spec_filters = [
      #Individuals filters 
      {
        "id": "NCIT_C28421",
        "label": "Sex. Permitted values: NCIT_C16576, NCIT_C20197, NCIT_C124294, NCIT_C17998",
        "type": "alphanumeric",
        "scope": "individuals"
      },
      {
        "id": "A single value or an array of orphanet terms.",
        "label": "Disease or disorder",
        "type": "ontology",
        "scope": "individuals"

      },
      {
        "id": "A single value or an array of HPO terms.",
        "label": "Phenotype",
        "type": "ontology",
        "scope": "individuals"

      },
      {
        "id": "data_2295",
        "label": "Causative genes. Permitted values: a HGNC gene symbol",
        "type": "alphanumeric",
        "scope": "individuals"
      },

      #Currently not supported
      {
        "id": "NCIT_C83164",
        "label": "Age this year",
        "type": "numeric",
        "scope": "individuals"
      },
      {
        "id": "NCIT_C124353",
        "label": "Symptom Onset",
        "type": "numeric",
        "scope": "individuals"
      },
      {
        "id": "NCIT_C156420",
        "label": "Age at diagnosis",
        "type": "numeric",
        "scope": "individuals"
      },
      {
        "id": "Available Materials",
        "label": "Available materials",
        "type": "alphanumeric",
        "scope": "individuals"
      },

      #Biosamples filters
      {  

        #Id "DNA sequencing class"
        "id": "NCIT_C153598",
        "label": "Libary strategy. Permitted values: NCIT_C101294, NCIT_C101295",
        "type": "alphanumeric",
        "scope": "biosamples"
      },
      {
        "id": "ERN",
        "label": "ERN. Permitted values: any existing ERN",
        "type": "alphanumeric",
        "scope": "biosamples"
      },


      #G_variants filters
      {  
        #Id "DNA sequencing class"
        "id": "referenceName",
        "label": "Chromosome",
        "type": "alphanumeric",
        "scope": "genomicVariations"
      },
      {
        "id": "start",
        "label": "Chromosome position",
        "type": "numeric",
        "scope": "genomicVariations"
      },
      {  
        "id": "referenceBases",
        "label": "Reference allele",
        "type": "alphanumeric",
        "scope": "genomicVariations"
      },
      {  
        "id": "alternateBases",
        "label": "Alternate allele",
        "type": "alphanumeric",
        "scope": "genomicVariations"
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

