
import server.framework.endpoints.handlers as handler

#from server.model.parameters import DatasetsParameters, CohortParameters
from server.framework.response import *
from server.gpap import *
from server.gpap.map_entities import *
import server.framework.endpoints.static_handlers as static_handlers

# MAPINT ROUTES WITH STATIC GET INFO
############################################################################################################

api_entry_types    = static_handlers.static_entry_types()
api_map            = static_handlers.static_map()
api_config         = static_handlers.static_config_txt()
api_info           = static_handlers.static_info()
api_filtering_term = static_handlers.static_filtering_terms()
api_service_info   = static_handlers.static_ga4gh()


# MAPINT ROUTES WITH MODEL
############################################################################################################

#individuals_proxy = IndividualsParameters()

"""
# Not implemented endpoints

individuals_by_biosample  = handler.not_implemented_handler('individuals')
#biosamples_by_biosample   = handler.not_implemented_handler('biosamples')
gvariants_by_biosample    =handler. not_implemented_handler('gvariants')

individuals_by_variant    = handler.not_implemented_handler('individuals')
biosamples_by_variant     = handler.not_implemented_handler('biosamples')
gvariants_by_variant      = handler.not_implemented_handler('gvariants')

#individuals_by_individual = handler.not_implemented_handler('individuals')
#biosamples_by_individual  = handler.not_implemented_handler('biosamples')
gvariants_by_individual   = handler.not_implemented_handler('gvariants')

cohorts_by_cohort         = handler.not_implemented_handler('cohorts')

# Implemented endpoints
"""

# Test
query_test                = handler.test( 'test' )

#Handler to use based on token type
if config.fixed_token_use:
    handler_to_use = handler.handler_fixed_token
else:
    handler_to_use = handler.handler_jwt_token

# Individuals
query_individuals_by_individuals = handler_to_use( 'individuals', fetch_individuals_by_individual, individuals )

# Biosamples
query_biosamples_by_biosample = handler_to_use( 'biosamples', fetch_biosamples_by_biosample, experiments )


'''Beacon v1'''
# Variants
query_variants_by_variant = handler.handler_variants( 'variants', fetch_variants_by_variant, variants )


# Additional endpoints for the Beacon verifier to pass (not actually implemented)
query_runs_by_run = handler.handler_fixed_token( 'runs' , fetch_rest_by_type, lambda x, y: x )
query_analyses_by_analyses = handler.handler_fixed_token( 'analyses' , fetch_rest_by_type, lambda x, y: x )
query_cohorts_by_cohort = handler.handler_fixed_token( 'cohorts' , fetch_rest_by_type, lambda x, y: x )
query_datasets_by_dataset = handler.handler_fixed_token( 'datasets' , fetch_rest_by_type, lambda x, y: x )



"""
# Individuals
query_individuals_by_individual
query_individuals_by_individual
query_gvariants_by_individual
query_biosamples_by_individual






# individuals_by_biosample = generic_handler('individuals', BeaconEntity.BIOSAMPLE, individuals_proxy, fetch_individuals_by_biosample, build_biosample_or_individual_response)
biosamples_by_biosample = generic_handler('biosamples' , BeaconEntity.BIOSAMPLE, biosamples_proxy , fetch_biosamples_by_biosample, build_biosample_or_individual_response)
# gvariants_by_biosample = generic_handler('gvariants'  , BeaconEntity.BIOSAMPLE, gvariants_proxy  , fetch_variants_by_biosample, build_variant_response)

# individuals_by_variant = generic_handler('individuals', BeaconEntity.VARIANT, individuals_proxy, fetch_individuals_by_variant, build_biosample_or_individual_response)
# biosamples_by_variant = generic_handler('biosamples' , BeaconEntity.VARIANT, biosamples_proxy , fetch_biosamples_by_variant, build_biosample_or_individual_response)
# gvariants_by_variant = generic_handler('gvariants'  , BeaconEntity.VARIANT, gvariants_proxy  , fetch_variants_by_variant, build_variant_response)

individuals_by_individual = generic_handler('individuals', BeaconEntity.INDIVIDUAL, individuals_proxy, fetch_individuals_by_individual, build_biosample_or_individual_response)
biosamples_by_individual = generic_handler('biosamples' , BeaconEntity.INDIVIDUAL, biosamples_proxy , fetch_biosamples_by_individual, build_biosample_or_individual_response)
# gvariants_by_individual = generic_handler('gvariants'  , BeaconEntity.INDIVIDUAL, gvariants_proxy  , fetch_variants_by_individual, build_variant_response)

# cohorts_by_cohort = generic_handler('cohorts', BeaconEntity.COHORT, cohorts_proxy, fetch_cohorts_by_cohort, count_cohorts_by_cohort, build_cohort_response)
"""