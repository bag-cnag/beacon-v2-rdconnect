#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.framework.exceptions import BeaconBadRequest
from server.config import config


# List of valid filtering keys per GPAP's endpoint
# _valid_individuals = [ 'id', 'family_id', 'index', 'solved', 'sex', 'affectedStatus', 'lifeStatus' ]
# _valid_biosamples  = [ 'RD_Connect_ID_Experiment', 'EGA_ID', 'Participant_ID', 'Owner', 'in_platform', 'POSTEMBARGO', 'experiment_type', 'kit', 'tissue', 'library_source', 'library_selection', 'library_strategy', 'library_contruction_protocol', 'erns' ]

# Function to translate from RequestParameters to PhenoStore filtering
def ps_to_gpap( qparams, psid = None ):
    fltrs = []
    if psid:
        fltrs.append( { 'id': 'phenotips_id', 'value': psid } )
    if len( qparams[ 'query' ][ 'filters' ] ) > 0:
        for item in qparams[ 'query' ][ 'filters' ]:
            if item["id"].startswith('HP'):
                fltrs.append ({ 'id': 'features', 'value': item["id"] } )
            if item["id"].startswith('Orpha'):
                fltrs.append ({ 'id': 'diagnosis', 'value': item["id"] } )
            if item["id"] == 'NCIT:C16576': # female
                fltrs.append ({ 'id': 'sex', 'value': 'F' } )
            if item["id"] == 'NCIT:C20197': # male
                fltrs.append ({ 'id': 'sex', 'value': 'M' } )
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
            if item["id"] == 'NCIT:C101294':
                fltrs.append( { 'id': 'library_strategy', 'value': [ 'WGS' ] } )
            if item["id"] == 'NCIT:C101295':
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