import uuid
from app import db, bcrypt, create_app
from app.models.user import User
from app.models.role import Role

app = create_app('dev_pro')

with app.app_context():

    # Creating Admin
    admin_hash_password = bcrypt.generate_password_hash('toor')
    admin = User(public_id=str(uuid.uuid4()), first_name='John', last_name='Doe', username='johny', company='IWS', active=True, email_address='johny@doe.com', password=admin_hash_password)

    admin_role = Role(name='admin', description="Administrator to manage clients, feature requests and message to clients.", user=admin)

    # Creating Client
    client_hash_password = bcrypt.generate_password_hash('123456')
    client = User(public_id=str(uuid.uuid4()), first_name='William', last_name='Smith', username='william', company='Hooli', active=False, email_address='william@smith.com', password=client_hash_password)

    client_role = Role(name='client', description="Client can send feature requests and send messages.", user=client)

    # Executing queries
    db.session.add(admin)
    db.session.add(client)
    db.session.add(admin_role)
    db.session.add(client_role)
    db.session.commit()
