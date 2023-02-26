from sqlalchemy import func

from .. import models, schemas, oath2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=['POSTS']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10,
              skip: int = 0, search: Optional[str] = ''):
    # cursor.execute('''SELECT * FROM posts''')  # comando em SQL
    # posts = cursor.fetchall()  # pegar todos os posts

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # query simples

    # caso você queira que o usuario retorne apenas as proprias postagens.
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                       models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # query composta - duas mesas
    return posts


# The POST method submits an entity to the specified resource,
# often causing a change in state or side effects on the server.
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''',
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()  # pegar um post especifico.
    # conn.commit()  # salva no banco de dados

    new_post = models.Post(owner_id=current_user.id, **post.dict())  # cria o post
    db.add(new_post)  # adiciona o post a base de dados
    db.commit()  # salva essa alteração
    db.refresh(new_post)  # atualiza o banco de dados com as novas informações
    return new_post  # mandar de volta os dados para a API


# pegando um post da lista
@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts WHERE id = %s''', str(id))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                       models.Vote.post_id == models.Post.id, isouter=True).\
        group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

    # caso queira retornar a postagem apenas se for o usuario que a criou
    # if posts.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform request action')

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s returning *''', str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)  # definimos a consulta

    post = post_query.first()  # achamos a postagem

    # verificamos se ele existe
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')

    # verificamos se o usuario logado é dono desta postagem
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform request action')

    else:
        post_query.delete(synchronize_session=False)  # deletamos ele da consulta.
        db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''',
    #                (post.title, post.content, post.published, str(id)))  # %s == placeholder - impede fragilidades
    # # no codigo.
    # updated_post = cursor.fetchone()
    # conn.commit()  # sempre que quiser realizar mudanças em um banco de dados.
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform request action')

    else:
        post_query.update(updated_post.dict(), synchronize_session=False)

        db.commit()

    return post_query.first()
