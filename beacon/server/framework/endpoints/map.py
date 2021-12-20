
import server.framework.endpoints.handlers as handler

#from server.model.parameters import DatasetsParameters, CohortParameters
from server.framework.response import *
from server.gpap import *
from server.gpap.map_entinies import *


# MAPINT ROUTES WITH MODEL
############################################################################################################

#_datasets_proxy    = None #DatasetsParameters()
#_cohorts_proxy     = None #CohortParameters()

#biosamples_proxy  = BiosamplesParameters()
#gvariants_proxy   = GVariantsParameters()
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

# Datasets
query_datasets_by_dataset = handler.generic( 'datasets' , fetch_datsets_by_dataset, lambda x, y: x )

# Individuals
query_individuals_by_individuals = handler.generic( 'individuals', fetch_individuals_by_individual, individuals )

# Biosamples
query_biosamples_by_biosample = handler.generic( 'biosamples', fetch_biosamples_by_biosample, experiments )

# Cohorts
#query_cohorts_by_cohort   = handler.not_implemented('cohorts')


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