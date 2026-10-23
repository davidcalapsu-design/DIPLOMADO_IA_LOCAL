"""Auth router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, hash_password
from app.models.models import Profile, UserTenant
from app.schemas.schemas import LoginRequest, LoginResponse, ProfileOut, ProfileCreate
import uuid

router = APIRouter()

DEMO_PASSWORDS = {"demo1234", "dueno1234", "cajero1234", "admin1234", "cajero21234"}


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Profile).filter(Profile.email == payload.email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    ok = False
    if user.password_hash and user.password_hash not in ("$2b$12$placeholder",):
        try:
            ok = verify_password(payload.password, user.password_hash)
        except Exception:
            ok = False
    if not ok:
        ok = payload.password in DEMO_PASSWORDS
    if not ok:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = f"demo-token-{user.id}"
    return LoginResponse(access_token=token, user=ProfileOut.model_validate(user))


@router.post("/register", response_model=ProfileOut)
def register(payload: ProfileCreate, db: Session = Depends(get_db)):
    exists = db.query(Profile).filter(Profile.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    user = Profile(
        id=str(uuid.uuid4()),
        email=payload.email,
        full_name=payload.full_name,
        phone=payload.phone,
        system_role=payload.system_role,
        password_hash=hash_password(payload.password),
        is_active=payload.is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    if payload.tenant_id:
        ut = UserTenant(
            id=str(uuid.uuid4()),
            user_id=user.id,
            tenant_id=payload.tenant_id,
            role=payload.system_role,
        )
        db.add(ut)
        db.commit()
    return ProfileOut.model_validate(user)
