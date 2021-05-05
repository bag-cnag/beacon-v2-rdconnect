import logging
import re
import json

from server.config import config

under_pat = re.compile(r'_([a-z])')

LOG = logging.getLogger(__name__)

def snake_case_to_camelCase(j):
    return j if j is None else json.loads(under_pat.sub(lambda x: x.group(1).upper(), j))

def beacon_info_v30(datasets, authorized_datasets=[]):
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
        'datasets': [beacon_dataset_info_v30(row, authorized_datasets) for row in datasets],
        'info': None,
    }


def beacon_dataset_info_v30(row, authorized_datasets=[]):
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


def beacon_variant_v30(row):
    return {
            'variantId': row['variant_id'],         # ¿?
            'assemblyId': row['assembly_id'],       #
            'refseqId': row['refseq_id'],           #
            'start': row['start'],                  #
            'end': row['end'],                      #
            'ref': row['reference'],                #
            'alt': row['alternate'],                #
            'variantType': row['variant_type'],     #
            'info': None,                           #
        }


def beacon_variant_annotation_v30(row):
    return {
            'variantId': row['variant_id'],
            'variantAlternativeId': [row['alternative_id']],
            'genomicHGVSId': row['genomic_hgvs_id'],
            'transcriptHGVSId': row['transcript_hgvs_ids'],
            'proteinHGVSId': row['protein_hgvs_ids'],
            'genomicRegion': row['genomic_regions'],
            'genomicFeatures': row['genomic_features_ontology'],
            'annotationToolVersion': 'SnpEffVersion=5.0d (build 2021-01-28 11:39)',
            'molecularEffect': row['molecular_effects'],
            #'molecularConsequence': row['molecular_consequence'],
            'aminoacidChange': row['aminoacid_changes'],
            'info': {
                'aaref': row['aaref'],
                #'aapos': row['aapos'],
                'aaalt': row['aaalt'],
                'aa_pos_aa_length': row['functional_classes'],
                'rank': row['exon_ranks'],
                'annotation_impact': row['genomic_regions']
            }
        }

def beacon_biosample_v30(row):
    return {
        'biosampleId': row['biosample_stable_id'],                      # EXPERIMENT ID
        'subjectId': row['individual_stable_id'],                       # PHENOSTORE ID
        'description': row['description'],                              # ''
        'biosampleStatus': row['biosample_status_ontology'],            #
        'collectionDate':  str(row['collection_date']) if row['collection_date'] else None, # NONE
        'subjectAgeAtCollection': row['individual_age_at_collection'],  # ''
        'sampleOriginDescriptors': row['sample_origins_ontology'],      # ''
        'obtentionProcedure': row['obtention_procedure_ontology'],      # ''
        'cancerFeatures': {                                             # {}
            'tumorProgression': row['tumor_progression_ontology'],
            'tumorGrade': row['tumor_grade_ontology'],
        },
        'handovers': row['handovers'],                                  # []
        'info': {                                                       # FREE FIELD - NOW EMPTY
            'alternativeIds': row['alternative_ids'],                   # DNA/RNA
            'studyId': row['study_id'],                                 # WHS/WES
            'bioprojectId': row['bioproject_id'],                       # Kit
            'files': row['files'],                                      # Tissue
        }
    }

def beacon_individual_v30(row):                                    # PHENOSTORE PERMISION LAYER
    return {
        'individualId': row['id'],                                 # PHENOSTORE ID
        'taxonId': None,                                           # NONE
        'sex': row['sex'],                                         #
        'ethnicity': None,                                         # NONE
        'geographicOrigin': None,                                  # NONE
        'phenotypicFeatures': row['features'],                     # FEATURES
        'diseases': row['diagnosis'],                              # DIAGNOSIS
        'pedigrees': [],                                           # ?
        'handovers': [],                                           # NONE/[]
        'treatments': [],                                          # NONE/[]
        'interventions': [],                                       # NONE/[]
        'measures': snake_case_to_camelCase(row['measurements']),  #
        'exposures': [],                                           # NONE/[]
        'info': {                                                  # FREE FIELD
            'family': row['famid'],                                # PS FAMILY ID
            'index': row['index'],                                 # RD-CONNECT INDEX CASE
            'solved': row['solved'],                               # RD-CONNECT SOLVED STATUS
        },
    }


def beacon_cohort_v31(row):
    return {
        'cohortId': row['id'],
        'cohortName': row['cohort_name'],
        'cohortType': row['cohort_type'],
        'cohortDesign': row['cohort_design'],
        'cohortInclusionCriteria': row['cohort_inclusion_criteria'],
        'cohortExclusionCriteria': row['cohort_exclusion_criteria'],
        'cohortLicense': row['cohort_license'],
        'cohortContact': row['cohort_contact'],
        'cohortRights': row['cohort_rights'],
        'cohortSize': row['cohort_size'],
        'cohortDataTypes': row['cohort_data_types'],
        'collectionEvents': snake_case_to_camelCase(row['collection_events']),
    }