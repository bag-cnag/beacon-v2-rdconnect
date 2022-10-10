#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from server.config import config

# THE FOLLIWING ARE THE TEST FOR THE ENDPOINTS NOT IMPLEMENTED
# THE FIRST SET OF TEST QUERY THOSE WITH NO TOKEN, EXPEXTING A 403

def test_individuals_by_biosample_no_token():
    target_id_req = 'unknown'
    url = '{}/api/biosamples/{}/individuals'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

def test_gvariants_by_biosample_no_token():
    target_id_req = 'unknown'
    url = '{}/api/biosamples/{}/g_variants'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

def test_individuals_by_variant_no_token():
    target_id_req = 'unknown'
    url = '{}/api/g_variants/{}/biosamples'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

def test_biosamples_by_variant_no_token():
    target_id_req = 'unknown'
    url = '{}/api/g_variants/{}/individuals'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

def test_gvariants_by_variant_no_token():
    url = '{}/api/g_variants'.format(config.server_api_url)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

    target_id_req = 'unknown'
    url = '{}/api/g_variants/{}'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

def test_gvariants_by_individual_no_token():
    target_id_req = 'unknown'
    url = '{}/api/individuals/{}/g_variants'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

def test_cohorts_by_cohort_no_token():
    url = '{}/api/cohorts'.format(config.server_api_url)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

    target_id_req = 'unknown'
    url = '{}/api/cohorts/{}'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, verify = False)
    assert rsp.status_code == 403

# THE SECOND SET OF TEST QUERY THOSE WITH TOKEN, EXPEXTING A 500
# WITH A BEACON ERROR 501

def test_individuals_by_biosample_with_token(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    target_id_req = 'unknown'
    url = '{}/api/biosamples/{}/individuals'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

def test_gvariants_by_biosample_with_token(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    target_id_req = 'unknown'
    url = '{}/api/biosamples/{}/g_variants'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

def test_individuals_by_variant_with_token(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    target_id_req = 'unknown'
    url = '{}/api/g_variants/{}/individuals'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

def test_biosamples_by_variant_with_token(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    target_id_req = 'unknown'
    url = '{}/api/g_variants/{}/biosamples'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

def test_gvariants_by_variant_with_token(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/g_variants'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

    target_id_req = 'unknown'
    url = '{}/api/g_variants/{}'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

def test_gvariants_by_individual_with_token(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    target_id_req = 'unknown'
    url = '{}/api/individuals/{}/g_variants'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

def test_cohorts_by_cohort_with_token(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/cohorts'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

    target_id_req = 'unknown'
    url = '{}/api/cohorts/{}'.format(config.server_api_url, target_id_req)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 500
    assert cnt['response']['error']['errorCode'] == 501

