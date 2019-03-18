import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from workspace.database import *

import datetime as dt

from workspace.login_app import login_required

bp = Blueprint('main_index', __name__,url_prefix='/main_index')

@bp.route('/',methods=('GET', 'POST'))

def main_page():

    connect = Database()
    connect.Connect_to_db()

    new_pic = connect.select_funcALL("""SELECT `title`,`ID`,`picture`,`auth_ID` FROM `picture` ORDER BY`timestamp` DESC LIMIT 9""")

    new_row=[]
    new_like=[]
    new_coll=[]
    new_like_row=[]
    new_coll_row=[]
    for i in range(len(new_pic)):
        pic_like = connect.select_funcOne("""SELECT COUNT(*) FROM `love` WHERE `picture_ID` = %s"""%new_pic[i]['ID'])
        new_like.append(pic_like['COUNT(*)'])
        pic_collect = connect.select_funcOne("""SELECT COUNT(*) FROM `collection` WHERE `picture_ID` = %s"""%new_pic[i]['ID'])
        new_coll.append(pic_collect['COUNT(*)'])
    for i in range(0,len(new_pic),3):
        new_row.append(new_pic[i:i+3])
        new_like_row.append(new_like[i:i+3])
        new_coll_row.append(new_coll[i:i+3])


    pic_like_pop = connect.select_funcALL("""SELECT `picture_ID`,COUNT(*) ,picture.timestamp \
        FROM `love` join picture on picture_ID = id GROUP BY `picture_ID`""" )

    pic_collect = connect.select_funcALL("""SELECT `picture_ID`,COUNT(*) FROM `collection` GROUP BY `picture_ID`""")

    for i in range(len(pic_like_pop)):

        for a in range(len(pic_collect)):
             if pic_like_pop[i]['picture_ID'] == pic_collect[a]['picture_ID']:
                pic_like_pop[i]['collection'] = pic_collect[a]['COUNT(*)']


    for i in range(len(pic_like_pop)):
        db = str(pic_like_pop[i]['timestamp'])
        a = dt.datetime.now()
        b = dt.datetime(int(db[0:4]),int(db[5:7]),int(db[8:10]),int(db[11:13]),int(db[14:16]),int(db[17:19]))

        TD = (a-b).total_seconds()


        pic_like_pop[i]['timestamp'] = int(TD/60/60)
        try:
            pic_like_pop[i]['Score'] = (pic_like_pop[i]['COUNT(*)']+pic_like_pop[i]['collection']) / ( pic_like_pop[i]['timestamp']+2)**1.8

        except KeyError:

            pic_like_pop[i]['Score'] = pic_like_pop[i]['COUNT(*)'] / ( pic_like_pop[i]['timestamp']+2)**1.8
            
    def myFunc(e):
      return e['Score']

    pic_like_pop.sort(key=myFunc,reverse=True)


    if len(pic_like_pop) > 9:
        for i in range(9):
            picture = connect.select_funcOne("""SELECT `picture` FROM `picture` WHERE `ID`=%s"""%pic_like_pop[i]['picture_ID'])
            pic_like_pop[i]['picture'] = picture['picture']
    else:
        for i in range(len(pic_like_pop)):
            picture = connect.select_funcOne("""SELECT `picture` FROM `picture` WHERE `ID`=%s"""%pic_like_pop[i]['picture_ID'])
            pic_like_pop[i]['picture'] = picture['picture']

    pop_like_row=[]
    for i in range(0,len(pic_like_pop),3):
        pop_like_row.append(pic_like_pop[i:i+3])

    if not not g.user:
        follow_pic = connect.select_funcALL("""SELECT picture.ID,picture.title,picture.picture from picture LEFT JOIN 
            follow ON picture.auth_ID=follow.following WHERE follow.follower = %s ORDER BY `picture`.`timestamp` DESC"""%g.user['ID'])
        if len(follow_pic) >9:
            for i in range(9):
                like =  connect.select_funcOne("""SELECT COUNT(*) FROM `love` WHERE `picture_ID` = %s"""%follow_pic[i]['ID'])
                collection =  connect.select_funcOne("""SELECT COUNT(*) FROM `collection` WHERE `picture_ID` = %s"""%follow_pic[i]['ID'])
                follow_pic[i]['like']= like['COUNT(*)']
                follow_pic[i]['collection'] = collection['COUNT(*)']

        else:
            for i in range(len(follow_pic)):
                like =  connect.select_funcOne("""SELECT COUNT(*) FROM `love` WHERE `picture_ID` = %s"""%follow_pic[i]['ID'])
                collection =  connect.select_funcOne("""SELECT COUNT(*) FROM `collection` WHERE `picture_ID` = %s"""%follow_pic[i]['ID'])
                follow_pic[i]['like']= like['COUNT(*)']
                follow_pic[i]['collection'] = collection['COUNT(*)']

        follow_row =[]
        for i in range(0,len(follow_pic),3):
            follow_row.append(follow_pic[i:i+3])

        if len(follow_row) >3 :
            follow_loop = 3
        else:
            follow_loop = len(follow_row)

    return render_template('main_index/main_page.html',row=new_row,len=len,\
        new_like_row=new_like_row,new_coll_row=new_coll_row,pop_like_row=pop_like_row,follow_row=follow_row,follow_loop=follow_loop)



@bp.route('/Newest', defaults={'page':1},methods=('GET', 'POST'))
@bp.route('/Newest<int:page>',methods=('GET', 'POST'))
def Newest_page(page):

    connect = Database()
    connect.Connect_to_db()
    Newest =  connect.select_funcALL("""SELECT `ID`,`title` ,`picture`,`timestamp`FROM `picture` ORDER BY `timestamp` DESC""")


    for i in range(len(Newest)):
        db = str(Newest[i]['timestamp'])
        a = dt.datetime.now()
        b = dt.datetime(int(db[0:4]),int(db[5:7]),int(db[8:10]),int(db[11:13]),int(db[14:16]),int(db[17:19]))

        TD = (a-b).total_seconds()

        if TD < 59:
            Newest[i]['timestamp'] = str(int(TD))+'s ago'
        elif TD < 3599:
            Newest[i]['timestamp'] = str(int(TD/60))+' mins ago'
        elif TD <86399:
            Newest[i]['timestamp'] = str(int(TD/60/60))+' hours ago'
        elif TD <31535999:
            Newest[i]['timestamp'] = str(int(TD/60/60/24))+' days ago'
        else:
            Newest[i]['timestamp'] = str(int(TD/60/60/24/365))+' years ago'

    for x in range(len(Newest)):
        like = connect.select_funcOne("""select count(*) from love where picture_ID = %s"""%Newest[x]['ID'])
        Newest[x]['like'] = like['count(*)']

        collection = connect.select_funcOne("""select count(*) from collection where picture_ID = %s"""%Newest[x]['ID'])
        Newest[x]['collection'] = collection['count(*)']

    paginate =[]
    row = []
    for i in range(0,len(Newest),5):
        row.append(Newest[i:i+5])

    for i in range(0,len(row),4):
        paginate.append(row[i:i+4])

    if page > len(paginate):
        page = 1

    return render_template('main_index/Newest_page.html',paginate=paginate,page=page,len=len)


@bp.route('/popular', defaults={'page':1},methods=('GET', 'POST'))
@bp.route('/popular<int:page>',methods=('GET', 'POST'))
def pop_page(page):

    connect = Database()
    connect.Connect_to_db()



    pic_like_pop = connect.select_funcALL("""SELECT `picture_ID`,COUNT(*) ,picture.timestamp \
        FROM `love` join picture on picture_ID = id GROUP BY `picture_ID`""" )

    pic_collect = connect.select_funcALL("""SELECT `picture_ID`,COUNT(*) FROM `collection` GROUP BY `picture_ID`""")

    for i in range(len(pic_like_pop)):

        for a in range(len(pic_collect)):
             if pic_like_pop[i]['picture_ID'] == pic_collect[a]['picture_ID']:
                pic_like_pop[i]['collection'] = pic_collect[a]['COUNT(*)']


    for i in range(len(pic_like_pop)):
        db = str(pic_like_pop[i]['timestamp'])
        a = dt.datetime.now()
        b = dt.datetime(int(db[0:4]),int(db[5:7]),int(db[8:10]),int(db[11:13]),int(db[14:16]),int(db[17:19]))

        TD = (a-b).total_seconds()


        pic_like_pop[i]['timestamp_C'] = int(TD/60/60)
        try:
            pic_like_pop[i]['Score'] = (pic_like_pop[i]['COUNT(*)']+pic_like_pop[i]['collection']) / ( pic_like_pop[i]['timestamp_C']+2)**1.8

        except KeyError:

            pic_like_pop[i]['Score'] = pic_like_pop[i]['COUNT(*)'] / ( pic_like_pop[i]['timestamp_C']+2)**1.8
    def myFunc(e):
      return e['Score']

    pic_like_pop.sort(key=myFunc,reverse=True)

    for i in range(len(pic_like_pop)):
            picture = connect.select_funcOne("""SELECT `picture`,title FROM `picture` WHERE `ID`=%s"""%pic_like_pop[i]['picture_ID'])
            pic_like_pop[i]['picture'] = picture['picture']
            pic_like_pop[i]['title'] = picture['title']



    for i in range(len(pic_like_pop)):
        db = str(pic_like_pop[i]['timestamp'])
        a = dt.datetime.now()
        b = dt.datetime(int(db[0:4]),int(db[5:7]),int(db[8:10]),int(db[11:13]),int(db[14:16]),int(db[17:19]))

        TD = (a-b).total_seconds()

        if TD < 59:
            pic_like_pop[i]['timestamp'] = str(int(TD))+'s ago'
        elif TD < 3599:
            pic_like_pop[i]['timestamp'] = str(int(TD/60))+' mins ago'
        elif TD <86399:
            pic_like_pop[i]['timestamp'] = str(int(TD/60/60))+' hours ago'
        elif TD <31535999:
            pic_like_pop[i]['timestamp'] = str(int(TD/60/60/24))+' days ago'
        else:
            pic_like_pop[i]['timestamp'] = str(int(TD/60/60/24/365))+' years ago'

    for x in range(len(pic_like_pop)):
        like = connect.select_funcOne("""select count(*) from love where picture_ID = %s"""%pic_like_pop[x]['picture_ID'])
        pic_like_pop[x]['like'] = like['count(*)']

        collection = connect.select_funcOne("""select count(*) from collection where picture_ID = %s"""%pic_like_pop[x]['picture_ID'])
        pic_like_pop[x]['collection'] = collection['count(*)']

    paginate =[]
    row = []
    for i in range(0,len(pic_like_pop),5):
        row.append(pic_like_pop[i:i+5])

    for i in range(0,len(row),4):
        paginate.append(row[i:i+4])


    if page > len(paginate):
        page = 1

    return render_template('main_index/pop_page.html',paginate=paginate,page=page,len=len)


@bp.route('/follow', defaults={'page':1},methods=('GET', 'POST'))
@bp.route('/follow<int:page>',methods=('GET', 'POST'))
@login_required
def follow_page(page):

    connect = Database()
    connect.Connect_to_db()
    follow = connect.select_funcALL(""" SELECT picture.ID,picture.title,picture.picture \
            ,picture.timestamp , picture.auth_ID from picture LEFT JOIN follow ON \
            picture.auth_ID=follow.following WHERE follow.follower = %s ORDER BY `picture`.`timestamp` DESC"""%g.user['ID'])

    for i in range(len(follow)):
        like =  connect.select_funcOne("""SELECT COUNT(*) FROM `love` WHERE `picture_ID` = %s"""%follow[i]['ID'])
        collection =  connect.select_funcOne("""SELECT COUNT(*) FROM `collection` WHERE `picture_ID` = %s"""%follow[i]['ID'])
        auth_name = connect.select_funcOne("""SELECT `nick_name` FROM `Profile` WHERE ID =%s"""%follow[i]['auth_ID'])
        follow[i]['like']= like['COUNT(*)']
        follow[i]['collection'] = collection['COUNT(*)']
        follow[i]['auth_name'] = auth_name['nick_name']
        db = str(follow[i]['timestamp'])
        a = dt.datetime.now()
        b = dt.datetime(int(db[0:4]),int(db[5:7]),int(db[8:10]),int(db[11:13]),int(db[14:16]),int(db[17:19]))

        TD = (a-b).total_seconds()

        if TD < 59:
            follow[i]['timestamp'] = str(int(TD))+'s ago'
        elif TD < 3599:
            follow[i]['timestamp'] = str(int(TD/60))+' mins ago'
        elif TD <86399:
            follow[i]['timestamp'] = str(int(TD/60/60))+' hours ago'
        elif TD <31535999:
            follow[i]['timestamp'] = str(int(TD/60/60/24))+' days ago'
        else:
            follow[i]['timestamp'] = str(int(TD/60/60/24/365))+' years ago'

    paginate =[]
    row = []
    for i in range(0,len(follow),5):
        row.append(follow[i:i+5])

    for i in range(0,len(row),4):
        paginate.append(row[i:i+4])


    if page > len(paginate):
        page = 1

    if not paginate:
        return redirect(url_for('main_index.main_page'))

    return render_template('main_index/follow_page.html',paginate=paginate,page=page,len=len)