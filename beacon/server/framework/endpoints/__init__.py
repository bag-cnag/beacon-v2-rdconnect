#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import web

import server.framework.endpoints.map as map



#
# ROUTES
#############################################################################################################


routes = [
    # Test endpoints
    web.get('/api/test'                                      , map.query_test),
    web.post('/api/test'                                     , map.query_test),

    # Datasets
    web.post('/api/datasets'                                 , map.query_datasets_by_dataset),
    #web.post('/api/datasets/{target_id_req}'                 , map.query_datasets_by_dataset),
    
    # Individuals
    web.post('/api/individuals'                              , map.query_individuals_by_individuals),
    web.post('/api/individuals/{target_id_req}'              , map.query_individuals_by_individuals),
    
    # Biosamples
    web.post('/api/biosamples'                               , map.query_biosamples_by_biosample),
    web.post('/api/biosamples/{target_id_req}'               , map.query_biosamples_by_biosample),

    # Cohorts
    #web.post('/api/cohorts'                                  , map.query_cohorts_by_cohort),
    #web.post('/api/cohorts/{target_id_req}'                  , map.query_cohorts_by_cohort),
]



"""
# Individuals in beacon map to particpiant in GPAP
web.post('/api/individuals'                              , query_individuals_by_individual),
web.post('/api/individuals/{target_id_req}'              , query_individuals_by_individual),
web.post('/api/individuals/{target_id_req}/g_variants'   , query_gvariants_by_individual),
web.post('/api/individuals/{target_id_req}/biosamples'   , query_biosamples_by_individual),


# Biosamples
web.post('/api/biosamples'                               , biosamples_by_biosample),    # IMPLEMENTED --> experiments
web.post('/api/biosamples/{target_id_req}'               , biosamples_by_biosample),
web.post('/api/biosamples/{target_id_req}/g_variants'    , gvariants_by_biosample),
web.post('/api/biosamples/{target_id_req}/individuals'   , individuals_by_biosample),

# Genomic Variant
web.post('/api/g_variants'                               , gvariants_by_variant),
web.post('/api/g_variants/{target_id_req}'               , gvariants_by_variant),
web.post('/api/g_variants/{target_id_req}/biosamples'    , individuals_by_variant),
web.post('/api/g_variants/{target_id_req}/individuals'   , biosamples_by_variant),

# Genomic query
web.get('/api/genomic_snp'                               , genomic_query.handler),
web.get('/api/genomic_region'                            , genomic_query.handler),
"""

# Info
"""
web.get('/api'                  , info_handler.info('api')),
web.get('/api/'                 , info_handler.info('api')),
web.get('/api/info'             , info_handler.info('api/info')),
web.get('/api/service-info'     , info_handler.ga4gh('api/service-info')),
web.get('/api/map'              , info_handler.map('api/map')),
web.get('/api/configuration'    , info_handler.config_txt('api/configuration')),
web.get('/api/entry_types'      , info_handler.entry_types('api/entry_types')),
web.get('/api/filtering_terms'  , info_handler.filtering_terms('api/filtering_terms')),
"""

