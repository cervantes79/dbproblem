from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from core.models import LedgerEntry, LedgerRequest, BalanceRequest
from core.operations import BaseLedgerOperations, OPERATION_VALUES
from core.database import get_session
from typing import Annotated

app = FastAPI()


@app.post("/ledger/balance")
async def get_balance(
    request: BalanceRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
) -> int:
    result = await session.execute(
        select(func.sum(LedgerEntry.amount))
        .where(
            LedgerEntry.app_id == request.app_id,
            LedgerEntry.owner_id == request.owner_id
        )
    )
    return result.scalar() or 0


@app.post("/ledger")
async def create_entry(
    request: LedgerRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    # 1. Operation validation
    if request.operation not in BaseLedgerOperations.values():
        raise HTTPException(400, "Invalid operation")

    # 2. Nonce validation
    existing = await session.execute(
        select(LedgerEntry).where(LedgerEntry.nonce == request.nonce)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Duplicate nonce")

    amount = OPERATION_VALUES[request.operation]

    # 3. Balance check for debits
    if amount < 0:
        current = await get_balance(
            BalanceRequest(app_id=request.app_id, owner_id=request.owner_id),
            session
        )
        if current + amount < 0:
            raise HTTPException(400, "Insufficient balance")

    entry = LedgerEntry(
        app_id=request.app_id,
        operation=request.operation,
        amount=amount,
        nonce=request.nonce,
        owner_id=request.owner_id
    )

    session.add(entry)
    await session.commit()
    return entry
