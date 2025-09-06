# Import all the models, so that Base has them before being imported by Alembic
from app.db.base_class import Base
from app.models.match import Match
from app.models.history import History
from app.models.ah_data import AHData
from app.models.ou_data import OUData
from app.models.user import User
