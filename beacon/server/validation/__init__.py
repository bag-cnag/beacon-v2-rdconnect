#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Beacon API endpoints.

The endpoints reflect the specification provided by:
- v1: https://github.com/ga4gh-beacon/specification/blob/develop/beacon.md
- v2: TBD

Endpoints:
* ``/api/``and ``/api/info`` -  Information about the datasets in the Beacon;
* ``/api/service-info`` and ``/api/info?model=GA4GH-ServiceInfo-v0.1`` -  Information about the Beacon (GA4GH Specification);
* ``/api/services`` -  Information about the services, required by the Beacon Network;
* ``/api/access_levels`` -  Information about the access levels of the Beacon;
* ``/api/filtering terms`` -  Information about existing ontology filters in the Beacon;
* ``/api/query`` -  querying/filtering datasets in the Beacon;
* ``/api/genomic_query`` -  querying/filtering datasets in the Beacon that contain a certain SNP or that contain variants inside a certain region;
* ``/api/genomic_snp`` -  querying/filtering datasets in the Beacon that contain a certain SNP;
* ``/api/genomic_region`` -  querying/filtering datasets in the Beacon that contain variants inside a certain region;
* ``/api/samples`` -  querying/filtering samples in the Beacon that match certain parameters and/or contain a certain variant;
* ``/api/individuals`` -  querying/filtering individuals in the Beacon that match certain parameters and/or contain a certain variant;

"""

import logging

from server.utils.exceptions import BeaconBadRequest
from server.validation.fields import *
from server.validation.request import RequestParameters
from server.utils.exceptions import BeaconUnauthorised
from server.utils.streamer import json_response

LOG = logging.getLogger(__name__)

class GVariantParametersBase(RequestParameters):
    start = BoundedListField(name='start', items=IntegerField(min_value=0, default=None), min_items=1, max_items=2)
    end = BoundedListField(name='end', items=IntegerField(min_value=0, default=None), min_items=1, max_items=2)
    referenceBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
    alternateBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
    referenceName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14",
                                "15", "16", "17", "18", "19", "20",
                                "21", "22", "X", "Y", "MT")
    includeDatasetResponses = ChoiceField("NONE", "ALL", "HIT", "MISS", default="NONE")
    assemblyId = RegexField(r'^((GRCh|hg)[0-9]+([.]?p[0-9]+)?)$', ignore_case=True, default=None)
    variantType = ChoiceField("DEL", "INS", "DUP", "INV", "CNV", "SNP", "MNP", "DUP:TANDEM", "DEL:ME", "INS:ME", "BND")

    # Examples:
    # PATO:0000011<=P70Y
    # HP:0100526-
    # HP:0005978
    # HP:0012622&sim=low
    # HP:0012622&sim=medium
    # HP:0012622&sim=high
    # HP:0032443="unknown medical history"
    # HP:0032443=%"unknown medical history"%
    # HP:0032443=!"unknown medical history"
    # filters = ListField(items=RegexField(r'^.*:\w+(>|<)?=?P?[0-9]+Y?$'), default=None)
    filters = ListField(items=RegexField(r'^.*:\w+(((>|<)?=?(P?[0-9]+Y?))|-|&sim=(low|medium|high)|=(%|!)?"[0-9a-zA-Z\s]+"%?)?$'), default=None)

    datasetIds = DatasetsField()
    # TODO implement fusions
    mateName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
        "8", "9", "10", "11", "12", "13", "14",
        "15", "16", "17", "18", "19", "20",
        "21", "22", "X", "Y", "MT"
    )

    apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')
    # pagination
    skip = IntegerField(min_value=0, default=0)
    limit = IntegerField(min_value=1, default=10)
    targetIdReq = Field(default=None)

    def correlate(self, req, values):

        if values.variantType and values.alternateBases and values.alternateBases != "N":
            raise BeaconBadRequest("If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'")

        if values.end is not None and len(values.end) == 1 and values.start is None:
            raise BeaconBadRequest("'start' is required if 'end' is provided")

        if values.referenceBases is not None and (values.alternateBases is None or values.start is None):
            raise BeaconBadRequest("If 'referenceBases' is provided then 'alternateBases' and ' start' are required")

        if (values.referenceBases is not None or values.alternateBases is not None) and len(values.end) > 0:
            raise BeaconBadRequest("'referenceBases' cannot be combined with 'end'")

        if (values.start or values.referenceName or values.alternateBases or values.variantType or values.end ) \
                and (values.referenceName is None or values.assemblyId is None):
            raise BeaconBadRequest("'assemblyId' and 'referenceName' are mandatory")

        if len(values.start) == 2 and (values.end is None or len(values.end) == 1) \
                or len(values.end) == 2 and (values.start is None or len(values.start) == 1):
            raise BeaconBadRequest("All 'start[0]', 'start[1]', 'end[0]', 'end[1]' are required")

        if len(values.end) > 0 and values.end[0] < values.start[0]:
            raise BeaconBadRequest("'end[0]' must be greater than 'start[0]'")

        if len(values.start) > 1 and values.start[0] > values.start[1]:
            raise BeaconBadRequest("'start[0]' must be smaller than 'start[1]'")

        if len(values.end) > 1 and values.end[0] > values.end[1]:
            raise BeaconBadRequest("'end[0]' must be smaller than 'end[1]'")

        if values.mateName:
            raise BeaconBadRequest("Queries using 'mateName' are not implemented (yet)")


class BiosamplesParameters(GVariantParametersBase):
    requestedSchema = SchemaField('ga4gh-phenopacket-biosample-v1.0',
                                  'beacon-biosample-v2.0.0-draft.3',
                                  default='beacon-biosample-v2.0.0-draft.3')

class IndividualsParameters(GVariantParametersBase):
    requestedSchema = SchemaField('ga4gh-phenopacket-individual-v1.0',
                                  'beacon-individual-v2.0.0-draft.3',
                                  default='beacon-individual-v2.0.0-draft.3')
    id = StringField()
    family_id = StringField() 
    index = ChoiceField('Yes', 'No')
    solved = ChoiceField('Solved','Unsolved','NA')
    sex = ChoiceField('F', 'M', 'U')
    affectedStatus = ChoiceField('Affected', 'Unaffected', 'Unknown')
    lifeStatus = ChoiceField('Alive', 'Deceased')


class GVariantsParameters(GVariantParametersBase):
    requestedSchema = SchemaField('beacon-variant-v2.0.0-draft.3',
                                  'ga4gh-phenopacket-variant-v1.0',
                                  'ga4gh-variant-representation-v1.1',
                                  default='beacon-variant-v2.0.0-draft.3')
    requestedAnnotationSchema = SchemaField('beacon-variant-annotation-v2.0.0-draft.3',
                                            'ga4gh-phenopacket-variant-annotation-v1.0',
                                  default='beacon-variant-annotation-v2.0.0-draft.3')

class CohortParameters(GVariantParametersBase):
    requestedSchema = SchemaField(
        'beacon-cohort-v2.0.0-draft.3.1',
        default='beacon-cohort-v2.0.0-draft.3.1'
    )

class ValidationError(Exception):
    pass