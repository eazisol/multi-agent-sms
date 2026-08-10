"""SQLAlchemy unit of work (MOD-020-MP-005)."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.orm import Session


class SqlAlchemyUnitOfWork:
    """Thin transactional boundary over a Session.

    Application services must mutate business state through the session owned by
    this UoW and commit once per use-case. Agents/workflows must call APIs, not
    open sessions against business tables.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, instance: object) -> None:
        self.session.add(instance)

    def flush(self) -> None:
        self.session.flush()

    def refresh(self, instance: object) -> None:
        self.session.refresh(instance)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    @contextmanager
    def transaction(self) -> Iterator[SqlAlchemyUnitOfWork]:
        try:
            yield self
            self.commit()
        except Exception:
            self.rollback()
            raise


def get_uow(session: Session) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)
