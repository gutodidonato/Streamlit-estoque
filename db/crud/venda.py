from ..db import SessionLocal
from ..models import Venda


def create_venda():
    db = SessionLocal()
    