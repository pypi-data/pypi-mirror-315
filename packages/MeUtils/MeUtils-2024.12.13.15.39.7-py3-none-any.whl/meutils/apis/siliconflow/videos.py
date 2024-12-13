#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2024/12/12 08:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.caches.redis_cache import cache
from meutils.llm.check_utils import check_token_for_siliconflow
from meutils.schemas.task_types import TaskResponse
from meutils.schemas.siliconflow_types import BASE_URL, VideoRequest
from meutils.config_utils.lark_utils import get_next_token_for_polling

from openai import OpenAI, AsyncOpenAI

FEISHU_URL_FREE = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=ICzCsC"

check_token = partial(check_token_for_siliconflow, threshold=0.01)


@cache(ttl=7 * 24 * 3600)
async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL_FREE, check_token=check_token, from_redis=True)

    payload = request.model_dump(exclude_none=True)
    payload["model"] = "tencent/HunyuanVideo"

    client = OpenAI(
        base_url=BASE_URL,
        api_key=token
    )

    response = client.post("/video/submit", cast_to=object, body=payload)
    logger.debug(response)
    task_id = response.get('requestId')

    return TaskResponse(task_id=task_id, system_fingerprint=token)


async def get_task(task_id, token: str):
    client = OpenAI(
        base_url=BASE_URL,
        api_key=token
    )
    payload = {"requestId": task_id}
    response = client.post(f"/video/status", cast_to=object, body=payload)
    logger.debug(response)

    return TaskResponse(
        task_id=task_id,
        data=response.get("results"),
        status=response.get("status"),
        message=response.get("reason"),
    )


if __name__ == '__main__':
    token = None
    # tokens = config_manager.text.split()

    # tokens_ = arun(check_token_for_siliconflow(tokens, threshold=0.01))

    token = "sk-raapiguffsnsxgkfiwfusjmbpcyqoxhcohhxaybflrnvpqjw"
    arun(get_task("73a15e11-310f-4464-a9af-3ab84b201fff", token))

    # token = "sk-oeptckzkhfzeidbtsqvbrvyrfdtyaaehubfwsxjytszbgohd"
    # arun(get_task("5ea22f57-45f0-425c-9d1e-bf3dae7e1e81", token))

    # arun(create_task(VideoRequest(model="tencent/HunyuanVideo", prompt="a dog in the forest."), token=token))
