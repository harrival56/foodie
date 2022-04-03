from app import db
from models import User, Menu, Favorite


db.drop_all()
db.create_all()


# u1 = User(email="example@yahoo.com", username="harri", password="mypassword")
# u2 = User.signup("example2@yahoo.com", "harr1", "mypassword")
# db.session.add_all([u1, u2])
# db.session.commit()


# m1 = Menu(day="monday", time="lunch", title="okpa", user_id=u1.id)
# m2 = Menu(day="monday", time="dinner", title="akam", user_id=u1.id)
# m3 = Menu(day="monday", time="dinner", title="azamkpa", user_id=u2.id)
# db.session.add_all([m1, m2, m3])
# db.session.commit()

# f1 = Favorite(title="first title", image="no image", user_id=u1.id)
# f2 = Favorite(title="first title1", image="no image1", user_id=u1.id)
# f3 = Favorite(title="first title2", image="no image2", user_id=u2.id)
# db.session.add_all([f1,f2,f3])
# db.session.commit()
