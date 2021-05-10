#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.utils.exceptions import BeaconBadRequest

# List of valid filtering keys per GPAP's endpoint
_valid_individuals = ['id', 'family_id', 'index', 'solved', 'sex', 'affectedStatus', 'lifeStatus' ]
_valid_biosamples  = ['RD_Connect_ID_Experiment', 'EGA_ID', 'Participant_ID', 'Owner', 'in_platform', 'POSTEMBARGO', 'experiment_type', 'kit', 'tissue', 'library_source', 'library_selection', 'library_strategy', 'library_contruction_protocol', 'erns']

# Function to translate from RequestParameters to PhenoStore filtering
def ps_to_gpap(qparams):
    fltrs = []
    for qkey in _valid_individuals:
        x = getattr(qparams, qkey)
        if x:
            fltrs.append({ 'id': qkey, 'value': x})
    return fltrs

# Function to translate from RequestParameters to DataManagement filtering
def dm_to_gpap(qparams):
    fltrs = []
    if qparams.targetIdReq:
        if qparams.targetIdReq.startswith('P'):
            fltrs.append({'id': 'Participant_ID', 'value': qparams.targetIdReq})
        elif qparams.targetIdReq.startswith('E') or qparams.targetIdReq.startswith('C'): # E real experiments, C fake/demo ones
            fltrs.append({'id': 'RD_Connect_ID_Experiment', 'value': qparams.targetIdReq})
        else:
            raise BeaconBadRequest('Invalid provided identifier "{}". It should start by "P" or "E".'.format(qparams.targetIdReq))
    for qkey in _valid_biosamples:
        x = getattr(qparams, qkey)
        if x:
            fltrs.append({ 'id': qkey, 'value': x})
    return fltrs

# For individuals, filtering criteria is expected a dictionarly
# having keys matching PhenoStore. This matching is done in
# server/validation.py IndividualParameters
def phenostore_playload(qparams):
    """
    PhenoStore filtering ciretia to be included as playload in each query.
    """
    return {
        'page':     1 + qparams.skip,
        'pageSize': qparams.limit,
        'sorted':   [],
        'filtered': ps_to_gpap(qparams)
    }


def datamanagement_playload(qparams, groups):
    """
    DataManagement filtering ciretia to be included as playload in each query.
    """
    return {
        'page':     1 + qparams.skip,
        'pageSize': qparams.limit,
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
        'filtered': dm_to_gpap(qparams)
    }