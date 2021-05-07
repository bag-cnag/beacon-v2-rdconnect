#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# List of valid filtering keys per GPAP's endpoint
_valid_individuals = ['id', 'family_id', 'index', 'solved', 'sex', 'affectedStatus', 'lifeStatus' ]

# Function to translate from RequestParameters to PhenoStore filtering
def to_ps(qparams):
    fltrs = []
    for qkey in _valid_individuals:
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
    LOG.debug(to_ps(qparams))
    return {
        'page':     1 + qparams.skip,
        'pageSize': qparams.limit,
        'sorted':   [],
        'filtered': to_ps(qparams)
    }