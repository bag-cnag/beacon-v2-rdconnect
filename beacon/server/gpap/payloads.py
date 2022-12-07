#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.framework.exceptions import BeaconBadRequest
from server.config import config
import re


# List of valid filtering keys per GPAP's endpoint
# _valid_individuals = [ 'id', 'family_id', 'index', 'solved', 'sex', 'affectedStatus', 'lifeStatus' ]
# _valid_biosamples  = [ 'RD_Connect_ID_Experiment', 'EGA_ID', 'Participant_ID', 'Owner', 'in_platform', 'POSTEMBARGO', 'experiment_type', 'kit', 'tissue', 'library_source', 'library_selection', 'library_strategy', 'library_contruction_protocol', 'erns' ]

def set_hpo(item):
    """ Set HPO filter """
    hpo = {}
    if ("type" in item) and ((item["type"] == "SIO_010056") or (item["type"] == "sio:SIO_010056")) and ((item["id"].lower().startswith('hp')) or (item["id"].lower().startswith('obo:hp'))):
        hpo_string = "HP:" + re.split('[_ :]', item["id"])[-1]
        hpo = { 'id': 'features', 'value': hpo_string }

    return hpo

def set_ordo(item):
    """ Set ORDO filter """
    ordo = {}
    if ("type" in item) and ((item["type"] == "SIO_001003") or (item["type"] == "sio:SIO_001003")) and ((item["id"].lower().startswith('orpha')) or (item["id"].lower().startswith('ordo:orpha'))):
        ordo_string = "Orphanet:" + re.split('[_ :]', item["id"])[-1]
        ordo = { 'id': 'diagnosis', 'value': ordo_string }
    
    return ordo

def set_omim(item):
    """ Set OMIM filter """
    omim = {}
    if ("type" in item) and ((item["type"] == "SIO_001003") or (item["type"] == "sio:SIO_001003")) and (item["id"].lower().startswith('omim')):
        omim_string = "OMIM:" + re.split('[_ :]', item["id"])[1]
        omim = { 'id': 'disorders', 'value': omim_string }
    
    return omim

def set_gene(item):
    """ Set gene filter """
    gene = {}
    if ('type' in item) and ((item['type'] == 'NCIT_C16612') or (item["type"] == "obo:NCIT_C16612")):
        gene = { 'id': 'genes', 'value': item["id"] }
    
    return gene

def set_sex(item):
    """ Set sex filter """
    sex = {}
    if ("type" in item) and ((item["type"] == "NCIT_C28421") or (item["type"] == "obo:NCIT_C28421")):
        if item["id"] == 'NCIT_C16576' or item["id"] == 'obo:NCIT_C16576': # female
            sex = { 'id': 'sex', 'value': 'F' }
        if item["id"] == 'NCIT_C20197' or item["id"] == 'obo:NCIT_C20197': # male
            sex = { 'id': 'sex', 'value': 'M' }
        if item["id"] == 'NCIT_C124294' or item["id"] == 'obo:NCIT_C124294': # unknown
            sex = { 'id': 'sex', 'value': 'U' }
        if item["id"] == 'NCIT_C17998' or item["id"] == 'obo:NCIT_C17998': # unknown
            sex = { 'id': 'sex', 'value': 'U' }
    
    return sex


# Function to translate from RequestParameters to PhenoStore filtering
def ps_to_gpap( qparams, psid = None ):
    fltrs = []
    if psid:
        fltrs.append( { 'id': 'phenotips_id', 'value': psid } )
    if len( qparams[ 'query' ][ 'filters' ] ) > 0:
        for item in qparams[ 'query' ][ 'filters' ]:

            #HPOs
            #if ("type" in item) and ((item["type"] == "SIO_010056") or (item["type"] == "sio:SIO_010056")) and ((item["id"].lower().startswith('hp')) or (item["id"].lower().startswith('obo:hp'))):
            #    hpo_string = "HP:" + re.split('[_ :]', item["id"])[-1]
            #    fltrs.append ({ 'id': 'features', 'value': hpo_string } )

            #ORDO
            #if ("type" in item) and ((item["type"] == "SIO_001003") or (item["type"] == "sio:SIO_001003")) and ((item["id"].lower().startswith('orpha')) or (item["id"].lower().startswith('ordo:orpha'))):
            #    ordo_string = "Orphanet:" + re.split('[_ :]', item["id"])[-1]
            #    fltrs.append ({ 'id': 'diagnosis', 'value': ordo_string } )

            #OMIM
            #if ("type" in item) and ((item["type"] == "SIO_001003") or (item["type"] == "sio:SIO_001003")) and (item["id"].lower().startswith('omim')):
            #    omim_string = "OMIM:" + re.split('[_ :]', item["id"])[1]
            #    fltrs.append ({ 'id': 'disorders', 'value': omim_string } )

            #Sex
            #if ("type" in item) and ((item["type"] == "NCIT_C28421") or (item["type"] == "obo:NCIT_C28421")):
            #    if item["id"] == 'NCIT_C16576' or item["id"] == 'obo:NCIT_C16576': # female
            #        fltrs.append ({ 'id': 'sex', 'value': 'F' } )
            #    if item["id"] == 'NCIT_C20197' or item["id"] == 'obo:NCIT_C20197': # male
            #        fltrs.append ({ 'id': 'sex', 'value': 'M' } )
            #    if item["id"] == 'NCIT_C124294' or item["id"] == 'obo:NCIT_C124294': # unknown
            #        fltrs.append ({ 'id': 'sex', 'value': 'U' } )
            #    if item["id"] == 'NCIT_C17998' or item["id"] == 'obo:NCIT_C17998': # unknown
            #        fltrs.append ({ 'id': 'sex', 'value': 'U' } )

            #Genes
            #if ('type' in item) and ((item['type'] == 'NCIT_C16612') or (item["type"] == "obo:NCIT_C16612")):
            #    fltrs.append ({ 'id': 'genes', 'value': item["id"] } )

            
            hpo_fltr = set_hpo(item)
            ordo_fltr = set_ordo(item)
            omim_fltr = set_omim(item)
            gene_fltr = set_gene(item)
            sex_fltr = set_sex(item)
            
            if hpo_fltr:  fltrs.append(hpo_fltr)
            if ordo_fltr: fltrs.append(ordo_fltr)
            if omim_fltr: fltrs.append(omim_fltr)
            if gene_fltr: fltrs.append(gene_fltr)
            if sex_fltr:  fltrs.append(sex_fltr)

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