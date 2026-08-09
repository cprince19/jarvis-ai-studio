from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so metadata is available to migration tooling.
from app.models.render_job import RenderJob  # noqa: E402,F401
