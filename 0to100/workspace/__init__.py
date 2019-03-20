import os
from flask_dropzone import Dropzone
from flask import Flask
from flask_avatars import Avatars
from flask_mail import Mail, Message
from faker import Faker
import random
from PIL import Image
import click


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='CUproject',
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='nonamelascope@gmail.com',
        MAIL_PASSWORD='vai12121',
        MAIL_DEFAULT_SENDER=('Mason Lai', 'vai12121'),

    )

    avatars = Avatars(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from workspace import database

    from workspace import first_page
    app.register_blueprint(first_page.bp)
    from workspace import login_app, main_index, profile, upload, show,admin
    app.register_blueprint(login_app.bp)
    app.register_blueprint(main_index.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(show.bp)
    app.register_blueprint(admin.bp)
    basedir = os.path.abspath(os.path.dirname(__name__))
    app.config['AVATARS_SAVE_PATH'] = os.path.join(basedir, 'avatars')
    app.add_url_rule('/', endpoint='index')

    return app



def image_to_base64(img):
    '''
    convert image to base64.
    It is beacuse database save picture in string form
    '''
    from io import BytesIO
    import base64
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

app = create_app()
@app.cli.command()
def create_fake():
    from workspace.database import Database
    

    fake = Faker(locale='en_US')
    connect = Database()
    connect.Connect_to_db()
    gender=['No_show','Male','Female']
    user_list=[]
    post_list=[]
    comments_list=[]
    for i in range(0,300):
        username = fake.password(length=10, special_chars=True, digits=True, upper_case=False, lower_case=True)
        while connect.select_funcOne( """SELECT username FROM user WHERE username = '%s'""" %username) is not None:
            username = fake.password(length=10, special_chars=True, digits=True, upper_case=False, lower_case=True)

        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.ascii_safe_email()
        time_zone = random.randint(-12,13)
        if time_zone > 0:
            time_zone = str(time_zone)
        else:
            time_zone = str(time_zone)

        img = Image.new("RGB", (1280, 720), fake.safe_hex_color())
        base64_pic = image_to_base64(img)
        picture = bytes.decode(base64_pic)
        icon = ['default',picture]
        try:
            run = connect.Non_select("""INSERT INTO `user` ( `username`, \
                `password`, `first_name`, `last_name`, `email`, `vaildation`, `admin`) VALUES ( '%s', '%s', '%s', '%s', '%s', 'Y', 'N')\
                """%(username,password,first_name,last_name,email))
            run2 = connect.select_funcOne("""SELECT ID, username FROM user where username = '%s'""" %username)
            run3 = connect.Non_select("""INSERT INTO `Profile` (`ID`, `nick_name`, `gender`, `country`, `company`,`time_zone`, `status`, `background`, `icon`) 
                VALUES ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s')\
                ;"""%(run2['ID'],fake.last_name(),random.choice(gender),fake.country(),fake.company(),time_zone,fake.text(max_nb_chars=200, ext_word_list=None)\
                    ,fake.safe_hex_color(),random.choice(icon)))
            all_user =connect.select_funcALL( """SELECT ID FROM user """)
            for i in range(len(all_user)):
                user_list.append(all_user[i]['ID'])
            run4 = connect.Non_select("""INSERT INTO `picture` (`ID`, `auth_ID`,`title`,`caption`, \
            `picture`, `timestamp`) VALUES (NULL, '%s', '%s','%s','%s',\
            CURRENT_TIMESTAMP);"""%(random.choice(user_list),fake.text(max_nb_chars=20, ext_word_list=None),fake.text(max_nb_chars=200, ext_word_list=None),picture))
        except:
            pass
        if i%30 == 0:
            click.echo('Fake user :'+str(i/3)+'%')

    click.echo('Fake user : DONE!')
    for i in range(0,1000):
        all_post =connect.select_funcALL( """SELECT ID FROM picture """)
        for i in range(len(all_post)):
            post_list.append(all_post[i]['ID'])
        try:
            run6 = connect.Non_select("""INSERT INTO `love` (`love_ID`, `picture_ID`, `timestamp`) \
                VALUES (%s, %s, CURRENT_TIMESTAMP)"""%(int(random.choice(user_list)),int(random.choice(post_list))))
            run7 = connect.Non_select("""INSERT INTO `collection` (`picture_ID`, `collecter_ID`, `timestamp`) \
                VALUES (%s, %s, CURRENT_TIMESTAMP)"""%(int(random.choice(user_list)),int(random.choice(post_list))))
            run8 = connect.Non_select("""INSERT INTO `follow` (`following`, `follower`, `timestamp`) \
                VALUES (%s, %s, CURRENT_TIMESTAMP)"""%(int(random.choice(user_list)),int(random.choice(post_list))))
            run9 = connect.Non_select("""INSERT INTO `comments` (`ID`, `pic_ID`, `user_ID`, `comments`, `timestamp`)\
                 VALUES (NULL, %s, %s, '%s',CURRENT_TIMESTAMP);"""%(int(random.choice(user_list)),int(random.choice(post_list)),fake.text(max_nb_chars=299, ext_word_list=None)))
        except:
            pass

        all_comments =connect.select_funcALL( """SELECT ID  FROM comments """)
        for i in range(len(all_comments)):
            comments_list.append(all_comments[i]['ID'])


        try:
            run10 = connect.Non_select("""INSERT INTO `report` (`post_ID`, `reporter_ID`,\
             `timestamp`, `reason`, `Details`) VALUES (%s, %s, CURRENT_TIMESTAMP, '%s',\
              '%s')"""%(int(random.choice(post_list)),int(random.choice(user_list)),fake.text(max_nb_chars=20, ext_word_list=None),fake.text(max_nb_chars=20, ext_word_list=None)))
            run11 = connect.Non_select("""INSERT INTO `report_comment` (`comment_ID`, \
                `reporter_ID`, `status`) VALUES (%s, %s, 'exist')"""%(int(random.choice(comments_list)),int(random.choice(post_list))))


        except :
            pass


        if i%100 == 0:
            click.echo('Fake relationship :'+str(i/10)+'%')
    click.echo('Fake relationship : DONE!')

@app.cli.command()
def init_db():
    from workspace.database import Database
    connect = Database()
    connect.Connect_to_db()
    run = connect.Non_select("""DELETE FROM `user` where username != 'mason123'""")
    click.echo('DELETE FROM `user`')
    run = connect.Non_select("""DELETE FROM `report_comment` """)
    click.echo('DELETE FROM `report_comment`')
    run = connect.Non_select("""DELETE FROM `report` """)
    click.echo('DELETE FROM `report`')
    run = connect.Non_select("""DELETE FROM `Profile` where ID != 1435""")
    click.echo('DELETE FROM `Profile`')
    run = connect.Non_select("""DELETE FROM `picture` """)
    click.echo('DELETE FROM `picture`')
    run = connect.Non_select("""DELETE FROM `love` """)
    click.echo('DELETE FROM `love`')
    run = connect.Non_select("""DELETE FROM `follow` """)
    click.echo('DELETE FROM `follow`')
    run = connect.Non_select("""DELETE FROM `comments` """)
    click.echo('DELETE FROM `comments`')
    run = connect.Non_select("""DELETE FROM `collection` """)
    click.echo('DELETE FROM `collection`')
