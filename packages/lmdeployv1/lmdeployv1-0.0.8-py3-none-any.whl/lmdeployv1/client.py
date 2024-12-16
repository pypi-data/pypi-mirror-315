#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : client
# Author  : zhoubohan
# Date    : 2024/11/29
# Time    : 14:18
# Description :
"""

from typing import Union, List, Optional

import httpx
from bceidaas.auth.bce_credentials import BceCredentials
from lmdeployv1.api import BatchChatCompletionRequest, BatchChatCompletionResponse
from openai import (
    OpenAI,
    AsyncOpenAI,
    Stream,
)
from openai.pagination import SyncPage
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionContentPartImageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_content_part_image_param import (
    ImageURL, )
from openai.types.model import Model
from tenacity import retry, stop_after_attempt


class LMDeployClient(object):
    """
    LMDeployClient is a client for lm deploy
    """

    def __init__(
        self,
        endpoint: str,
        base_url: str = "",
        credentials: BceCredentials = None,
        max_retries: int = 1,
        timeout_in_seconds: int = 30,
        is_async: bool = False,
        context: Optional[dict] = None,
    ):
        """
        Constructor
        """
        self._endpoint = endpoint
        self._base_url = base_url
        self._credentials = credentials
        self._is_async = is_async
        self._max_retries = max_retries
        self._timeout_in_seconds = timeout_in_seconds
        self._context = context

        if self._credentials is None:
            self._credentials = BceCredentials("", "")

        if self._base_url == "":
            self._base_url = "v1"

        self._endpoint = (self._endpoint.rstrip("/") + "/" +
                          self._base_url.strip("/") + "/")

        headers = dict()
        if self._context is not None:
            headers[b"x-impersonate-target-org-id"] = self._context.get(
                "OrgID", ""
            ).encode("utf-8")
            headers[b"x-impersonate-target-user-id"] = self._context.get(
                "UserID", ""
            ).encode("utf-8")
            headers[b"x-impersonate-target-project-id"] = self._context.get(
                "ProjectID", ""
            ).encode("utf-8")

        if is_async:
            self._openai_client = AsyncOpenAI(
                # api_key无作用，仅为绕过client参数检查
                api_key=self._credentials.access_key_id,
                base_url=self._endpoint,
                max_retries=self._max_retries,
                timeout=self._timeout_in_seconds,
                default_headers=headers,
            )

            self._http_client = httpx.AsyncClient(
                base_url=self._endpoint,
                timeout=self._timeout_in_seconds,
                headers=headers,
            )

        else:
            self._openai_client = OpenAI(
                # api_key无作用，仅为绕过client参数检查
                api_key=self._credentials.access_key_id,
                base_url=self._endpoint,
                max_retries=self._max_retries,
                timeout=self._timeout_in_seconds,
                default_headers=headers,
            )

            self._http_client = httpx.Client(
                base_url=self._endpoint,
                timeout=self._timeout_in_seconds,
                headers=headers,
            )

    async def async_models(self) -> SyncPage[Model]:
        """
        Get models
        """
        return await self._openai_client.models.list()

    def models(self) -> SyncPage[Model]:
        """
        Get models
        """
        return self._openai_client.models.list()

    async def async_available_models(self) -> Union[str, ValueError]:
        """
        Async Get available models
        """
        models = await self.async_models()
        if len(models.data) == 0:
            return ValueError("No available models")

        return models.data[0].id

    def available_models(self) -> Union[str, ValueError]:
        """
        Get available models
        """
        models = self.models()
        if len(models.data) == 0:
            return ValueError("No available models")

        return models.data[0].id

    def chat_completion(
        self,
        messages: list[ChatCompletionMessageParam],
        model: str = "",
        n: int = 1,
        max_completion_tokens: int = 512,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        presence_penalty: float = 0.6,
        frequency_penalty: float = 0.6,
        repetition_penalty: float = 1.2,
        stream: bool = False,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Chat completion
        """
        return self._openai_client.chat.completions.create(
            messages=messages,
            model=model,
            n=n,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=stream,
            extra_body={
                "repetition_penalty": repetition_penalty,
            },
        )

    async def chat_acompletion(
        self,
        messages: list[ChatCompletionMessageParam],
        model: str = "",
        n: int = 1,
        max_completion_tokens: int = 512,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        presence_penalty: float = 0.6,
        frequency_penalty: float = 0.6,
        repetition_penalty: float = 1.2,
        stream: bool = False,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Async Chat completion
        """
        return await self._openai_client.chat.completions.create(
            messages=messages,
            model=model,
            n=n,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=stream,
            extra_body={
                "repetition_penalty": repetition_penalty,
            },
        )

    async def batch_chat_acompletion(
        self,
        request: BatchChatCompletionRequest,
    ) -> BatchChatCompletionResponse:
        """
        Async batch chat completion
        """

        @retry(stop=stop_after_attempt(self._max_retries), reraise=True)
        async def _batch_chat_acompletion(req):
            response = await self._http_client.post(
                url="chat/batch_completions",
                json=req,
            )

            await response.aclose()
            response.raise_for_status()

            return BatchChatCompletionResponse.model_validate(response.json())

        return await _batch_chat_acompletion(request.model_dump())

    def batch_chat_completion(
        self,
        request: BatchChatCompletionRequest,
    ) -> BatchChatCompletionResponse:
        """
        Batch chat completion
        """

        @retry(stop=stop_after_attempt(self._max_retries), reraise=True)
        def _batch_chat_completion(req):
            response = self._http_client.post(
                url="chat/batch_completions",
                json=req,
            )

            response.close()
            response.raise_for_status()

            return BatchChatCompletionResponse.model_validate(response.json())

        return _batch_chat_completion(request.model_dump(mode="json"))


def format_base64_string(s: str) -> str:
    """
    Format base64 string
    """
    return f"data:image/jpeg;base64,{s}"


def build_batch_chat_messages(
        kv_list: List[dict[str,
                           str]]) -> List[List[ChatCompletionMessageParam]]:
    """
    Build batch chat messages
    :param kv_list: List{"image_url":"prompt"}
    :return:
    """
    messages: List[List[ChatCompletionMessageParam]] = []

    for kv in kv_list:
        for img_url, prompt in kv.items():
            content: List[ChatCompletionContentPartParam] = []
            text_param = ChatCompletionContentPartTextParam(type="text",
                                                            text=prompt)
            content.append(text_param)

            image_url = ImageURL(url=img_url)
            image_param = ChatCompletionContentPartImageParam(
                type="image_url", image_url=image_url)
            content.append(image_param)

            message_param = ChatCompletionUserMessageParam(role="user",
                                                           content=content)

            messages.append([message_param])

    return messages


def build_chat_messages(
        kv: dict[str, str]) -> List[ChatCompletionMessageParam]:
    """
    Build chat messages
    :param kv: {"image_url":"prompt"}
    :return:
    """
    content: List[ChatCompletionContentPartParam] = []

    for img_url, prompt in kv.items():
        text_param = ChatCompletionContentPartTextParam(type="text",
                                                        text=prompt)
        content.append(text_param)

        image_url = ImageURL(url=img_url)
        image_param = ChatCompletionContentPartImageParam(type="image_url",
                                                          image_url=image_url)
        content.append(image_param)

    messages: List[ChatCompletionMessageParam] = []

    message_param = ChatCompletionUserMessageParam(role="user",
                                                   content=content)

    messages.append(message_param)

    return messages