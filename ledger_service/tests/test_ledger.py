import pytest
from core.models import LedgerRequest, BalanceRequest
from core.operations import BaseLedgerOperations
from api.main import create_entry, get_balance
from uuid import uuid4


@pytest.mark.asyncio
async def test_create_valid_entry(test_session):
    request = LedgerRequest(
        app_id="test_app",
        operation=BaseLedgerOperations.CREDIT_ADD.value,
        owner_id="user1",
        nonce=str(uuid4())
    )

    entry = await create_entry(request, test_session)
    assert entry.amount == 10
    assert entry.app_id == "test_app"


@pytest.mark.asyncio
async def test_duplicate_nonce(test_session):
    nonce = str(uuid4())
    request = LedgerRequest(
        app_id="test_app",
        operation=BaseLedgerOperations.CREDIT_ADD.value,
        owner_id="user1",
        nonce=nonce
    )

    await create_entry(request, test_session)

    with pytest.raises(Exception) as exc_info:
        await create_entry(request, test_session)
    assert "Duplicate nonce" in str(exc_info.value)


@pytest.mark.asyncio
async def test_insufficient_balance(test_session):
    request = LedgerRequest(
        app_id="test_app",
        operation=BaseLedgerOperations.CREDIT_SPEND.value,
        owner_id="user2",
        nonce=str(uuid4())
    )

    with pytest.raises(Exception) as exc_info:
        await create_entry(request, test_session)
    assert "Insufficient balance" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_balance(test_session):
    # Add credit
    add_request = LedgerRequest(
        app_id="test_app",
        operation=BaseLedgerOperations.CREDIT_ADD.value,
        owner_id="user3",
        nonce=str(uuid4())
    )
    await create_entry(add_request, test_session)

    # Check balance
    balance_request = BalanceRequest(
        app_id="test_app",
        owner_id="user3"
    )
    balance = await get_balance(balance_request, test_session)
    assert balance == 10


@pytest.mark.asyncio
async def test_invalid_operation(test_session):
    request = LedgerRequest(
        app_id="test_app",
        operation="INVALID_OP",
        owner_id="user1",
        nonce=str(uuid4())
    )

    with pytest.raises(Exception) as exc_info:
        await create_entry(request, test_session)
    assert "Invalid operation" in str(exc_info.value)
