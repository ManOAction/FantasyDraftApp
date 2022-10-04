from app import db
from app.models import Player

RecordsDeleted = Player.query.delete()
db.session.commit()

print(f"""We remmoved {RecordsDeleted} from the Database.""")


print('We\'re done here.')