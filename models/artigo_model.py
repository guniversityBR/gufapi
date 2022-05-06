from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class ArtigoModel(settings.DBBaseModel):
    __tablename__ = 'artigos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    descricao = Column(String(256))
    url_fonte = Column(String(256))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    criador = relationship(
        "UsuarioModel", back_populates='artigos', lazy='joined')
