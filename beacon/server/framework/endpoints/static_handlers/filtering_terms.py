#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response
from server.utils.request_origin import check_request_origin

def generate_hpo_filters():
    """Generate filter objects for each HPO ID"""
    hpo_ids = config.filters_in.get('hpos', [])
    # Filter out empty strings
    hpo_ids = [hpo_id for hpo_id in hpo_ids if hpo_id.strip()]
    
    hpo_filters = []
    for hpo_id in hpo_ids:
        hpo_filters.append({
            "id": hpo_id,
            "label": "Phenotype",
            "type": "ontology",
            "scopes": ["individuals"]
        })
    
    return hpo_filters

def generate_ordo_filters():
    """Generate filter objects for each Orphanet ID"""
    ordo_ids = config.filters_in.get('ordos', [])
    # Filter out empty strings
    ordo_ids = [ordo_id for ordo_id in ordo_ids if ordo_id.strip()]
    
    ordo_filters = []
    for ordo_id in ordo_ids:
        ordo_filters.append({
            "id": ordo_id,
            "label": "Diagnosis",
            "type": "ontology",
            "scopes": ["individuals"]
        })
    
    return ordo_filters
  
def generate_omim_filters():
    """Generate filter objects for each OMIM ID"""
    omim_ids = config.filters_in.get('omims', [])
    # Filter out empty strings
    omim_ids = [omim_id for omim_id in omim_ids if omim_id.strip()]
    
    omim_filters = []
    for omim_id in omim_ids:
        omim_filters.append({
            "id": omim_id,
            "label": "Disorder",
            "type": "ontology",
            "scopes": ["individuals"]
        })
    
    return omim_filters

ejp_spec_filters = [
      #Individuals filters 
      {
        "id": "ncit_C28421",
        "label": "Sex. Permitted values: ncit_C16576, ncit_C20197, ncit_C124294, ncit_C17998",
        "type": "alphanumeric",
        "scopes": ["individuals"]
      },
      {
        "id": "edam:data_2295",
        "label": "Causative genes. Permitted values: a single value or an array of HGNC gene symbols",
        "type": "alphanumeric",
        "scopes": ["individuals"]
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
        "scopes": ["biosamples"]
      },
      {
        "id": "ERN",
        "label": "ERN. Permitted values: any existing ERN",
        "type": "alphanumeric",
        "scopes": ["biosamples"]
      },


      #G_variants filters
      {  
        #Id "DNA sequencing class"
        "id": "referenceName",
        "label": "Chromosome",
        "type": "alphanumeric",
        "scopes": ["genomicVariations"]
      },
      {
        "id": "start",
        "label": "Chromosome position",
        "type": "numeric",
        "scopes": ["genomicVariations"]
      },
      {  
        "id": "referenceBases",
        "label": "Reference allele",
        "type": "alphanumeric",
        "scopes": ["genomicVariations"]
      },
      {  
        "id": "alternateBases",
        "label": "Alternate allele",
        "type": "alphanumeric",
        "scopes": ["genomicVariations"]
      }
]


beacon_spec_filters = [
      #Individuals filters 
      {
        "id": "NCIT:C20197",
        "label": "male",
        "type": "ontology",
        "scopes": ["individuals"]
      },
      {
        "id": "NCIT:C16576",
        "label": "female",
        "type": "ontology",
        "scopes": ["individuals"]
      },
      {
        "id": "NCIT:C17998",
        "label": "unknown",
        "type": "ontology",
        "scopes": ["individuals"]
      },
      {
        "id": "edam:data_2295",
        "label": "Causative gene. Permitted values: a single value of a HGNC gene symbol",
        "type": "alphanumeric",
        "scopes": ["individuals"]
      },
      
      #Biosamples filters
      {  

        #Id "DNA sequencing class"
        "id": "NCIT:C153598",
        "label": "Library strategy. Permitted values: NCIT:C101294, NCIT:C101295",
        "type": "alphanumeric",
        "scopes": ["biosamples"]
      },

      {
        "id": "subproject",
        "label": "Subproject. Permitted values: any existing subproject e.g. NAGENPEDIATRICS",
        "type": "alphanumeric",
        "scopes": ["biosamples"]
      },
      #{
      #  "id": "ERN",
      #  "label": "ERN. Permitted values: any existing ERN",
      #  "type": "alphanumeric",
      #  "scopes": ["biosamples"]
      #}
      
      
      #G_variants filters
      {  
        "id": "assemblyId",
        "label": "Genome assembly. Permitted values: hg19,GRCh37,hg38,GRCh38",
        "type": "alphanumeric",
        "scopes": ["genomicVariations"]
      },
      {  
        "id": "referenceName",
        "label": "Chromosome",
        "type": "alphanumeric",
        "scopes": ["genomicVariations"]
      },
      {
        "id": "start",
        "label": "Chromosome position",
        "type": "numeric",
        "scopes": ["genomicVariations"]
      },
      {  
        "id": "referenceBases",
        "label": "Reference allele",
        "type": "alphanumeric",
        "scopes": ["genomicVariations"]
      },
      {  
        "id": "alternateBases",
        "label": "Alternate allele",
        "type": "alphanumeric",
        "scopes": ["genomicVariations"]
      }
]

# def filtering_terms(request):    
def filtering_terms():
    async def wrapper( request ):
         
        req_origin = check_request_origin()
        spec_filters =  ejp_spec_filters if req_origin == 'ejp' else beacon_spec_filters
  
        scope_endpoint = str(request.url).split("/")[-2]

        if scope_endpoint == "g_variants": scope_endpoint = "genomicVariations"
        f_spec_filters = [d for d in spec_filters if d.get("scopes")[0] == scope_endpoint]
        if not f_spec_filters: f_spec_filters = list(spec_filters)  # Create a copy to avoid mutating the module-level list
        
        # Add HPO and Orphanet filters for individuals scope
        if scope_endpoint == "individuals" or scope_endpoint == "api":
            hpo_filters = generate_hpo_filters()
            ordo_filters = generate_ordo_filters()
            omim_filters = generate_omim_filters()
            f_spec_filters.extend(hpo_filters)
            f_spec_filters.extend(ordo_filters)
            f_spec_filters.extend(omim_filters)
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

