from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

# Import model classes untuk memastikan mereka ter-register oleh SQLAlchemy
from .meta import Base
from .mahasiswa import Mahasiswa
from .matakuliah import Matakuliah

# Jalankan configure_mappers setelah seluruh model diimpor
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    """Mendapatkan engine database SQLAlchemy dengan fallback otomatis jika server PostgreSQL lokal tidak aktif."""
    url = settings.get(prefix + 'url', '')
    fallback_url = settings.get('pyramid_mahasiswa.fallback_url')

    # Filter parameter khusus agar tidak dilewatkan ke create_engine
    filtered_settings = {k: v for k, v in settings.items() if k.startswith(prefix)}

    try:
        engine = engine_from_config(filtered_settings, prefix)
        # Uji koneksi aktif terutama untuk dialek PostgreSQL
        if 'postgresql' in url:
            with engine.connect() as conn:
                pass
        return engine
    except Exception as e:
        if fallback_url:
            print(f"[INFO] Database utama PostgreSQL ({url}) tidak aktif: {e}")
            print(f"[INFO] Menggunakan fallback database SQLite: {fallback_url}")
            fb_settings = dict(filtered_settings)
            fb_settings[prefix + 'url'] = fallback_url
            return engine_from_config(fb_settings, prefix)
        raise


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """Mendapatkan SQLAlchemy Session yang terikat otomatis dengan zope.sqlalchemy"""
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """Inisialisasi konfigurasi database saat Pyramid startup"""
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry['dbsession_factory'] = session_factory

    # Menyediakan properti request.dbsession di setiap request HTTP
    config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )
