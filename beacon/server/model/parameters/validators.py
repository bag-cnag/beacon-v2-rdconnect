#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.framework.exceptions import BeaconBadRequest
from server.model.schemas import supported_schemas, supported_schemas_by_entity

def api_version(val):
    if type(val) is not str or not val.startswith('2.0'):
        raise BeaconBadRequest('Beacon expected Beacon API v 2, requested "{}".'.format(val))
    return val

def requested_schemas(val):
    rst = []
    for elm in val:
        if elm['entityType'] in supported_schemas_by_entity.keys() and elm['schema'] in supported_schemas.keys():
            rst.append( { 'entityType': elm['entityType'], 'schema': elm['schema'] } )
        else:
            raise BeaconBadRequest('This Beacon does not suppor requested entity "{}" with schema "{}".'.format(elm['entityType'], elm['schema']))
    return rst

def filters(val):
    rst = []
    for idx, elm in enumerate(val):
        onf, onv = _flt_ontology(elm)
        anf, afn = _flt_alpnum(elm)
        if onf and not anf:
            rst.append(onv)
        elif anf:
            rst.append(afn)
        else:
            raise BeaconBadRequest('Invalid filter #{}'.format(str(idx)))
    return rst


def _flt_ontology(val):
    if not 'id' in val.keys():
        return False, {}
    else:
        rst = {}
        rst['id'] = val['id']
        if 'includeDescendantTerms' in val.keys():
            rst['includeDescendantTerms']
        if 'similarity' in val.keys() and val['similarity'] in ('exact', 'high', 'medium', 'low'):
            rst['similarity'] = val['similarity']
        if 'scope' in val.keys():
          rst['scope'] = val['scope']
        return True, rst


def _flt_alpnum(val):
    mandatory = ['id', 'operator', 'value']
    if sum( [ x in val.keys() for x in mandatory ]) == 3:
        rst = { 'id': val[id], 'operator': val['operator'], 'value': val['value'] }
        if 'scope' in val.keys():
            rst['scope'] = val['scope']
        return True, rst
    else:
        return False, {}


def pagination(val):
    mandatory = ['skip', 'limit']
    if sum( [ x in val.keys() for x in mandatory ]) == 2:
        rst = { 'skip': val['skip'], 'limit': val['limit'] }
    return rst

def requested_granularity(val):
    if val in ("boolean", "count", "aggregated", "record"):
        return val
    else:
        raise BeaconBadRequest('Invalid value for "requestedGranularity". Obatined "{}"'.format(str(val)))