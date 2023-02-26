from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/users',  # todos os decorators ficam com esse inicio fixo por padrão
    tags=['USERS']  # separa nossa documentação no site.
)


# Registro de credenciais do usuario
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hashed(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())  # cria o post
    db.add(new_user)  # adiciona o post a base de dados
    db.commit()  # salva essa alteração
    db.refresh(new_user)  # atualiza o banco de dados com as novas informações

    return new_user  # mandar de volta os dados para a API


# Retorna as informações do usuario
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist')
    else:
        return user
