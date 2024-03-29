#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import re
import json

from server.config import config


## UTILS
##############################################################################

under_pat = re.compile(r'_([a-z])')

def snake_case_to_camelCase(j):
    return j if j is None else json.loads(under_pat.sub(lambda x: x.group(1).upper(), j))

def get_val(dd, k, rst = [], conv = lambda x: x):
    if k in dd.keys():
        return conv(dd[k])
    else:
        return rst

## SHEMAS
##############################################################################

def beacon_info(datasets, authorized_datasets=[]):
    return {
        'id': config.beacon_id,
        'name': config.beacon_name,
        'apiVersion': config.api_version,
        'environment': config.environment,
        'organization': {
            'id': config.org_id,
            'name': config.org_name,
            'description': config.org_description,
            'address': config.org_adress,
            'welcomeUrl': config.org_welcome_url,
            'contactUrl': config.org_contact_url,
            'logoUrl': config.org_logo_url,
            'info': config.org_info,
        },
        'description': config.description,
        'version': config.version,
        'welcomeUrl': config.welcome_url,
        'alternativeUrl': config.alternative_url,
        'createDateTime': config.create_datetime,
        'updateDateTime': config.update_datetime,
        'serviceType': config.service_type,
        'serviceUrl': config.service_url,
        'entryPoint': config.entry_point,
        'open': config.is_open,
        'datasets': [beacon_dataset_info(row, authorized_datasets) for row in datasets],
        'info': None,
    }


def beacon_dataset_info(row, authorized_datasets=[]):
    dataset_id = row['stable_id']
    is_authorized = dataset_id in authorized_datasets

    return {
        'id': dataset_id,
        'name': row['name'],
        'description': row['description'],
        'assemblyId': row['reference_genome'],
        'createDateTime': row['created_at'].strftime(config.datetime_format) if row['created_at'] else None,
        'updateDateTime': row['updated_at'].strftime(config.datetime_format) if row['updated_at'] else None,
        'dataUseConditions': None,
        'version': None,
        'variantCount': row['variant_count'],
        'callCount': row['call_count'],
        'sampleCount': row['sample_count'],
        'externalURL': None,
        'handovers': row['handovers'],
        'info': {
            'accessType': row['access_type'],
            'authorized': True if row['access_type'] == 'PUBLIC' else is_authorized,
            'datasetSource': row['dataset_source'],
            'datasetType': row['dataset_type']
        }
    }


# def beacon_variant(row):
#     return {
#             'variantId': row['variant_id'],         # ¿?
#             'assemblyId': row['assembly_id'],       #
#             'refseqId': row['refseq_id'],           #
#             'start': row['start'],                  #
#             'end': row['end'],                      #
#             'ref': row['reference'],                #
#             'alt': row['alternate'],                #
#             'variantType': row['variant_type'],     #
#             'info': None,                           #
#         }


# def beacon_variant_annotation(row):
#     return {
#             'variantId': row['variant_id'],
#             'variantAlternativeId': [row['alternative_id']],
#             'genomicHGVSId': row['genomic_hgvs_id'],
#             'transcriptHGVSId': row['transcript_hgvs_ids'],
#             'proteinHGVSId': row['protein_hgvs_ids'],
#             'genomicRegion': row['genomic_regions'],
#             'genomicFeatures': row['genomic_features_ontology'],
#             'annotationToolVersion': 'SnpEffVersion=5.0d (build 2021-01-28 11:39)',
#             'molecularEffect': row['molecular_effects'],
#             #'molecularConsequence': row['molecular_consequence'],
#             'aminoacidChange': row['aminoacid_changes'],
#             'info': {
#                 'aaref': row['aaref'],
#                 #'aapos': row['aapos'],
#                 'aaalt': row['aaalt'],
#                 'aa_pos_aa_length': row['functional_classes'],
#                 'rank': row['exon_ranks'],
#                 'annotation_impact': row['genomic_regions']
#             }
#         }

def beacon_biosample( experiments ):
    one = experiments[ 0 ]
    formated_experiments = []
    for row in experiments:
        formated_experiments.append( {
            'experimentId':                 row[ 'RD_Connect_ID_Experiment' ],     # EXPERIMENT ID
            'owner':                        row[ 'Owner'] ,                        # OWNER
            'tissue':                       row[ 'tissue' ],                       # TISSUE
            'ega_id':                       row[ 'EGA_ID' ],                       #
            'in_platform':                  row[ 'in_platform' ],                  # AVAILABLE FOR QUERY
            'experiment_type':              row[ 'experiment_type' ],              # WES/WGS
            'library_source':               row[ 'library_source' ],               # LIBRARY
            'library_selection':            row[ 'library_selection' ],            # LIBRARY
            'library_strategy':             row[ 'library_strategy' ],             # LIBRARY
            'library_contruction_protocol': row[ 'library_contruction_protocol' ], # LIBRARY
            'POSTEMBARGO':                  row[ 'POSTEMBARGO' ],                  # OTHERS THAN OWNER CAN QUERY
            'kit':                          row[ 'kit' ],                          # KIT
            'tumour_experiment_id':         row[ 'tumour_experiment_id' ],         # CANCER TUMORAL SAMPLES
            'design':                       row[ 'design_description' ],           # DESIGN
        } )
    return {
        'biosampleId':             'B-' + one[ 'Participant_ID' ],          # EXPERIMENT ID
        'subjectId':               one[ 'Participant_ID' ],                 # PHENOSTORE ID
        'description':             '',                                      # ''
        'biosampleStatus':         None,                                    # NONE
        'collectionDate':          None,                                    # NONE
        'subjectAgeAtCollection':  None,                                    # NONE
        'sampleOriginDescriptors': None,                                    # NONE
        'obtentionProcedure':      None,                                    # NONE
        'cancerFeatures': {                                                 # MOVED TO info
            'tumorProgression':    None,
            'tumorGrade':          None,
        },
        'handovers': [],                                                    # []
        'info': {                                                           # INFO FROM THE EXPERIMENTS
            'experiments_count': len( formated_experiments ),
            'experiments': formated_experiments
        }
    }

def beacon_individual( ind ):                                      # PHENOSTORE PERMISION LAYER
    return {
        'id':                 ind[ 'report_id'] ,                  # PHENOSTORE ID
        'taxonId':            None,                                # NONE
        'sex':                get_val(ind, 'sex', None, lambda x: 'Female' if x == 'F' else 'Male'), # Female/Male instead of F/M
        'ethnicity':          None,                                # NONE
        'geographicOrigin':   None,                                # NONE
        'phenotypicFeatures': get_val( ind, 'features' , [] ),     # FEATURES
        'diseases':           get_val( ind, 'diagnosis', [] ),     # DIAGNOSIS
        'pedigrees':          [],                                  # NOT MAPPED -- TODO NEEDS DISCUSION
        'handovers':          [],                                  # NONE/[]
        'treatments':         [],                                  # NONE/[]
        'interventions':      [],                                  # NONE/[]
        'measures':           get_val( ind, 'measurements', []),   #
        'exposures':          [],                                  # NONE/[]
        'info': {                                                  # FREE FIELD
            'family':         get_val( ind, 'famid' , None ),      # PS FAMILY ID
            'index':          get_val( ind, 'index' , None ),      # RD-CONNECT INDEX CASE
            'solved':         get_val( ind, 'solved', None ),      # RD-CONNECT SOLVED STATUS
            'iid':            get_val( ind, 'id'    , None )       # INTERNAL ID
        },
    }


# def beacon_cohort(row):
#     return {
#         'cohortId': row['id'],
#         'cohortName': row['cohort_name'],
#         'cohortType': row['cohort_type'],
#         'cohortDesign': row['cohort_design'],
#         'cohortInclusionCriteria': row['cohort_inclusion_criteria'],
#         'cohortExclusionCriteria': row['cohort_exclusion_criteria'],
#         'cohortLicense': row['cohort_license'],
#         'cohortContact': row['cohort_contact'],
#         'cohortRights': row['cohort_rights'],
#         'cohortSize': row['cohort_size'],
#         'cohortDataTypes': row['cohort_data_types'],
#         'collectionEvents': snake_case_to_camelCase(row['collection_events']),
#     }