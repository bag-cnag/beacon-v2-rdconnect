#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.framework.exceptions import BeaconBadRequest
from server.config import config
import re
import json

#Comment as it has to be installed in the docker
#from elasticsearch import Elasticsearch


# List of valid filtering keys per GPAP's endpoint
# _valid_individuals = [ 'id', 'family_id', 'index', 'solved', 'sex', 'affectedStatus', 'lifeStatus' ]
# _valid_biosamples  = [ 'RD_Connect_ID_Experiment', 'EGA_ID', 'Participant_ID', 'Owner', 'in_platform', 'POSTEMBARGO', 'experiment_type', 'kit', 'tissue', 'library_source', 'library_selection', 'library_strategy', 'library_contruction_protocol', 'erns' ]

def set_hpo(item, flt_schema):
    """ Set HPO filter """
    hpo = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['phenotype']

    #For v0.2
    if version == "v0.2":
        key = value = "id"

    if not isinstance(item["id"], list):
        if (key in item) and ((item[value].lower().startswith('hp')) or (item[value].lower().startswith('obo:hp'))):
            hpo_string = "HP:" + re.split('[_ :]', item[value])[-1]
            hpo = {'id': 'features', 'value': hpo_string}
    
    else:
        mult_values = []
        if key in item:
            for obj in item[key]:
                if ((obj.lower().startswith('hp')) or (obj.lower().startswith('obo:hp'))):
                    hpo_string = "HP:" + re.split('[_ :]', obj)[-1]
                    mult_values.append(hpo_string)

        if len(mult_values) > 0:
            hpo = {'id': 'features', 'value': mult_values}

    return hpo

def set_ordo(item, flt_schema):
    """ Set ORDO filter """
    ordo = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['diagnosis']

    #For v0.2
    if version == "v0.2":
        key = value = "id"
    
    if not isinstance(item["id"], list):
        if (key in item) and ((item[value].lower().startswith('orpha')) or (item[value].lower().startswith('ordo:orpha'))):
            ordo_string = "Orphanet:" + re.split('[_ :]', item[value])[-1]
            ordo = {'id': 'diagnosis', 'value': ordo_string}
    
    #If input is an array we are in v0.2
    else:        
        mult_values = []
        if key in item:
            for obj in item[key]:
                if ((obj.lower().startswith('orpha')) or (obj.lower().startswith('ordo:orpha'))):
                    ordo_string = "Orphanet:" + re.split('[_ :]', obj)[-1]
                    mult_values.append(ordo_string)
        
        if len(mult_values) > 0:
            ordo = {'id': 'diagnosis', 'value': mult_values}
        
    return ordo

def set_omim(item, flt_schema):
    """ Set OMIM filter """
    omim = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['diagnosis']

    if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split(":")[-1])) and (item[value].lower().startswith('omim')):
        omim_string = "OMIM:" + re.split('[_ :]', item[value])[-1]
        omim = {'id': 'disorders', 'value': omim_string}
    
    return omim

def set_gene(item, flt_schema):
    """ Set gene filter """
    gene = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['gene']
    
    if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split(":")[-1])):
        if not isinstance(item["value"], list):
            gene = {'id': 'genes', 'value': item[value]}
        else:
            mult_values = []
            for obj in item["value"]:
                mult_values.append(obj)
            if len(mult_values) > 0:
                gene = {'id': 'genes', 'value': mult_values}
    
    return gene

def set_sex(item, flt_schema):
    """ Set sex filter """
    sex = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['sex']

    if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split(":")[-1])):
        if not isinstance(item["value"], list):
            sex = map_sex(item["value"])
        else:
            mult_values = []
            for obj in item["value"]:
                sex = map_sex(obj)
                mult_values.append(sex["value"])
            if len(mult_values) > 0:
                    sex = {'id': 'sex', 'value': mult_values}
    return sex


def map_sex(item):
    """ Sex mapper """
    sex = {}

    if item == 'NCIT_C16576' or item == 'obo:NCIT_C16576': # female
        sex = {'id': 'sex', 'value': 'F'}
    elif item == 'NCIT_C20197' or item == 'obo:NCIT_C20197': # male
        sex = {'id': 'sex', 'value': 'M'}
    elif item == 'NCIT_C124294' or item == 'obo:NCIT_C124294': # unknown
        sex = {'id': 'sex', 'value': 'U'}
    elif item == 'NCIT_C17998' or item == 'obo:NCIT_C17998': # unknown
        sex = {'id': 'sex', 'value': 'U'}
    else:
        sex = {'id': 'sex', 'value': 'None'}
    
    return sex


def requested_api_version(qparams):
    """ Check api version from request and return corresponding body schema """
    api_version = qparams["meta"]["apiVersion"]

    if api_version == "v0.1":
        ontology_filter_schema = {"version":"v0.1","key":"type", "value":"id"}
    else:
        ontology_filter_schema = {"version":"v0.2", "key":"id", "value":"value"}
    
    return ontology_filter_schema


# Function to translate from RequestParameters to PhenoStore filtering
def ps_to_gpap( qparams, psid = None ):
    fltrs = []
    
    #Filters schema keys depending on api version (0.1 & 0.2)
    ontology_filter_schema = requested_api_version(qparams)

    if psid:
        fltrs.append( { 'id': 'phenotips_id', 'value': psid } )
    if len( qparams[ 'query' ][ 'filters' ] ) > 0:
        for item in qparams[ 'query' ][ 'filters' ]:
            #Set filters
            sex_fltr = set_sex(item, ontology_filter_schema)
            hpo_fltr = set_hpo(item, ontology_filter_schema)
            ordo_fltr = set_ordo(item, ontology_filter_schema)
            omim_fltr = set_omim(item, ontology_filter_schema)
            gene_fltr = set_gene(item, ontology_filter_schema)
            
            if sex_fltr:  fltrs.append(sex_fltr)
            if hpo_fltr:  fltrs.append(hpo_fltr)
            if ordo_fltr: fltrs.append(ordo_fltr)
            if omim_fltr: fltrs.append(omim_fltr)
            if gene_fltr: fltrs.append(gene_fltr)

        #If nothing from the above applies
        if len(fltrs) == 0:
            fltrs.append ({ 'id': '_no_filter', 'value': '_no_filter' } )
    
    else:
        fltrs.append ({ 'id': '_no_filter', 'value': '_no_filter' } )
    
    print (fltrs)
    return fltrs

# Function to translate from RequestParameters to DataManagement filtering
def dm_to_gpap( qparams ):
    fltrs = []
    if qparams[ 'targetIdReq' ] and qparams[ 'targetIdReq' ].startswith('B-'):
        #Remove the prefix "B-" added to the participant
        
        print("hello!",qparams[ 'targetIdReq' ]  )
        if qparams[ 'targetIdReq' ].startswith( 'P' ):
            fltrs.append( { 'id': 'Participant_ID', 'value': qparams[ 'targetIdReq' ] } )
        elif qparams[ 'targetIdReq' ].startswith('E') or qparams[ 'targetIdReq' ].startswith( 'C' ): # E real experiments, C fake/demo ones
            fltrs.append( { 'id': 'RD_Connect_ID_Experiment', 'value': qparams[ 'targetIdReq' ] } )
        else:
            raise BeaconBadRequest( 'Invalid provided identifier "{}". It should start by "B-P" or "B-E".'.format( qparams[ 'targetIdReq' ] ) )
    if len( qparams[ 'query' ][ 'filters' ] ) > 0:
        for item in qparams[ 'query' ][ 'filters' ]:
            #Library strategy
            if item["id"] == 'NCIT_C101294':
                fltrs.append( { 'id': 'library_strategy', 'value': [ 'WGS' ] } )
            if item["id"] == 'NCIT_C101295':
                fltrs.append( { 'id': 'library_strategy', 'value': [ 'WXS' ] } )
            
            #ERN
            if (item["id"] in config.filters_in[ 'erns' ]):
                fltrs.append( { 'id': 'erns', 'value': [ item["id"] ] } )


    return fltrs

# For individuals, filtering criteria is expected a dictionary
# having keys matching PhenoStore. This matching is done in
# server/validation.py IndividualParameters
def phenostore_playload( qparams, psid ):
    """
    PhenoStore filtering ciretia to be included as playload in each query.
    """
    return {
        'page'    : 1 + qparams[ 'query' ][ 'pagination' ][ 'skip' ],
        'pageSize': qparams[ 'query' ][ 'pagination' ][ 'limit' ],
        'sorted'  : [],
        'filtered': ps_to_gpap( qparams, psid )
    }


def datamanagement_playload( qparams, groups ):
    """
    DataManagement filtering ciretia to be included as playload in each query.
    """

    payload = {
        'page':     1 + qparams[ 'query' ][ 'pagination' ][ 'skip' ],
        'pageSize': qparams[ 'query' ][ 'pagination' ][ 'limit' ],
        'fields': [
            'RD_Connect_ID_Experiment',
            'Participant_ID',
            'EGA_ID',
            'Owner',
            'in_platform',
            'POSTEMBARGO',
            'experiment_type',
            'kit',
            'tissue',
            'library_source',
            'library_selection',
            'library_strategy',
            'library_contruction_protocol',
            'design_description',
            'read_insert_size'
            'erns',
            'tumour_experiment_id'
        ],
        'sorted':   [],
        'filtered': dm_to_gpap( qparams )
    }

    print (payload['filtered'])

    return payload




#Beacon v1 for variants
def elastic_playload(chrom, start):
    
    es_body = {
          "query": {
            "bool": {
              "must": [
                 {"term" : { "chrom" : chrom }
          },
          {"term" : { "pos" : start }
          }
          ]
        }
      }
    }


    return es_body


def query_elastic(chrom, start):

    elastic_user  = config.elastic_user
    elastic_passwd= config.elastic_password
    elastic_host  = config.elastic_host
    elastic_index = config.elastic_index
    es = Elasticsearch(elastic_host, http_auth=(elastic_user,elastic_passwd))
    res = es.search(index=elastic_index, body=elastic_playload(chrom,start))

    return res


def elastic_resp_handling(qparams, variants_dict):

    #Get from variants dicts
    chrom = variants_dict["chrom"]
    start = variants_dict["start"]
    ref = variants_dict["ref"]
    alt = variants_dict["alt"]

    #Query elastic
    res = query_elastic(chrom,start)

    found=0
    if res['hits']['total']['value'] >=1:
        for result in res['hits']['hits']:
            if result['_source']['alt']==alt and result["_source"]['ref']==ref:
                found+=1
    
  
    #return data
    return found