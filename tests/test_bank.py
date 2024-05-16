# import pytest

# @pytest.fixture(scope="function")
# def session(engine, tables):
#     # Créez une mock session utilisant UnifiedAlchemyMagicMock
#     session = UnifiedAlchemyMagicMock()
#     yield session
#     session.rollback()


import pytest
from unittest.mock import Mock
from source.example_app import main

@pytest.fixture
def mock_session():
    return Mock()


def test_main(mock_session):
    main(mock_session)

    # Vérifiez que les méthodes appropriées de la session ont été appelées
    assert mock_session.add.call_count == 4  # 2 transactions et 2 comptes
    assert mock_session.commit.call_count == 3  # 3 fois pour les 3 commit() dans main()
