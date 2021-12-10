#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
from server.framework.exceptions import BeaconBadRequest
from server.framework.request import RequestParameters
from server.model.schemas import supported_schemas
from server.model.parameters.fields import *

LOG = logging.getLogger(__name__)


def paramaters_to_entity(qparam):
    x = str(type(qparam)).split('.')[::-1][0].replace("'>", "")
    if x == 'DatasetsParameters':
        return 'DATASET'
    if x == 'CohortParameters':
        return 'COHORT'
    if x == 'BiosamplesParameters':
        return 'BIOSAMPLE'
    if x == 'IndividualsParameters':
        return 'INDIVIDUAL'
    return ''


class FilteredParameters(RequestParameters):
    apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')
    filters = ListField(items=RegexField(r'^.*:\w+(((>|<)?=?(P?[0-9]+Y?))|-|&sim=(low|medium|high)|=(%|!)?"[0-9a-zA-Z\s]+"%?)?$'), default=None)
    skip = IntegerField(min_value=0, default=0)
    limit = IntegerField(min_value=1, default=10)
    targetIdReq = Field(default=None)

class DatasetsParameters(FilteredParameters):
    requestedSchema = SchemaField('beacon-dataset-v2.0.0-draft.4', default = 'beacon-dataset-v2.0.0-draft.4')
    id              = StringField()

class CohortParameters(FilteredParameters):
    requestedSchema = SchemaField('beacon-cohort-v2.0.0-draft.4', default = 'beacon-cohort-v2.0.0-draft.4')

class BiosamplesParameters(FilteredParameters):
    requestedSchema = SchemaField('beacon-biosample-v2.0.0-draft.4', default = 'beacon-biosample-v2.0.0-draft.4') # TODO: add 'ga4gh-phenopacket-biosample-v1.0' (?)
    RD_Connect_ID_Experiment     = StringField()
    Participant_ID               = StringField()
    EGA_ID                       = StringField()
    Owner                        = StringField()
    in_platform                  = BooleanField()
    POSTEMBARGO                  = BooleanField()
    experiment_type              = StringField()
    kit                          = StringField()
    tissue                       = StringField()
    library_source               = ChoiceField('Genomic', 'Transcriptomic', 'Other')
    library_selection            = StringField()
    library_strategy             = StringField()
    library_contruction_protocol = StringField()
    erns                         = StringField()

class IndividualsParameters(FilteredParameters):
    requestedSchema = SchemaField('beacon-individual-v2.0.0-draft.4', default = 'beacon-individual-v2.0.0-draft.4') # TODO: add 'ga4gh-phenopacket-individual-v1.0'
    id             = StringField()
    family_id      = StringField() 
    index          = ChoiceField('Yes', 'No')
    solved         = ChoiceField('Solved','Unsolved','NA')
    sex            = ChoiceField('F', 'M', 'U')
    affectedStatus = ChoiceField('Affected', 'Unaffected', 'Unknown')
    lifeStatus     = ChoiceField('Alive', 'Deceased')













"""
from server.validation.fields import *
from server.validation.request import RequestParameters
from server.utils.exceptions import BeaconUnauthorised
from server.utils.streamer import json_response
"""




# class GVariantParametersBase(RequestParameters):
#     start = BoundedListField(name='start', items=IntegerField(min_value=0, default=None), min_items=1, max_items=2)
#     end = BoundedListField(name='end', items=IntegerField(min_value=0, default=None), min_items=1, max_items=2)
#     referenceBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
#     alternateBases = RegexField(r'^([ACGT]+)$', ignore_case=True, default=None)
#     referenceName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
#                                 "8", "9", "10", "11", "12", "13", "14",
#                                 "15", "16", "17", "18", "19", "20",
#                                 "21", "22", "X", "Y", "MT")
#     includeDatasetResponses = ChoiceField("NONE", "ALL", "HIT", "MISS", default="NONE")
#     assemblyId = RegexField(r'^((GRCh|hg)[0-9]+([.]?p[0-9]+)?)$', ignore_case=True, default=None)
#     variantType = ChoiceField("DEL", "INS", "DUP", "INV", "CNV", "SNP", "MNP", "DUP:TANDEM", "DEL:ME", "INS:ME", "BND")

#     # Examples:
#     # PATO:0000011<=P70Y
#     # HP:0100526-
#     # HP:0005978
#     # HP:0012622&sim=low
#     # HP:0012622&sim=medium
#     # HP:0012622&sim=high
#     # HP:0032443="unknown medical history"
#     # HP:0032443=%"unknown medical history"%
#     # HP:0032443=!"unknown medical history"
#     # filters = ListField(items=RegexField(r'^.*:\w+(>|<)?=?P?[0-9]+Y?$'), default=None)
#     filters = ListField(items=RegexField(r'^.*:\w+(((>|<)?=?(P?[0-9]+Y?))|-|&sim=(low|medium|high)|=(%|!)?"[0-9a-zA-Z\s]+"%?)?$'), default=None)

#     datasetIds = DatasetsField()
#     # TODO implement fusions
#     mateName = ChoiceField("1", "2", "3", "4", "5", "6", "7",
#         "8", "9", "10", "11", "12", "13", "14",
#         "15", "16", "17", "18", "19", "20",
#         "21", "22", "X", "Y", "MT"
#     )

#     apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')
#     # pagination
#     skip = IntegerField(min_value=0, default=0)
#     limit = IntegerField(min_value=1, default=10)
#     targetIdReq = Field(default=None)

#     def correlate(self, req, values):

#         if values.variantType and values.alternateBases and values.alternateBases != "N":
#             raise BeaconBadRequest("If 'variantType' is provided then 'alternateBases' must be empty or equal to 'N'")

#         if values.end is not None and len(values.end) == 1 and values.start is None:
#             raise BeaconBadRequest("'start' is required if 'end' is provided")

#         if values.referenceBases is not None and (values.alternateBases is None or values.start is None):
#             raise BeaconBadRequest("If 'referenceBases' is provided then 'alternateBases' and ' start' are required")

#         if (values.referenceBases is not None or values.alternateBases is not None) and len(values.end) > 0:
#             raise BeaconBadRequest("'referenceBases' cannot be combined with 'end'")

#         if (values.start or values.referenceName or values.alternateBases or values.variantType or values.end ) \
#                 and (values.referenceName is None or values.assemblyId is None):
#             raise BeaconBadRequest("'assemblyId' and 'referenceName' are mandatory")

#         if len(values.start) == 2 and (values.end is None or len(values.end) == 1) \
#                 or len(values.end) == 2 and (values.start is None or len(values.start) == 1):
#             raise BeaconBadRequest("All 'start[0]', 'start[1]', 'end[0]', 'end[1]' are required")

#         if len(values.end) > 0 and values.end[0] < values.start[0]:
#             raise BeaconBadRequest("'end[0]' must be greater than 'start[0]'")

#         if len(values.start) > 1 and values.start[0] > values.start[1]:
#             raise BeaconBadRequest("'start[0]' must be smaller than 'start[1]'")

#         if len(values.end) > 1 and values.end[0] > values.end[1]:
#             raise BeaconBadRequest("'end[0]' must be smaller than 'end[1]'")

#         if values.mateName:
#             raise BeaconBadRequest("Queries using 'mateName' are not implemented (yet)")

# class GVariantsParameters(GVariantParametersBase):
#     requestedSchema = SchemaField('beacon-variant-v2.0.0-draft.4',
#                                   'ga4gh-phenopacket-variant-v1.0',
#                                   'ga4gh-variant-representation-v1.1',
#                                   default='beacon-variant-v2.0.0-draft.4')
#     requestedAnnotationSchema = SchemaField('beacon-variant-annotation-v2.0.0-draft.4',
#                                             'ga4gh-phenopacket-variant-annotation-v1.0',
#                                   default='beacon-variant-annotation-v2.0.0-draft.4')



# class ValidationError(Exception):
#     pass

# import logging
# import re

# LOG = logging.getLogger(__name__)

# class ValidationError(Exception):
#     pass

# class RegexValidator:

#     def __init__(self, pattern, ignore_case):
#         self.pattern = pattern
#         flags = re.I if ignore_case else 0
#         self.regex = re.compile(pattern, flags=flags)

#     def __call__(self, value):
#         """
#         Validate that the input contains a match for the regular expression.
#         """
#         regex_matches = self.regex.search(str(value))
#         if not regex_matches:
#             raise ValidationError(f'{value} does not follow the pattern {self.pattern}')


# class EnumValidator:
#     enums = None
#     choices = None

#     def __init__(self, enums=None):
#         self.enums = enums or []
#         self.choices = set(self.enums)

#     def __call__(self, value):
#         """
#         Validate that the input is in the given enumeration.
#         """
#         if value not in self.choices:
#             if len(self.enums) == 1:
#                 message = f'{value} =/= {self.enums[0]}'
#             else:
#                 message = f'{value} not an element of {self.enums}'
#             raise ValidationError(message)


# # We limit the min-value and max-value validators
# # to using the < and > comparator.
# # We also just int or float, although we don't need to.

# class MinValueValidator:

#     def __init__(self, minimum=None):
#         assert isinstance(minimum, (int,float)), "Why don't you use an integer or a float?"
#         self.minimum = minimum

#     def __call__(self, value):
#         if value < self.minimum:
#             raise ValidationError(f'{value} < {self.minimum}')


# class MaxValueValidator:

#     def __init__(self, maximum=None):
#         assert isinstance(maximum, (int,float)), "Why don't you use an integer or a float?"
#         self.maximum = maximum

#     def __call__(self, value):
#         if value > self.maximum:
#             raise ValidationError(f'{value} > {self.maximum}')


