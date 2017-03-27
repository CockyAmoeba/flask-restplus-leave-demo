from app import db
from app.modules.users.models import User
from app.modules.roles.models import Role


def setup():
    adminUser = User(email='admin@admin.com',
                     username='admin',
                     first_name='Omni',
                     last_name='Potent',
                     password='admin@password')

    db.session.add(adminUser)
    testUser = User(email='test@test.com',
                    username='test',
                    first_name='Chaos',
                    last_name='Monkey',
                    password='password')

    db.session.add(testUser)
    role = Role(name='Admin',
                description='All powerful')
    db.session.add(role)
    db.session.commit()

if __name__ == '__main__':
    setup()