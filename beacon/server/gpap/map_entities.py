#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.model.schemas.default import *

def individuals( ind_list, qparmas ):
    return [ beacon_individual( x ) for x in ind_list ]


def experiments( exp_list, qparams ):
    participants = list( set( [ x[ 'Participant_ID' ] for x in exp_list ] ) )
    biosamples = []
    for part_id in participants:
        part_exps = [ x for x in exp_list if x[ 'Participant_ID' ] == part_id ]
        biosamples.append( beacon_biosample( part_exps ) )
    return biosamples


def variants( ind_list, qparmas ):
    return [ beacon_individual( x ) for x in ind_list ]