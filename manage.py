# -*- encoding=UTF-8 -*-
from Nowstagram import db, app
from flask_script import Manager
from Nowstagram.models import User, Image, Comment
import random

import random
manage = Manager(app)


def get_image():
    return 'https://www.gravatar.com/avatar/fc35e0f354c03' + str(random.randint(0, 1000)) + '0cf6db5b65c86ef5905c?s=328&d=identicon&r=PG&f=1'
print get_image()


@manage.command
def database_init():
    db.drop_all()
    db.create_all()
    for i in range(100):
        db.session.add(User('用户'+str(i+1), 'pw'+str(i)))
        for j in range(10):
            db.session.add(Image(get_image(), i + 1))
            for k in range(3):
                db.session.add(Comment(('This is a Comment'+str(k)), i+1, 1+10*i+j))

    db.session.commit()
    print 1, User.query.all()
    print 2, Image.query.all()
    user = User.query.get(1)
    print 3, user.images.all()
    image = Image.query.first()
    print 4, image.user.username, image.user.head_url
    print 5, Image.query.limit(10).all()

if __name__ == '__main__':
    manage.run()
