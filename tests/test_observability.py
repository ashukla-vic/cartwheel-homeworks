"""Authentication tests for the Homework 2 endpoint.

No Langfuse, Docker, or model key is needed: the checks run against the
session helpers directly.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from server import app as server_app


@pytest.fixture(autouse=True)
def _isolated_sessions(world, tmp_path, monkeypatch):
    monkeypatch.setattr(server_app, "SESSIONS_DB", tmp_path / "sessions.db")
    server_app._SESSIONS.clear()
    yield
    server_app._SESSIONS.clear()


def test_session_creation_rejects_role_mismatch() -> None:
    # User 1 is a shopper in the database; claiming "support" must be refused.
    with pytest.raises(HTTPException) as exc:
        server_app.create_session(server_app.SessionCreate(user_id=1, role="support"))
    assert exc.value.status_code == 403
    assert not server_app._SESSIONS


def test_token_for_one_session_cannot_authorize_another() -> None:
    first = server_app.create_session(server_app.SessionCreate(user_id=1, role="shopper"))
    second = server_app.create_session(
        server_app.SessionCreate(user_id=9002, role="merchant")
    )
    # Control: the token works for its own session.
    ctx = server_app._authorize(first["session_id"], f"Bearer {first['token']}")
    assert ctx.user_id == 1
    # The same token must not open a different session.
    with pytest.raises(HTTPException) as exc:
        server_app._authorize(second["session_id"], f"Bearer {first['token']}")
    assert exc.value.status_code == 403
