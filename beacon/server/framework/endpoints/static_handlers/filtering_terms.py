#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response
from server.utils.request_origin import check_request_origin

ejp_spec_filters = [
      #Individuals filters 
      {
        "id": "NCIT_C28421",
        "label": "Sex. Permitted values: NCIT_C16576, NCIT_C20197, NCIT_C124294, NCIT_C17998",
        "type": "alphanumeric",
        "scope": ["individuals"]
      },
      {
        "id": "A single Orphanet id or an array of Orphanet ids (e.g. Orphanet_141091)",
        "label": "Disease or disorder",
        "type": "ontology",
        "scope": ["individuals"]

      },
      {
        "id": "A single HPO id or an array of HPO ids (e.g. HP_0000957)",
        "label": "Phenotype",
        "type": "ontology",
        "scope": ["individuals"]

      },
      {
        "id": "data_2295",
        "label": "Causative genes. Permitted values: a single value or an array of HGNC gene symbols",
        "type": "alphanumeric",
        "scope": ["individuals"]
      },

      #Currently not supported
      #{
      #  "id": "NCIT_C83164",
      #  "label": "Age this year",
      #  "type": "numeric",
      #  "scope": "individuals"
      #},
      #{
      #  "id": "NCIT_C124353",
      #  "label": "Symptom Onset",
      #  "type": "numeric",
      #  "scope": "individuals"
      #},
      #{
      #  "id": "NCIT_C156420",
      #  "label": "Age at diagnosis",
      #  "type": "numeric",
      #  "scope": "individuals"
      #},
      #{
      #  "id": "Available Materials",
      #  "label": "Available materials",
      #  "type": "alphanumeric",
      #  "scope": "individuals"
      #},

      #Biosamples filters
      {  

        #Id "DNA sequencing class"
        "id": "NCIT_C153598",
        "label": "Library strategy. Permitted values: NCIT_C101294, NCIT_C101295",
        "type": "alphanumeric",
        "scope": ["biosamples"]
      },
      {
        "id": "ERN",
        "label": "ERN. Permitted values: any existing ERN",
        "type": "alphanumeric",
        "scope": ["biosamples"]
      },


      #G_variants filters
      {  
        #Id "DNA sequencing class"
        "id": "referenceName",
        "label": "Chromosome",
        "type": "alphanumeric",
        "scope": ["genomicVariations"]
      },
      {
        "id": "start",
        "label": "Chromosome position",
        "type": "numeric",
        "scope": ["genomicVariations"]
      },
      {  
        "id": "referenceBases",
        "label": "Reference allele",
        "type": "alphanumeric",
        "scope": ["genomicVariations"]
      },
      {  
        "id": "alternateBases",
        "label": "Alternate allele",
        "type": "alphanumeric",
        "scope": ["genomicVariations"]
      }
]


beacon_spec_filters = [
      #Individuals filters 
      {
        "id": "NCIT:C20197",
        "label": "male",
        "type": "ontology",
        "scope": ["individuals"]
      },
      {
        "id": "NCIT:C16576",
        "label": "female",
        "type": "ontology",
        "scope": ["individuals"]
      },
      {
        "id": "NCIT:C17998",
        "label": "unknown",
        "type": "ontology",
        "scope": ["individuals"]
      },
      {
        "id": "A single Orphanet id or an array of Orphanet ids (e.g. Orphanet:141091)",
        "label": "Disease or disorder",
        "type": "ontology",
        "scope": ["individuals"]

      },
      {
        "id": "A single HPO id or an array of HPO ids (e.g. HP:0000957)",
        "label": "Phenotype",
        "type": "ontology",
        "scope": ["individuals"]

      },
      #Biosamples filters
      {  

        #Id "DNA sequencing class"
        "id": "NCIT:C153598",
        "label": "Library strategy. Permitted values: NCIT:C101294, NCIT:C101295",
        "type": "alphanumeric",
        "scope": ["biosamples"]
      },
      {
        "id": "ERN",
        "label": "ERN. Permitted values: any existing ERN",
        "type": "alphanumeric",
        "scope": ["biosamples"]
      },
      #G_variants filters
      {  
        #Id "DNA sequencing class"
        "id": "referenceName",
        "label": "Chromosome",
        "type": "alphanumeric",
        "scope": ["genomicVariations"]
      },
      {
        "id": "start",
        "label": "Chromosome position",
        "type": "numeric",
        "scope": ["genomicVariations"]
      },
      {  
        "id": "referenceBases",
        "label": "Reference allele",
        "type": "alphanumeric",
        "scope": ["genomicVariations"]
      },
      {  
        "id": "alternateBases",
        "label": "Alternate allele",
        "type": "alphanumeric",
        "scope": ["genomicVariations"]
      }
]

# def filtering_terms(request):    
def filtering_terms():
    async def wrapper( request ):
         
        req_origin = check_request_origin()
        spec_filters =  ejp_spec_filters if req_origin == 'ejp' else beacon_spec_filters
  
        scope_endpoint = str(request.url).split("/")[-2]

        if scope_endpoint == "g_variants": scope_endpoint = "genomicVariations"
        f_spec_filters = [d for d in spec_filters if d.get("scope") == scope_endpoint]
        if not f_spec_filters: f_spec_filters = spec_filters

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
                'filteringTerms': f_spec_filters
            }
        }
        return await json_response( request, rsp )
    return wrapper

