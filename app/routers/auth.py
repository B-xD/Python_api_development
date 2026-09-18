from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session 
from .. import database, schemas, models, utils, auth2  

router = APIRouter(
    tags = ['Authentication']
    )

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    #create token 
    access_token = auth2.create_access_token(data = {"user_id" : user.id}) #put all information you want to pass

    #return token 
    return {"access_token": access_token, "token_type": "bearer"} #you configure the token type in the frontend 

#then go to the jwt website pass the token generated to see whats in the token