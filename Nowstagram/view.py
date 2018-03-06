# -*- encoding=UTF-8 -*-
from Nowstagram import app, db, login_manager
from Nowstagram.models import User, Comment, Image
from flask import redirect, render_template, request, flash, get_flashed_messages, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
import random, hashlib, json, uuid, os


@app.route('/')
def index():
    #users = User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items
    paginate = Image.query.order_by('id desc').paginate(page=1, per_page=10)
    length = Image.query.order_by('id desc').first().id
    print
    return render_template('index.html', images=paginate.items, has_next=paginate.has_next, j=0, len=length)


@app.route('/index/<int:page>/<int:per_page>/')
def index_ext(page, per_page):
    paginate = Image.query.order_by('id desc').paginate(page=page, per_page=per_page)
    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        comments_user = []
        comments_userid=[]
        for i in image.comments:
            comments.append(i.content)
            comments_user.append(i.user.username)
            comments_userid.append(i.user.id)
        imgvo = {'image_id': image.id, 'url': image.url, 'comments': comments, 'create_time': str(image.created_time),'comments_user':comments_user,
                 'comments_userid':comments_userid,'comment_length': len(image.comments), 'user_id': image.user_id,
                 'username': image.user.username, 'head_url': image.user.head_url}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


@app.route('/profile/<int:userid>/')
@login_required
def profile(userid):
    user = User.query.get(userid)
    if user == None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=userid).paginate(page=1, per_page=3)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


@app.route('/image/<int:imag_id>/')
def image(imag_id):
    image = Image.query.get(imag_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image, comments=image.comments)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_image(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    map = {'has_next': paginate.has_next}
    images = []
    for m in paginate.items:
        imgvo = {'id': m.id, 'url': m.url, 'comment_count': len(m.comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)




@app.route('/base/')
def base():
    return render_template("base.html")


def flash_msg(target, msg, category):
    if msg != None :
        flash(msg, category=category)
    return redirect(target)


@app.route('/reg/', methods={'POST', 'GET'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    username_test = User.query.filter_by(username=username).first()
    if username_test != None :
        return flash_msg('/reglogin', u'用户名已存在', 'relogin')
    if username == '' or password == '':
        return flash_msg('/reglogin', u'用户名或密码不能为空', 'relogin')
    # 特殊字符 和 敏感词 检测
    salt = ''.join(random.sample('0123456789abcdefghijklmnopgrstABCDEFGHIJKLMN', 7),)
    md5 = hashlib.md5()
    md5.update(password+salt)
    password = md5.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    next = request.values.get('next')
    if next!=None and next.startswith('/') :
        return redirect(next)
    return redirect('/')


@app.route('/login/', methods={'POST', 'GET'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    if username == '' or password == '':
        return flash_msg('/reglogin', u'用户名或密码不能为空', 'relogin')
    user = User.query.filter_by(username=username).first()
    if user == None :
        return flash_msg('/reglogin', u'用户名或密码出错', 'relogin')
    md5 = hashlib.md5()
    salt = user.salt
    md5.update(password + salt)
    if md5.hexdigest() != user.password:
        return flash_msg('/reglogin', u'用户名或密码出错', 'relogin')
    login_user(user)
    next = request.values.get('next')
    if next!=None and next.startswith('/') :
        return redirect(next)
    return redirect('/')


@app.route('/reglogin/')
def reglogin(msg=''):
    if current_user.is_authenticated:
        return redirect('/')
    for m in get_flashed_messages(with_categories=False, category_filter=['relogin']):
        msg += m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


def save_to_local(file, filename):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, filename))
    return '/image/' + filename


@login_required
@app.route('/upload/', methods={'post'})
def upload():
    file = request.files['file']
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.')[-1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-' , '')+'.'+file_ext
        url = save_to_local(file,file_name)
        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()
    return redirect('/profile/' + str(current_user.id))


@app.route('/image/<image_id>')
def view_image(image_id):
    return send_from_directory((app.config['UPLOAD_DIR']), image_id)


@login_required
@app.route('/addcomment/', methods={'post'})
def addcomment():
    image_id = int(request.values['image_id'])
    content = request.values['content']
    comment = Comment(content, current_user.id, image_id)
    db.session.add(comment)
    db.session.commit()
    map = {"code": 0, "id": comment.id, "content": comment.content
           , "user_id": comment.user_id, "username": comment.user.username}
    return json.dumps(map)


@login_required
@app.route('/addindexcomment/', methods={'post'})
def addindexcomment():
    image_id = int(request.values['image_id'])
    content = request.values['content']
    comment = Comment(content, current_user.id, image_id)
    print image_id, content
    db.session.add(comment)
    db.session.commit()
    map = {"code": 0, "content": comment.content, "user_id": comment.user.id,
            "username": comment.user.username}
    #return json.dumps(map)
    return redirect('/')
