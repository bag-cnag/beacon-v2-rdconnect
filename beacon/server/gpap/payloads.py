#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.framework.exceptions import BeaconBadRequest
from server.config import config
import re
import json
from elasticsearch import Elasticsearch
from server.utils.request_origin import check_request_origin
import requests

# List of valid filtering keys per GPAP's endpoint
# _valid_individuals = [ 'id', 'family_id', 'index', 'solved', 'sex', 'affectedStatus', 'lifeStatus' ]
# _valid_biosamples  = [ 'RD_Connect_ID_Experiment', 'EGA_ID', 'Participant_ID', 'Owner', 'in_platform', 'POSTEMBARGO', 'experiment_type', 'kit', 'tissue', 'library_source', 'library_selection', 'library_strategy', 'library_contruction_protocol', 'erns' ]

def set_hpo(item, flt_schema):
    """ Set HPO filter """
    hpo = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['phenotype']

    #For v0.2
    if version == "v0.2":
        key = value = "id"

    if not isinstance(item["id"], list):
        if (key in item) and ((item[value].lower().startswith('hp')) or (item[value].lower().startswith('obo:hp'))):
            hpo_string = "HP:" + re.split('[_ :]', item[value])[-1]
            hpo = {'id': 'features', 'value': hpo_string}
    
    else:
        mult_values = []
        if key in item:
            for obj in item[key]:
                if ((obj.lower().startswith('hp')) or (obj.lower().startswith('obo:hp'))):
                    hpo_string = "HP:" + re.split('[_ :]', obj)[-1]
                    mult_values.append(hpo_string)

        if len(mult_values) > 0:
            req_origin = check_request_origin()

            #For EJP, if we have an array the logic is OR
            if (req_origin == 'ejp'):
                hpo = {'id': 'features', 'value': mult_values}
            
            #Otherwise, the logic is AND as in Beaconv2 spec
            else:
                hpo = []
                for i in mult_values:
                    hpo.append({'id': 'features', 'value': i})

    return hpo

def set_ordo(item, flt_schema):
    """ Set ORDO filter """
    ordo = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['diagnosis']

    #For v0.2
    if version == "v0.2":
        key = value = "id"
    
    if not isinstance(item["id"], list):
        if (key in item) and ((item[value].lower().startswith('orpha')) or (item[value].lower().startswith('ordo:orpha'))):
            ordo_string = "Orphanet:" + re.split('[_ :]', item[value])[-1]
            ordo = {'id': 'diagnosis', 'value': ordo_string}
    
    #If input is an array we are in v0.2
    else:        
        mult_values = []
        if key in item:
            for obj in item[key]:
                if ((obj.lower().startswith('orpha')) or (obj.lower().startswith('ordo:orpha'))):
                    ordo_string = "Orphanet:" + re.split('[_ :]', obj)[-1]
                    mult_values.append(ordo_string)
        
        if len(mult_values) > 0:
            req_origin = check_request_origin()

            #For EJP, if we have an array the logic is OR
            if (req_origin == 'ejp'):
                ordo = {'id': 'diagnosis', 'value': mult_values}
            
            #Otherwise, the logic is AND as in Beaconv2 spec
            else:
                ordo = []
                for i in mult_values:
                    ordo.append({'id': 'diagnosis', 'value': i})
    return ordo

def set_omim(item, flt_schema):
    """ Set OMIM filter """
    omim = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['diagnosis']

    if version == "v0.2":
        key = value = "id"
    
    if not isinstance(item["id"], list):
        if (key in item) and (item[value].lower().startswith('omim')):
            omim_string = "OMIM:" + re.split('[_ :]', item[value])[-1]
            omim = {'id': 'disorders', 'value': omim_string}
    else:
        mult_values = []
        if key in item:
            for obj in item[key]:
                if ((obj.lower().startswith('omim'))):
                    omim_string = "OMIM:" + re.split('[_ :]', obj)[-1]
                    mult_values.append(omim_string)

        if len(mult_values) > 0:
            req_origin = check_request_origin()

            #For EJP, if we have an array the logic is OR
            if (req_origin == 'ejp'):
                omim = {'id': 'disorders', 'value': mult_values}
            
            #Otherwise, the logic is AND as in Beaconv2 spec
            else:
                omim = []
                for i in mult_values:
                    omim.append({'id': 'disorders', 'value': i})
    
    return omim

def set_gene(item, flt_schema):
    """ Set gene filter """
    gene = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['gene']
    
    if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split(":")[-1])):
        if not isinstance(item["value"], list):
            gene = {'id': 'genes', 'value': item[value]}
        else:
            mult_values = []
            for obj in item["value"]:
                mult_values.append(obj)
            if len(mult_values) > 0:
                gene = {'id': 'genes', 'value': mult_values}
    
    return gene

def set_sex(item, flt_schema):
    """ Set sex filter """
    sex = {}
    key = flt_schema["key"]
    value = flt_schema["value"]
    version = flt_schema["version"]
    ontology_id = config.filters_in['ontologies_' + version]['sex']
    
    req_origin = check_request_origin()

    #For EJP sex is alphanumeric
    if (req_origin == 'ejp'):

        if (key in item) and ((item[key] == ontology_id) or (item[key] == ontology_id.split("obo:")[1])):

            if not isinstance(item["value"], list):
                sex = map_sex(item["value"])
            else:
                mult_values = []
                for obj in item["value"]:
                    sex = map_sex(obj)
                    mult_values.append(sex["value"])
                if len(mult_values) > 0:
                        sex = {'id': 'sex', 'value': mult_values}

    # For generic Beacon it is an ontology
    else:
        if (item[key] in config.filters_in['sex']):
            sex = map_sex(item["id"])

    return sex



def set_library_strategy(item):
    """ Set Library strategy (WXS or WGS)"""
    library_strategy = {}
    if item["id"] == 'NCIT_C153598' or item["id"] == 'NCIT:C153598':
        if item["value"] == 'NCIT_C101294' or item["value"] == 'NCIT:C101294':
            library_strategy = { 'id': 'library_strategy', 'value': [ 'WGS' ] }
        elif item["value"] == 'NCIT_C101295' or item["value"] == 'NCIT:C101295':
            library_strategy = { 'id': 'library_strategy', 'value': [ 'WXS' ] }
        else:
            library_strategy = { 'id': 'library_strategy', 'value': [ 'no_value' ] }
    
    return library_strategy


def set_ern(item):
    """ Set ERN """
    ern = {}
    if item["id"] == 'ERN':
        if (item["value"] in config.filters_in[ 'erns' ]):
            ern = { 'id': 'erns', 'value': [ item["value"] ] } 
    
    return ern

        
def set_unsupported_filter(item, service):    
    obj = {}
    if service == "ps":
        if "value" not in item:
            obj = {"id": item["id"], "value": "no_value"}
        else:
            obj = item
    
    # In case of DM set to arbitrary filter which is accepted from the API
    #else:
    #    obj = {"id": "subproject", "value": ["no_value"]}

    return obj


def map_sex(item):
    """ Sex mapper """
    sex = {}

    if item == 'NCIT_C16576' or item == 'obo:NCIT_C16576' or item == 'NCIT:C16576' or item == 'ncit:C16576': # female
        sex = {'id': 'sex', 'value': 'F'}
    elif item == 'NCIT_C20197' or item == 'obo:NCIT_C20197' or item == 'NCIT:C20197' or item == 'ncit:C20197': # male
        sex = {'id': 'sex', 'value': 'M'}
    elif item == 'NCIT_C124294' or item == 'obo:NCIT_C124294' or item == 'NCIT:C124294' or item == 'ncit:C124294': # unknown
        sex = {'id': 'sex', 'value': 'U'}
    elif item == 'NCIT_C17998' or item == 'obo:NCIT_C17998' or item == 'NCIT:C17998' or item == 'ncit:C17998' : # unknown
        sex = {'id': 'sex', 'value': 'U'}
    else:
        sex = {'id': 'sex', 'value': 'None'}
    
    return sex


def requested_api_version(qparams):
    """ Check api version from request and return corresponding body schema """
    api_version = qparams["meta"]["apiVersion"]

    if api_version == "v0.1":
        ontology_filter_schema = {"version":"v0.1","key":"type", "value":"id"}
    else:
        ontology_filter_schema = {"version":"v0.2", "key":"id", "value":"value"}
    
    return ontology_filter_schema


# Function to translate from RequestParameters to PhenoStore filtering
def ps_to_gpap( qparams, psid = None ):
    fltrs = []
    
    #Filters schema keys depending on api version (0.1 & 0.2)
    ontology_filter_schema = requested_api_version(qparams)
    
    #Most probably no case of asking with specific id
    #if psid:
    #    fltrs.append( { 'id': 'phenotips_id', 'value': psid } )
    
    #Filters
    if len( qparams[ 'query' ][ 'filters' ] ) > 0:
        for item in qparams[ 'query' ][ 'filters' ]:
            #Set filters
            sex_fltr = set_sex(item, ontology_filter_schema)
            hpo_fltr = set_hpo(item, ontology_filter_schema)
            ordo_fltr = set_ordo(item, ontology_filter_schema)
            omim_fltr = set_omim(item, ontology_filter_schema)
            gene_fltr = set_gene(item, ontology_filter_schema)

            if hpo_fltr:  
                if isinstance(hpo_fltr, list) and hpo_fltr[0]["id"] == "features":
                  for i in hpo_fltr:
                    fltrs.append(i)
                else:
                    fltrs.append(hpo_fltr)
            
            if ordo_fltr:  
                if isinstance(ordo_fltr, list) and ordo_fltr[0]["id"] == "diagnosis":
                  for i in ordo_fltr:
                    fltrs.append(i)
                else:
                    fltrs.append(ordo_fltr)
            
            if omim_fltr:
                if isinstance(omim_fltr, list) and omim_fltr[0]["id"] == "disorders":
                  for i in omim_fltr:
                    fltrs.append(i)
                else:
                    fltrs.append(omim_fltr)
                            
            #if hpo_fltr:  fltrs.append(hpo_fltr)
            #if ordo_fltr: fltrs.append(ordo_fltr)
            #if omim_fltr: fltrs.append(omim_fltr)

            if sex_fltr:  fltrs.append(sex_fltr)
            if gene_fltr: fltrs.append(gene_fltr)
            
            #For generic Beaconv2 spec include every filter in the query (in EJP unsupported filters are ignored)
            req_origin = check_request_origin()
            if (req_origin != "ejp") and (not sex_fltr and not hpo_fltr and not ordo_fltr and not omim_fltr and not gene_fltr) and ("id" in item and item["id"] != ""):
                fltrs.append(set_unsupported_filter(item, "ps"))

        #If nothing from the above applies
        if len(fltrs) == 0:
            fltrs.append ({ 'id': '_no_filter', 'value': '_no_filter' } )
    
    #No filters
    else:
        fltrs = []

    return fltrs

# Function to translate from RequestParameters to DataManagement filtering
def dm_to_gpap( qparams ):
    fltrs = []
    if qparams[ 'targetIdReq' ] and qparams[ 'targetIdReq' ].startswith('B-'):
        #Remove the prefix "B-" added to the participant
        
        print("hello!",qparams[ 'targetIdReq' ]  )
        if qparams[ 'targetIdReq' ].startswith( 'P' ):
            fltrs.append( { 'id': 'Participant_ID', 'value': qparams[ 'targetIdReq' ] } )
        elif qparams[ 'targetIdReq' ].startswith('E') or qparams[ 'targetIdReq' ].startswith( 'C' ): # E real experiments, C fake/demo ones
            fltrs.append( { 'id': 'RD_Connect_ID_Experiment', 'value': qparams[ 'targetIdReq' ] } )
        else:
            raise BeaconBadRequest( 'Invalid provided identifier "{}". It should start by "B-P" or "B-E".'.format( qparams[ 'targetIdReq' ] ) )
    if len( qparams[ 'query' ][ 'filters' ] ) > 0:
        for item in qparams[ 'query' ][ 'filters' ]:
            #Set filters
            ern_fltr = set_ern(item)
            library_strategy_fltr = set_library_strategy(item)

            if ern_fltr:  fltrs.append(ern_fltr)
            if library_strategy_fltr: fltrs.append(library_strategy_fltr)

            #For generic Beaconv2 spec include every filter in the query (in EJP unsupported filters are ignored)
            req_origin = check_request_origin()
            if (req_origin != "ejp") and (not ern_fltr and not library_strategy_fltr) and ("id" in item and item["id"] != ""):
                unsupported_filter = set_unsupported_filter(item, "dm")
                if unsupported_filter:
                    fltrs.append(unsupported_filter)
            
    return fltrs

# For individuals, filtering criteria is expected a dictionary
# having keys matching PhenoStore. This matching is done in
# server/validation.py IndividualParameters
def phenostore_playload( qparams, psid ):
    """
    PhenoStore filtering ciretia to be included as playload in each query.
    """
    return {
        #'page'    : 1,
        #In case of returning records need to have a pageSize (to check)
        #'pageSize': 50,
        'page': 1 + qparams[ 'query' ][ 'pagination' ][ 'skip' ],
        'pageSize': qparams[ 'query' ][ 'pagination' ][ 'limit' ],
         #Configure fields to return in the full response
        'fields': [
            'sex', 
            'features', 
            'diagnosis', 
            'disorders',
            'genes',
            'id',
            'birth',
            'index',
            'affectedStatus',
            'solved',
            'otheraffected',
            'owner'
        ],
        'sorted'  : [],
        'filtered': ps_to_gpap( qparams, psid ),
       
    }


def datamanagement_playload( qparams, groups ):
    """
    DataManagement filtering ciretia to be included as playload in each query.
    """

    payload = {
        # In the case of 0 results and with page set to 2, DM API returns a 500. Setting to 1 solves it.
        #'page':     1,
        #'pageSize': 100000,
        'page':     1 + qparams[ 'query' ][ 'pagination' ][ 'skip' ],
        'pageSize': qparams[ 'query' ][ 'pagination' ][ 'limit' ],
        'fields': [
            'RD_Connect_ID_Experiment',
            'Participant_ID',
            'project',
            'subproject',
            #'experiment_type',
            'kit',
            'tissue',
            'library_source',
            'library_strategy',
            'LOADDATE'
        ],
        'sorted':   [],
        'filtered': dm_to_gpap( qparams )
    }


    return payload




#Beacon v1 for variants
def elastic_playload(chrom, start):
    
    es_body = {
          "query": {
            "bool": {
              "must": [
                 {"term" : { "chrom" : chrom }
          },
          {"term" : { "pos" : start }
          }
          ]
        }
      }
    }


    return es_body


def query_elastic(chrom, start):

    elastic_user  = config.elastic_user
    elastic_passwd= config.elastic_password
    elastic_host  = config.elastic_host
    elastic_index = config.elastic_index
    es = Elasticsearch(elastic_host, http_auth=(elastic_user,elastic_passwd))
    res = es.search(index=elastic_index, body=elastic_playload(chrom,start))

    return res


def elastic_resp_handling(qparams, variants_dict):

    #Get from variants dicts
    chrom = variants_dict["chrom"]
    start = variants_dict["start"]
    ref = variants_dict["ref"]
    alt = variants_dict["alt"]

    #Query elastic6
    res = query_elastic(chrom,start)

    found=0
    if res['hits']['total']['value'] >=1:
        for result in res['hits']['hits']:
            if result['_source']['alt']==alt and result["_source"]['ref']==ref:
                found+=1
    
  
    #return data
    return found

'''With scala API'''
def query_genomics_variants(access_token, chrom, start, experiments_to_query):

    samples_germline = []
    for i in experiments_to_query:
        sample = {"sample_id":i,"gq":30,"gt":["0/1","1/1"],"dp":10,"ad_low":0.2,"ad_high":0.8,"index":1}
        samples_germline.append(sample)
    
    url = config.gpap_base_url + config.genomic_variants

    headers = {'Content-Type': 'application/json', 'Accept':"*", 'X-TOKEN-AUTH': access_token}
    
    #If no parameters are provided, query for all samples without chrom details (query fails)
    if chrom == '25':
        es_body = {"size":3000,"from":0,"fromCNV":0,"chrom":[],"indel":False,"svn":False,"genotypefeatures":{"other":False,"coding":False,"RNA":False},"variantclasses":{"high":False,"low":False,"moderate":False,"modifier":False},"variantconsequences":{"transcript_ablation":False,"splice_acceptor_variant":False,"splice_donor_variant":False,"stop_gained":False,"frameshift_variant":False,"stop_lost":False,"start_lost":False,"transcript_amplification":False,"feature_elongation":False,"feature_truncation":False,"inframe_insertion":False,"inframe_deletion":False,"missense_variant":False,"protein_altering_variant":False,"splice_donor_5th_base_variant":False,"splice_region_variant":False,"splice_donor_region_variant":False,"splice_polypyrimidine_tract_variant":False,"incomplete_terminal_codon_variant":False,"start_retained_variant":False,"stop_retained_variant":False,"synonymous_variant":False,"coding_sequence_variant":False,"mature_miRNA_variant":False,"prime_5_UTR_variant":False,"prime_3_UTR_variant":False,"non_coding_transcript_exon_variant":False,"intron_variant":False,"NMD_transcript_variant":False,"non_coding_transcript_variant":False,"coding_transcript_variant":False,"upstream_gene_variant":False,"downstream_gene_variant":False,"TFBS_ablation":False,"TFBS_amplification":False,"TF_binding_site_variant":False,"regulatory_region_ablation":False,"regulatory_region_amplification":False,"regulatory_region_variant":False,"intergenic_variant":False,"sequence_variant":False},"mutationtaster":{"A":False,"D":False,"P":False},"intervarclasses":{"P":False,"LP":False,"B":False,"LB":False,"VUS":False},"clinvarclasses":{"P":False,"L":False,"A":False,"U":False,"C":False,"D":False},"onco_filter":{"K":False,"P1":False,"P2":False,"PP":False},"onco_classifier":{"O":False,"LO":False,"VUS":False,"B":False,"LB":False},"polyphen2hvarpred":{"D":False,"P":False,"B":False},"population":{},"siftpred":{"D":False,"T":False},"gnomad_filter":{"pass":False,"nonpass":False},"gene":[],"samples_germline":samples_germline,"samples_somatic":[],"compound_in":False,"cosmic":False,"qc_filter":{"dp_tumor":10,"dp_control":10,"dp_ref_tumor":10,"dp_alt_tumor":3,"vaf_tumor_low":0.05,"vaf_tumor_high":0.8},"nprograms":0,"programs_filter":{"mutect":False,"strelka":False,"caveman":False,"muse":False,"lancet":False},"cnv_germline":True,"cnv_somatic":False}
    else:
        es_body = {"size":-1,"from":0,"fromCNV":0,"chrom":[{"chrom": chrom, "pos": start, "end_pos": start}],"indel":False,"svn":False,"genotypefeatures":{"other":False,"coding":False,"RNA":False},"variantclasses":{"high":False,"low":False,"moderate":False,"modifier":False},"variantconsequences":{"transcript_ablation":False,"splice_acceptor_variant":False,"splice_donor_variant":False,"stop_gained":False,"frameshift_variant":False,"stop_lost":False,"start_lost":False,"transcript_amplification":False,"feature_elongation":False,"feature_truncation":False,"inframe_insertion":False,"inframe_deletion":False,"missense_variant":False,"protein_altering_variant":False,"splice_donor_5th_base_variant":False,"splice_region_variant":False,"splice_donor_region_variant":False,"splice_polypyrimidine_tract_variant":False,"incomplete_terminal_codon_variant":False,"start_retained_variant":False,"stop_retained_variant":False,"synonymous_variant":False,"coding_sequence_variant":False,"mature_miRNA_variant":False,"prime_5_UTR_variant":False,"prime_3_UTR_variant":False,"non_coding_transcript_exon_variant":False,"intron_variant":False,"NMD_transcript_variant":False,"non_coding_transcript_variant":False,"coding_transcript_variant":False,"upstream_gene_variant":False,"downstream_gene_variant":False,"TFBS_ablation":False,"TFBS_amplification":False,"TF_binding_site_variant":False,"regulatory_region_ablation":False,"regulatory_region_amplification":False,"regulatory_region_variant":False,"intergenic_variant":False,"sequence_variant":False},"mutationtaster":{"A":False,"D":False,"P":False},"intervarclasses":{"P":False,"LP":False,"B":False,"LB":False,"VUS":False},"clinvarclasses":{"P":False,"L":False,"A":False,"U":False,"C":False,"D":False},"onco_filter":{"K":False,"P1":False,"P2":False,"PP":False},"onco_classifier":{"O":False,"LO":False,"VUS":False,"B":False,"LB":False},"polyphen2hvarpred":{"D":False,"P":False,"B":False},"population":{},"siftpred":{"D":False,"T":False},"gnomad_filter":{"pass":False,"nonpass":False},"gene":[],"samples_germline":samples_germline,"samples_somatic":[],"compound_in":False,"cosmic":False,"qc_filter":{"dp_tumor":10,"dp_control":10,"dp_ref_tumor":10,"dp_alt_tumor":3,"vaf_tumor_low":0.05,"vaf_tumor_high":0.8},"nprograms":0,"programs_filter":{"mutect":False,"strelka":False,"caveman":False,"muse":False,"lancet":False},"cnv_germline":True,"cnv_somatic":False}


    try:
        res = requests.post(url, json=es_body, headers=headers)  
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying genomics variants: {e}") 
        return None  




def genomics_variants_resp_handling(qparams, access_token, variants_dict, experiments_to_query, roles):

    #Get from variants dicts
    chrom = variants_dict["chrom"]
    start = variants_dict["start"]
    ref = variants_dict["ref"]
    alt = variants_dict["alt"]

    #Query elastic
    res = query_genomics_variants(access_token, chrom, start, experiments_to_query)

    found = 0

    #print (res.text[0])
    found_zygosity = [{"Homozygous":{"total":0}}, {"Heterozygous":{"total":0}}]


    if res and res['snv']['hits']['total']['value'] >=1:
        for result in res['snv']['hits']['hits']:
            if result['_source']['alt']==alt and result["_source"]['ref']==ref:

                print (result)

                #Count the number of samples
                if "fields" in result and "samples_germline":
                    found = len(result["fields"]["samples_germline"])
                    
                    heterozygous = homozygous = 0
                    for sample in result["fields"]["samples_germline"]:
                        if "gt" in sample and sample["gt"] == "0/1":
                            heterozygous += 1
                        elif "gt" in sample and sample["gt"] == "1/1":
                            homozygous +=1
                        else:
                            pass
                    
                    if "full_access" in roles:
                        rows = []
                        samples = result["fields"]["samples_germline"]
                        effs = result["fields"].get("effs", [])
                        
                        # Group effects by transcript_id and build transcript information array
                        transcripts_info = []
                        if effs:
                            for eff in effs:
                                transcript_data = {
                                    "transcript_id": eff.get("transcript_id", ""),
                                    "codon_change": eff.get("codon_change", ""),
                                    "amino_acid_change": eff.get("amino_acid_change", ""),
                                    "gene_name": eff.get("gene_name", ""),
                                    #"functional_class": eff.get("functional_class", ""),
                                    #"amino_acid_length": eff.get("amino_acid_length", ""),
                                    #"effect_impact": eff.get("effect_impact", ""),
                                    #"effect": eff.get("effect", "")
                                }
                                transcripts_info.append(transcript_data)
                        
                        # Add one row per sample with the same transcripts information
                        for sample in samples:
                            row = sample.copy()
                            row["transcripts"] = transcripts_info
                            rows.append(row)
                    else:
                        rows = []
                    
                    print (rows)

                    found_zygosity = [{"Homozygous":{"total":homozygous, "rows":rows}}, {"Heterozygous":{"total":heterozygous, "rows":rows}}]
                #else:
                #    found+=1
    
    return (found_zygosity)
    #return found