from app.infra.database import create_session

from unittest.mock import MagicMock
from sqlalchemy.orm import Session

import pytest

def test_create_session(mocker):
    mock_session = MagicMock(spec=Session)
    mocker.patch('app.infra.database.Session', return_value=mock_session)

    session_gen = create_session()
    session = next(session_gen)

    assert session == mock_session

    with pytest.raises(StopIteration):
        next(session_gen)

    mock_session.close.assert_called_once()