from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .settings import settings
from . import crud, database, deps, security
from .routes.user import router

app = FastAPI(name="Devslife Blog", version="1.0")
app.include_router(router, prefix="/user")


@app.on_event('startup')
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)
    db: Session = database.SessionLocal()
    db.close()


@app.post("{}".format(settings.login_url))
def login_for_access_token(
        db: Session = Depends(deps.get_db),
        form: OAuth2PasswordRequestForm = Depends()
):
    user = crud.authenticate_user(db, form.username, form.password)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Incorrect username or password")
    data = {
        "access_token": security.create_access_token(subject=user.username),
        "token_type": "bearer",
    }
    return data
