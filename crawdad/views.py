""" Cornice services.
"""
from cornice import Service
from models import DBSession, User, Message
import json
from pyramid.httpexceptions import HTTPUnauthorized
from datetime import datetime

crawdad_service = Service(name='Crawdad', path='/',
                          description="Root of Big Infosys (Crawsys) REST API")

messages_service = Service(name='MessagesRoot', path='/messages',
                           description="Create and see list of messages.")

users_create_service = Service(name='UserCreation', path='/users/',
                               description="Create users.")

users_service = Service(name='UserCreation', path='/users/{uid}',
                        description="Set settings for user.")


@crawdad_service.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}


@messages_service.get()
def get_messages(request):
    messages = DBSession.query(Message).all()
    messages_list = []
    for message in messages:
        messages_list.append(message.to_dict())
    return {"messages": messages_list}


#@crawsys.post(validators=[valid_body('username'), valid_user])
@messages_service.put()
def create_message(request):
    data = json.loads(request.body)
    cur_user = data['username']
    user_id = DBSession.query(User).filter_by(uid=cur_user).one().id
    data["owner_id"] = user_id
    target_query = DBSession.query(User).filter(
        User.uid == cur_user)
    if target_query.count() > 0:
        target = target_query.first()
        if target.uid == cur_user or cur_user.admin:
            m = Message.from_dict(data)
            #m = Message()
            DBSession.add(m)
            DBSession.commit()
            return m.to_dict()
    raise HTTPUnauthorized


@users_create_service.get()
def get_users(request):
    users = DBSession.query(User).all()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return {"users": users_list}


@users_create_service.put()
def create_user(request):
    data = json.loads(request.body)
    new_user = User(
        uid=data['username']
    )
    new_user.created_at = datetime.now()
    if DBSession.query(User).filter(User.name == new_user.name).count() > 0:
        raise HTTPUnauthorized()
    DBSession.add(new_user)
    DBSession.commit()
    return {"success": True}
