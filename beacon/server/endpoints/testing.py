import logging

# from aiohttp_session import get_session

# from ..utils.exceptions import BeaconBadRequest
# from ..validation.request import RequestParameters, print_qparams
# from ..validation.fields import (RegexField,
#                                  ChoiceField,
#                                  IntegerField,
#                                  ListField)
# from ..utils import resolve_token
# from ..utils.stream import json_stream
# from ..utils import db

from server.utils.streamer import json_reponse

LOG = logging.getLogger(__name__)

async def handler(request):
    # # Both in one: check the session, and if no session, check the header
    # session = await get_session(request)
    # token = session.get('access_token')
    # if not token:
    #     LOG.debug('No session token, checking the header')
    #     token = request.headers.get('Authorization')
    #     if token:
    #         LOG.debug('Got a header token')
    #         token = token[7:].strip() # 7 = len('Bearer ')

    # authorized_datasets, authenticated = await resolve_token(token, qparams_db.datasets)


    # response['authorized_datasets'] = authorized_datasets
    # response['authenticated'] = authenticated

    response = {'result': 'this is a test'}
    return await json_reponse(request, response)

