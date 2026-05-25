import pytest

from src.modules.history.use_cases.get_history import GetHistoryUseCase
from src.modules.history.use_cases.get_history_by_user import GetHistoryByUserUseCase
from src.modules.history.use_cases.record_history import RecordHistoryUseCase
from src.shared.exceptions.domain import NotFoundError
from tests.conftest import make_history, make_user


class TestRecordHistoryUseCase:
    async def test_record_creates_entry(self, history_repo):
        uc = RecordHistoryUseCase(history_repo)
        await uc.execute(1, "create", "user", 1, "User created")

        history_repo.create.assert_awaited_once_with(
            {
                "user_id": 1,
                "action": "create",
                "entity_type": "user",
                "entity_id": 1,
                "details": "User created",
            }
        )


class TestGetHistoryUseCase:
    async def test_get_history(self, history_repo):
        history_repo.get_all.return_value = [make_history(id=1), make_history(id=2)]
        history_repo.count.return_value = 2
        uc = GetHistoryUseCase(history_repo)

        entries, total = await uc.execute()
        assert len(entries) == 2
        assert total == 2

    async def test_get_history_empty(self, history_repo):
        history_repo.get_all.return_value = []
        history_repo.count.return_value = 0
        uc = GetHistoryUseCase(history_repo)

        entries, total = await uc.execute()
        assert entries == []
        assert total == 0


class TestGetHistoryByUserUseCase:
    async def test_get_history_by_user(self, history_repo, user_repo):
        user_repo.get_by_id.return_value = make_user(id=1)
        history_repo.get_by_user.return_value = [make_history(id=1, user_id=1)]
        history_repo.count_by_user.return_value = 1

        uc = GetHistoryByUserUseCase(history_repo, user_repo)
        entries, total = await uc.execute(1)
        assert len(entries) == 1
        assert total == 1

    async def test_get_history_user_not_found(self, history_repo, user_repo):
        user_repo.get_by_id.return_value = None
        uc = GetHistoryByUserUseCase(history_repo, user_repo)

        with pytest.raises(NotFoundError, match="Usuario"):
            await uc.execute(999)
