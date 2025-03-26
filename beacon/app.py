#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Beacon API Web Server for RD-Connect (R) at CNAG-CRG.
Designed with async/await programming model.

Author: Carles Hernandez-Ferrer
Last update: November, 24th, 2021
Creation date: May 3th, 2021

"""

__title__ = 'Beacon v2.0.0.d4'
__version__ = VERSION = '2.0.0.d4'
__author__ = 'CNAG-CRG Bioinformatic Unit, Analysis Team'
__license__ = 'MIT'
__copyright__ = 'Beacon 2.0.0.d4 @ CNAG-CRG, Barcelona, Spain'


from aiohttp import web
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import asyncio
import datetime
import jwt
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy import create_engine
from server.db_model import History

from server.config import config
from server.logger import LOG
from server.framework.endpoints import routes

jwt_options = config.jwt_options
jwt_algorithm = config.jwt_algorithm
public_key  = '-----BEGIN PUBLIC KEY-----\n' + config.beacon_idrsa + '\n-----END PUBLIC KEY-----'

#For restart on change
#from watchgod import run_process
#from asgiref.wsgi import WsgiToAsgi
#from asgiref.compatibility import guarantee_single_callable


# Set up the SQLAlchemy engine and session for asynchronous use
DATABASE_URL = config.SQLALCHEMY_DATABASE_URI

# Create the async engine
engine = create_engine(DATABASE_URL, echo=True)

# Set up a base class for models
Base = declarative_base()

# Create a session factory bound to the engine
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

#Beacon keys
beacon_keys = config.beacon_keys
keys_list = list(map(lambda x: x['key'], beacon_keys))

#Middleware to manage DB sessions in requests
@web.middleware
async def db_session_middleware(request, handler):
    request.db = SessionLocal()
    try:       
        #Log history after the response is generated
        if (request.method != "OPTIONS"):

            response = await handler(request)

            token = request.headers.get('auth-key')

            if config.fixed_token_use:
                if (token in keys_list):
                    user_name = next(item["contact"] for item in beacon_keys if item["key"] == token)
                    institution = next(item["institution"] for item in beacon_keys if item["key"] == token)
                else:
                    if token:
                        user_name = institution = "invalid_token"
                    else:
                        user_name = institution = "missing_token"
            
            else:
                try:
                    decoded  = jwt.decode (token, public_key, algorithms = jwt_algorithm, options = jwt_options )
                    user_name = decoded['preferred_username']
                    institution = decoded['group']
                except Exception as e:
                    user_name = institution = "invalid_token"


            if not (config.gpap_token_required[0]):
                user_name = institution = "no_token_required"

            timestamp = datetime.datetime.now()
            splitted = str(request.url).split("/")
            entity_id = splitted[len(splitted)-1]            
            content = await request.json() if request.method in ['POST', 'PUT'] else {} 
            res_status_code = response.status
                       
            info_endpoints = ["api", "info", "map", "service-info", "configuration", "entry_types", "filtering_terms"]
 
            if entity_id not in info_endpoints:
                await create_history_entry(request, entity_id, timestamp, user_name, institution, content, res_status_code)

            return response
    finally:
        request.db.close()
        

async def create_history_entry(request, entity_id, timestamp, user_name, institution, content, res_status_code):
    history = History(
        entity_id=entity_id,
        timestamp=timestamp,
        username=user_name,
        groups=institution,
        endpoint=str(request.url),
        method=request.method,
        content=content,
        response_status_code = res_status_code
    )

    # Save the history entry to the database
    with request.db.begin(): 
        request.db.add(history)
        request.db.commit()


# Create the database and tables if they do not exist
def init_db():
    Base.metadata.create_all(engine) 


#For restart on change
'''def create_app():
    """Creates and configures the aiohttp application."""
    config.load_filts()
    init_db()

    app = web.Application(middlewares=[db_session_middleware])
    app.add_routes(routes)
    return app


def start_server():
    """Starts the aiohttp application."""
    app = create_app()
    web.run_app(
        app,
        host=getattr(config, "beacon_host", "0.0.0.0"),
        port=getattr(config, "beacon_port", 5050),
        shutdown_timeout=0,
        ssl_context=None,
    )


if __name__ == "__main__":
    # Use watchgod to restart the server on file changes
    run_process(".", target=start_server)'''


#Default main
def main():
    config.load_filts()

    init_db()

    beacon = web.Application(middlewares=[db_session_middleware])
    beacon.add_routes(routes)

    web.run_app(
        beacon,
        host=getattr(config, 'beacon_host', '0.0.0.0'),
        port=getattr(config, 'beacon_port', 5050),
        shutdown_timeout=0,
        ssl_context=None
    )


if __name__ == '__main__':
    main()