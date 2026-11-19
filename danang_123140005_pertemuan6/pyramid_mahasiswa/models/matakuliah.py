from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from .meta import Base


class Matakuliah(Base):
    """Model ORM untuk tabel data matakuliah"""
    __tablename__ = 'matakuliah'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_mk = Column(Text, unique=True, nullable=False)
    nama_mk = Column(Text, nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    def to_dict(self):
        """Serialisasi objek model menjadi dictionary agar siap dirender sebagai JSON"""
        return {
            'id': self.id,
            'kode_mk': self.kode_mk,
            'nama_mk': self.nama_mk,
            'sks': self.sks,
            'semester': self.semester,
        }
