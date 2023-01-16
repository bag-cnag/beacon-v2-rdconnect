#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.framework.exceptions import BeaconBadRequest
from server.config import config
import re


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

    if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split(":")[-1])) and ((item[value].lower().startswith('hp')) or (item[value].lower().startswith('obo:hp'))):
        hpo_string = "HP:" + re.split('[_ :]', item[value])[-1]
        hpo = {'id': 'features', 'value': hpo_string}

    return hpo

def set_ordo(item, flt_schema):
    """ Set ORDO filter """
    ordo = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['diagnosis']

    if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split(":")[-1])) and ((item[value].lower().startswith('orpha')) or (item[value].lower().startswith('ordo:orpha'))):
        ordo_string = "Orphanet:" + re.split('[_ :]', item[value])[-1]
        ordo = {'id': 'diagnosis', 'value': ordo_string}
    
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
        gene = {'id': 'genes', 'value': item[value]}
    
    return gene

def set_sex(item, flt_schema):
    """ Set sex filter """
    sex = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['sex']

    if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split(":")[-1])):
        if item[value] == 'NCIT_C16576' or item[value] == 'obo:NCIT_C16576': # female
            sex = {'id': 'sex', 'value': 'F'}
        if item[value] == 'NCIT_C20197' or item[value] == 'obo:NCIT_C20197': # male
            sex = {'id': 'sex', 'value': 'M'}
        if item[value] == 'NCIT_C124294' or item[value] == 'obo:NCIT_C124294': # unknown
            sex = {'id': 'sex', 'value': 'U'}
        if item[value] == 'NCIT_C17998' or item[value] == 'obo:NCIT_C17998': # unknown
            sex = {'id': 'sex', 'value': 'U'}
    
    return sex


def requested_api_version(qparams):
    """ Check api version from request and return corresponding body schema """
    api_version = qparams["meta"]["apiVersion"]

    if api_version == "v0.2":
        ontology_filter_schema = {"version":"v0.2", "key":"id", "value":"value"}
    
    else:
        ontology_filter_schema = {"version":"v0.1","key":"type", "value":"id"}
    
    return ontology_filter_schema


# Function to translate from RequestParameters to PhenoStore filtering
def ps_to_gpap( qparams, psid = None ):
    fltrs = []
    
    #Filters schema keys depending on api version (0.1 & 0.2)
    ontology_filter_schema = requested_api_version(qparams)
    print (ontology_filter_schema)

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