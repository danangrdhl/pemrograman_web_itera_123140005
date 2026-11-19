from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from pyramid.paster import get_appsettings

from alembic import context

# Objek konfigurasi Alembic yang membaca berkas .ini
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import declarative base metadata untuk autogenerate
from pyramid_mahasiswa.models.meta import Base
target_metadata = Base.metadata


def get_engine():
    # Ambil konfigurasi dari section [app:main] pada development.ini
    settings = get_appsettings(config.config_file_name, name='main')
    url = settings.get('sqlalchemy.url', '')
    fallback_url = settings.get('pyramid_mahasiswa.fallback_url')

    filtered_settings = {k: v for k, v in settings.items() if k.startswith('sqlalchemy.')}

    try:
        engine = engine_from_config(
            filtered_settings,
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
        )
        if 'postgresql' in url:
            with engine.connect() as conn:
                pass
        return engine
    except Exception as e:
        if fallback_url:
            print(f"[INFO] PostgreSQL tidak aktif ({url}): {e}")
            print(f"[INFO] Alembic menggunakan fallback database: {fallback_url}")
            fb_settings = dict(filtered_settings)
            fb_settings['sqlalchemy.url'] = fallback_url
            return engine_from_config(
                fb_settings,
                prefix='sqlalchemy.',
                poolclass=pool.NullPool,
            )
        raise


def run_migrations_offline():
    settings = get_appsettings(config.config_file_name, name='main')
    url = settings.get('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
