from jobplus.models import db, User

def add_admin():
    try:
        user=User(email='admin@admin.com',password='111111',role=30)
        db.session.add(user)
        db.session.commit()
        print('Add success')
    except Exception as e:
        print(e)
        print('Add failed')

