#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : tenant_middleware
# Author  : zhoubohan
# Date    : 2024/12/6
# Time    : 20:33
# Description :
"""
import bcelogger
from typing import Callable, Union

from bceiam.middleware.auth import const
from bceserver.auth.consts import (
    GLOBAL_AUTH_INFO_KEY,
    GLOBAL_CONFIG_KEY,
    GLOBAL_TENANT_CLIENT_KEY,
)
from bceserver.context.singleton_context import SingletonContext
from fastapi import Request
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from tenantv1.client.tenant_api import (
    ErrorResult,
    Message,
    IAMInfoRequest,
    UserDepartmentRequest,
    DEPARTMENT_NAME,
    DEPARTMENT_ID,
)
from tenantv1.client.tenant_client import TenantClient


class TenantServiceError(Exception):
    """
    TenantServiceError
    """

    pass


def tenant_handler(
    auth_info: dict[str, str], tenant_client: TenantClient
) -> Union[TenantServiceError, dict[str, str]]:
    """
    tenant service handler
    :param auth_info: auth_info
    :param tenant_client: TenantClient

    """
    context_manager = SingletonContext.instance()

    org_id = auth_info.get(const.ORG_ID, "")
    user_id = auth_info.get(const.USER_ID, "")
    auth_mode = auth_info.get(const.AUTH_MODE, "")

    if len(org_id) == 0 or len(user_id) == 0:
        bcelogger.error("[TenantHandler]org_id or user_id is empty")
        return TenantServiceError("org_id or user_id is empty")

    if auth_mode.startswith("IAM"):
        user_info = tenant_client.get_tenant_user_by_iam_info(
            IAMInfoRequest(iam_account_id=org_id, iam_user_id=user_id)
        )

        if (
            user_info.result is None
            or user_info.result.tenant_id is None
            or user_info.result.idaas_user_id is None
        ):
            bcelogger.error(
                f"[TenantHandler]get tenant user by iam info err:{user_info.message}"
            )
            return TenantServiceError(
                f"get tenant user by iam info err:{user_info.message}"
            )

        org_id = user_info.result.tenant_id
        user_id = user_info.result.idaas_user_id
        auth_info[const.ORG_ID] = org_id
        auth_info[const.USER_ID] = user_id

    if len(auth_info.get(DEPARTMENT_ID, "")) > 0:
        return auth_info

    department_info = tenant_client.get_user_department(
        UserDepartmentRequest(user_id=user_id)
    )

    if department_info.result is None or department_info.result.department_id is None:
        bcelogger.error(
            f"[TenantHandler]get department info err:{department_info.message} user_id:{user_id}"
        )
        return TenantServiceError(
            f"get department info err:{department_info.message} user_id:{user_id}"
        )

    auth_info[DEPARTMENT_ID] = department_info.result.department_id
    auth_info[DEPARTMENT_NAME] = department_info.result.department_name

    context_manager.set_var_value(GLOBAL_AUTH_INFO_KEY, auth_info)

    return auth_info


class TenantMiddleware(BaseHTTPMiddleware):
    """
    TenantMiddleware
    """

    async def dispatch(self, request: Request, call_next: Callable):
        """
        dispatch
        :param request:
        :param call_next:
        :return:
        """
        context_manager = SingletonContext.instance()
        tenant_client: TenantClient = context_manager.get_var_value(
            GLOBAL_TENANT_CLIENT_KEY
        )
        global_config = context_manager.get_var_value(GLOBAL_CONFIG_KEY)
        err_result = ErrorResult(
            code="UserDepartmentFail",
            message=Message(redirect=global_config.tenant.redirect_login_url),
            success=False,
        )

        auth_info = getattr(request.state, GLOBAL_AUTH_INFO_KEY, None)
        if auth_info is None:
            bcelogger.error("[TenantMiddleware]auth info is None")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=err_result.model_dump(),
            )

        auth_info = tenant_handler(auth_info, tenant_client)
        if isinstance(auth_info, TenantServiceError):
            bcelogger.error(f"[TenantMiddleware]get department err:{str(auth_info)}")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=err_result.model_dump(),
            )

        setattr(request.state, GLOBAL_AUTH_INFO_KEY, auth_info)

        return await call_next(request)
