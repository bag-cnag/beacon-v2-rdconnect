#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import web

import server.framework.endpoints.map as map



#
# ROUTES
#############################################################################################################


routes = [
    # Test endpoints
    web.get(  '/api/test'                                      , map.query_test ),
    web.post( '/api/test'                                     , map.query_test ),
    
    # Info
    
    web.get(  '/api'                  , map.api_info ),
    web.get(  '/api/'                 , map.api_info ),
    web.get(  '/api/info'             , map.api_info ),
    web.get(  '/api/service-info'     , map.api_service_info ),
    web.get(  '/api/map'              , map.api_map ),
    web.get(  '/api/configuration'    , map.api_config ),
    web.get(  '/api/entry_types'      , map.api_entry_types ),
    web.get(  '/api/filtering_terms'  , map.api_filtering_term ),
    

    # Datasets
    web.post( '/api/datasets'                                 , map.query_datasets_by_dataset ),
    #web.post( '/api/datasets/{target_id_req}'                 , map.query_datasets_by_dataset ),
    
    # Individuals
    web.post( '/api/individuals'                              , map.query_individuals_by_individuals ),
    web.post( '/api/individuals/{target_id_req}'              , map.query_individuals_by_individuals ),
    
    # Biosamples
    web.post( '/api/biosamples'                               , map.query_biosamples_by_biosample ),
    web.post( '/api/biosamples/{target_id_req}'               , map.query_biosamples_by_biosample ),

    # Cohorts
    #web.post( '/api/cohorts'                                  , map.query_cohorts_by_cohort ),
    #web.post( '/api/cohorts/{target_id_req}'                  , map.query_cohorts_by_cohort ),


    # Beacon v1 for variants
    web.get( '/api/g_variants'                                  , map.query_variants_by_variant ),


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



