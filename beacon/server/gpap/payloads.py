#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# "id": {"type": "string", "title": "Local ID","pattern": "^[_A-z0-9]*((-|/s)*[A-z0-9_.-])*$"},
# "family_id": {"type": "string", "title": "Local Family ID"},
# "template": {"type": "string", "title": "Form template"},
# "phenotips_id": {"type": "string", "title": "Phenotips ID"},
# "index": { "type": "string", "title": "Index case", "enum": ["Yes","No"]},
# "famid": {"type": "string", "title": "Family Id", "default": ""},
# "solved": {"type": "string", "title": "Solved status", "enum": ["Solved","Unsolved","NA"]},
# "sex": {"type": "string", "enum": ["M","F","U"], "enumNames": ["Male","Female","Unknown"],"title": "Sex"},
# "affectedStatus": {"type": "string", "title": "Disease status" ,"enum": ["Affected","Unaffected","Unknown"]},
# "birth": {"type": "string","title": "Date of birth*"},
# "lifeStatus":  {"type": "string", "title": "Vital status", "enum": ["Alive","Deceased"],"default": "Alive"},
# "country_of_birth":  {"$ref": "#/definitions/country", "title": "Country of birth", "default": "Unknown"},
# "baselineage": {"type": "integer","title": "Baseline age"},
# "referral": {"type": "string","title": "Indication for referral"}


def phenostore_playload(qparams):
    """
    PhenoStore filtering ciretia to be included as playload in each query.
    """
    return {"page":1,"pageSize":10,"sorted":[],"filtered":[],"aggrKeys":["sex","affectedStatus","solved","index"]}