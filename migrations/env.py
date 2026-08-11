"""Alembic migration environment."""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from masms_api.config import get_settings
from masms_api.db import Base
from masms_api.kernel import outbox as _outbox_models  # noqa: F401
from masms_api.modules.governance import models as _governance_models  # noqa: F401
from masms_api.modules.identity import models as _identity_models  # noqa: F401
from masms_api.modules.auth import models as _auth_models  # noqa: F401
from masms_api.modules.access import models as _access_models  # noqa: F401
from masms_api.modules.capacity import models as _capacity_models  # noqa: F401
from masms_api.modules.configadmin import models as _config_models  # noqa: F401
from masms_api.observability import models as _observability_models  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    return get_settings().database_url


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
