from datetime import datetime
from datetime import date
from server.config import config

def calculate_age(born):
    if born is None:
        return None
    else:
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def ga4gh_service_info_v10(row, authorized_datasets=None):
    return {
        'id': config.beacon_id,
        'name': config.beacon_name,
        'type': {
            'group': config.ga4gh_service_type_group,
            'artifact': config.ga4gh_service_type_artifact,
            'version': config.ga4gh_service_type_version
        },
        'description': config.description,
        'organization': {
            'name': config.org_name,
            'url': config.org_welcome_url
        },
        'contactUrl': config.org_contact_url,
        'documentationUrl': config.documentation_url,
        'createDateTime': config.create_datetime,
        'updateDateTime': config.update_datetime,
        'environment': config.environment,
        'version': config.version,
        'url': config.service_url,
    }


def ga4gh_phenopackets_biosamples_v10(row):
    abnormal_sample_ontology = 'EFO:0009655'
    biosample_id = row['biosample_stable_id']
    return {
        'id': conf.beacon_id + '_' + biosample_id, # required
        # 'subject': None,
        # 'phenotypic_features': None,
        'biosamples': [{
            'id': biosample_id,
            'individual_id': row['individual_stable_id'],
            'description': row['description'],
            'sampled_tissue': row['sample_origins_ontology'], #, schema_name),
            'phenotypic_features': None,
            'taxonomy': None,
            'individual_age_at_collection': {
                'age': row['individual_age_at_collection'],
            },
            'histological_diagnosis': None,
            'tumor_progression': {
                    'id': row['tumor_progression_ontology'],
                    'label': row['tumor_progression_ontology_label'],
                },
            'tumor_grade': {
                    'id': row['tumor_grade_ontology'],
                    'label': row['tumor_grade_ontology_label'],
                },
            'diagnostic_markers': None,
            'procedure': {
                'code': {
                    'id': row['obtention_procedure_ontology'],
                    'label': row['obtention_procedure_ontology_label'],
                },
                'body_site': None,
            },
            'hts_files': row['files'],
            'variants': None,
            'is_control_sample': True if row['biosample_status_ontology'] == abnormal_sample_ontology else False,
        }],
        # 'genes': None,
        # 'variants': None,
        # 'diseases': None,
        # 'hts_files': None,
        'meta_data': build_phenopackets_meta_data_block(row['ontologies_used']), # required
    }


def build_phenopackets_meta_data_block(ontologies_used):
    now = datetime.now()
    return {
        'created': now.strftime(conf.datetime_format),  # required
        'created_by': conf.beacon_name,  # required
        # 'submitted_by': None,
        'resources': ontologies_used,  # required
        # 'updates': None,
        # 'phenopacket_schema_version': None,
        # 'external_references': None,
    }


def ga4gh_phenopackets_individual_v10(row):
    individual_id = row['individual_stable_id']
    return {
        'id': conf.beacon_id + '_' + individual_id, # required
        'subject': {
            'id': individual_id, # required
            'alternate_ids': row['alternative_ids_phenopackets'],
            'date_of_birth': str(row["date_of_birth"]),
            'age': calculate_age(row["date_of_birth"]),
            'sex': row['sex'].upper() if row['sex'] else None,
            'karyotypic_sex': None,
            'taxonomy': {
                'id': row['taxon_id_ontology'],
                'label': row['taxon_id_ontology_label'],
            }
        },
        'phenotypic_features': row['phenotypic_features'],
        # 'biosamples': None,
        # 'genes': None,
        # 'variants': None,
        'diseases': row['diseases'],
        # 'hts_files': None,
        'meta_data': build_phenopackets_meta_data_block(row['ontologies_used']), # required
    }


def ga4gh_phenopackets_variant_v10(row):
    variant_id = row['variant_id']
    return {
        'id': conf.beacon_id + '_' + str(variant_id), # required
        # 'subject': None,
        # 'phenotypic_features': None,
        # 'biosamples': None,
        # 'genes': None,
        'variants': [{
            'vcfAllele': {
                'genome_assembly': row['assembly_id'],  # required
                'id': variant_id,
                'chr': row['chromosome'],  # required
                'pos': row['start'],  # required
                'ref': row['reference'],  # required
                'alt': row['alternate'],  # required
                'info': None,
            },
            'zygosity': None,
        }],
        # 'diseases': None,
        # 'hts_files': None,
        'meta_data': None, # required
    }


def ga4gh_phenopackets_variant_annotation_v10(row):
    transcripts_hgvs_ids = [{
        'hgvsAllele': {
            'id': None,
            'hgvs': hgvs_id
        },
        'zygosity': None,
    } for hgvs_id in row['transcript_hgvs_ids']]

    return {
        'id': None, # required
        # 'subject': None,
        # 'phenotypic_features': None,
        # 'biosamples': None,
        'genes': row['genomic_features_ontology'],
        'variants': transcripts_hgvs_ids,
        # 'diseases': None,
        # 'hts_files': None,
        'meta_data': build_phenopackets_meta_data_block(row['ontologies_used']), # required
    }


def ga4gh_vr_variant_v11(row):
    return {
        'Variation': {
            'id': row['variant_id'],
            'Allele': {
                'location': {
                    'interval': {
                        'end': row['end'],
                        'start': row['start']-1,
                        'type': 'SimpleInterval'
                    },
                    'sequence_id': 'refseq:' + row['refseq_id'],
                    'type': 'SequenceLocation'
                    },
                'state': {
                    'sequence': row['alternate'],
                    'type': 'SequenceState'
                },
                'type': 'Allele',
            },
        }
    }
