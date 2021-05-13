#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

def pytest_addoption(parser):
    parser.addoption("--token", action = 'store')

@pytest.fixture(scope = 'session')
def token(request):
    token_value = request.config.option.token
    if token_value is None:
        pytest.skip()
    return token_value