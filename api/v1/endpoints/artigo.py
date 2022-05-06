from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from core.deps import get_session, get_current_user


router = APIRouter()


# POST Artigo
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(
        titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=artigo.url_fonte, usuario_id=usuario_logado.id)

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo


# GET Artigos
@router.get('/', response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()

        return artigos


# GET Artigo
@router.get('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Artigo
@router.put('/{artigo_id}', response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_up: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_up:
            if artigo.titulo:
                artigo_up.titulo = artigo.titulo
            if artigo.descricao:
                artigo_up.descricao = artigo.descricao
            if artigo.url_fonte:
                artigo_up.url_fonte = artigo.url_fonte
            if usuario_logado.id != artigo_up.usuario_id:
                artigo_up.usuario_id = usuario_logado.id

            await session.commit()

            return artigo_up
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Artigo
@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(
            ArtigoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        artigo_del: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo_del:
            await session.delete(artigo_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
