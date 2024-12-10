#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import server.model.schemas.default as _default

supported_schemas = {
    'beacon-info-v2.0.0-draft.4'               : _default.beacon_info,
    'beacon-dataset-v2.0.0-draft.4'            : _default.beacon_dataset_info,
    #'beacon-variant-v2.0.0-draft.4'            : _default.beacon_variant,
    #'beacon-variant-annotation-v2.0.0-draft.4' : _default.beacon_variant_annotation,
    'beacon-biosample-v2.0.0-draft.4'          : _default.beacon_biosample,
    'beacon-individual-v2.0.0-draft.4'         : _default.beacon_individual,
    #'beacon-cohort-v2.0.0-draft.4'             : _default.beacon_cohort,
}

supported_schemas_by_entity = {
    'info'        : 'beacon-info-v2.0.0',
    'datasets'    : 'beacon-dataset-v2.0.0',
    'biosamples'  : 'beacon-biosample-v2.0.0',
    'individuals' : 'beacon-individual-v2.0.0',
    'cohorts'     : 'beacon-cohort-v2.0.0',
    'analyses'    : 'beacon-analyses-v2.0.0',
    'runs'        : 'beacon-run-v2.0.0',
    'variants'    : 'beacon-variant-v2.0.0',
    'genomicVariant': 'ga4gh-beacon-variant-v2.0.0'


}
