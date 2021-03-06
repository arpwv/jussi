# -*- coding: utf-8 -*-
import asyncio
import logging

import ujson

from ..typedefs import HTTPRequest
from ..typedefs import HTTPResponse
from ..utils import async_nowait_middleware
from ..validators import is_get_dynamic_global_properties_request

logger = logging.getLogger(__name__)


@async_nowait_middleware
async def update_last_irreversible_block_num(request: HTTPRequest, response: HTTPResponse) -> None:
    if request.method != 'POST':
        return
    try:
        jsonrpc_request = request.json
        jsonrpc_response = ujson.loads(response.body)
        if is_get_dynamic_global_properties_request(jsonrpc_request):
            last_irreversible_block_num = jsonrpc_response['result']['last_irreversible_block_num']
            cache_group = request.app.config.cache_group
            await asyncio.shield(cache_group.set('last_irreversible_block_num',
                                                 last_irreversible_block_num))
            logger.debug(
                f'updated last_irreversible_block_num: {last_irreversible_block_num}')
    except Exception:
        logger.exception('skipping update of last_irreversible_block_num')
