#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import web

from . import handlers
from . import info as info_handler

routes = [
    # Info
    web.get('/api'                  , info_handler.info('api')),
    web.get('/api/'                 , info_handler.info('api')),
    web.get('/api/info'             , info_handler.info('api/info')),
    web.get('/api/service-info'     , info_handler.ga4gh('api/service-info')),
    web.get('/api/map'              , info_handler.map('api/map')),
    web.get('/api/configuration'    , info_handler.config_txt('api/configuration')),
    web.get('/api/entry_types'      , info_handler.entry_types('api/entry_types')),
    web.get('/api/filtering_terms'  , info_handler.filtering_terms('api/filtering_terms')),

    # Datasets
    #web.get('/api/datasets'         , datasets.handler), # NOT IMPLEMENTED

    # Schemas
    # web.get('/api/schemas'          , schemas.handler),

    # Genomic query
    # web.get('/api/genomic_snp'                      , genomic_query.handler),
    # web.get('/api/genomic_region'                   , genomic_query.handler),

    # Biosamples
    web.post('/api/biosamples'                               , handlers.biosamples_by_biosample),    # IMPLEMENTED --> experiments
    web.post('/api/biosamples/{target_id_req}'               , handlers.biosamples_by_biosample),
    web.post('/api/biosamples/{target_id_req}/g_variants'    , handlers.gvariants_by_biosample),
    web.post('/api/biosamples/{target_id_req}/individuals'   , handlers.individuals_by_biosample),
    
    # # Individuals
    web.post('/api/individuals'                              , handlers.individuals_by_individual),  # IMPLEMENTED --> participant
    web.post('/api/individuals/{target_id_req}'              , handlers.individuals_by_individual),
    web.post('/api/individuals/{target_id_req}/g_variants'   , handlers.gvariants_by_individual),
    web.post('/api/individuals/{target_id_req}/biosamples'   , handlers.biosamples_by_individual),

    # # GVariant
    web.post('/api/g_variants'                               , handlers.gvariants_by_variant),
    web.post('/api/g_variants/{target_id_req}'               , handlers.gvariants_by_variant),
    web.post('/api/g_variants/{target_id_req}/biosamples'    , handlers.individuals_by_variant),
    web.post('/api/g_variants/{target_id_req}/individuals'   , handlers.biosamples_by_variant),

    # Cohorts
    web.post('/api/cohorts'                                  , handlers.cohorts_by_cohort),
    web.post('/api/cohorts/{target_id_req}'                  , handlers.cohorts_by_cohort),

    # TESTING
    web.get( '/api/test'                                     , handlers.test),
    web.post('/api/test'                                     , handlers.test),
]
