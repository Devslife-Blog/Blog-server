from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..settings import settings
from .. import crud, deps, schemas, security

router = APIRouter()


@router.post("{}".format(settings.signup_url))
def signup_request(
        form: schemas.SignupRequestCreate, db: Session = Depends(deps.get_db),
):
    username_check = crud.get_user(db, form.username)
    if username_check:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="username already exists"
        )
    fullname_check = crud.get_user_by_fullname(db, form.fullname)
    if fullname_check:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="username already exists"
        )
    email_check = crud.get_user_by_email(db, form.email)
    if email_check:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="username already exists"
        )
    if not crud.is_email(form.email):
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="email is invalid"
        )
    # TODO: check if signup request with this properties exists or no
    # TODO: hash password and save request
    crud.create_singup_request(db, form=form)
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="request saved"
    )


@router.post("/signup/answer")
def answer_signup_request(
        form: schemas.AnswerSignupRequest, db: Session = Depends(deps.get_db)
):
    signup_request = crud.get_signup_request(db, form.request_id)
    if not signup_request:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="request not found"
        )
    if form.answer:
        new_user_dict = {
            'username': signup_request.username,
            'fullname': signup_request.fullname,
            'email': signup_request.email,
            'password': security.hash_password(signup_request.password),
        }
        new_user_schema = schemas.UserCreate(**new_user_dict)
        crud.create_user(db, new_user_schema)
        crud.delete_signup_request(db, form.request_id)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="user created"
        )
    else:
        crud.delete_signup_request(db, form.request_id)
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="request not accepted"
        )
