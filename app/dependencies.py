"""FastAPI dependencies for authentication."""

import os
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .auth import decode_access_token

AUTH_DISABLED = os.getenv("AUTH_DISABLED", "false").lower() == "true"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=not AUTH_DISABLED)


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
) -> dict:
    """Extract and verify the JWT from the Authorization header.

    When AUTH_DISABLED=true, authentication is skipped and a
    dummy user payload is returned (for local development only).

    Args:
        token: The Bearer token extracted by OAuth2PasswordBearer.

    Returns:
        The decoded JWT payload containing user information.
    """
    if AUTH_DISABLED:
        return {"sub": "dev-user"}

    return decode_access_token(token)
