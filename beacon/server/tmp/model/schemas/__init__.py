#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import server.model.schemas.default as _default

supported_schemas = {
    # default
    'beacon-info-v2.0.0-draft.4': _default.beacon_info,
    'beacon-dataset-v2.0.0-draft.4': _default.beacon_dataset_info,
    #'beacon-variant-v2.0.0-draft.4': _default.beacon_variant,
    #'beacon-variant-annotation-v2.0.0-draft.4': _default.beacon_variant_annotation,
    'beacon-biosample-v2.0.0-draft.4': _default.beacon_biosample,
    'beacon-individual-v2.0.0-draft.4': _default.beacon_individual,
    'beacon-cohort-v2.0.0-draft.4': _default.beacon_cohort,
    # alternative
    # 'ga4gh-service-info-v1.0': alternative.ga4gh_service_info_v10,
    # phenopackets format
    # 'ga4gh-phenopacket-variant-v1.0': alternative.ga4gh_phenopackets_variant_v10,
    # 'ga4gh-phenopacket-variant-annotation-v1.0': alternative.ga4gh_phenopackets_variant_annotation_v10,
    # 'ga4gh-phenopacket-individual-v1.0': alternative.ga4gh_phenopackets_individual_v10,
    # 'ga4gh-phenopacket-biosample-v1.0': alternative.ga4gh_phenopackets_biosamples_v10,
    # variant representation format
    # 'ga4gh-variant-representation-v1.1': alternative.ga4gh_vr_variant_v11,
}
