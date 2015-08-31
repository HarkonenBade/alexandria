import datetime
import functools

from flask import (abort, g, jsonify, redirect,
                   request, render_template, url_for)

from . import app, db


def render(template, **kwargs):
    if hasattr(g, "user"):
        kwargs['user'] = db.obj_to_dict(g.user)

    kwargs['urls'] = {'root': url_for('root'),
                      'add_quote': url_for('add_quote'),
                      'add_user': url_for('add_user'),
                      'login': url_for('login')}
    return render_template(template, **kwargs)


@app.before_request
def before_request():
    g.sesh = db.Session()


@app.teardown_request
def teardown_request(exception):
    sesh = getattr(g, 'sesh', None)
    if sesh is not None:
        sesh.close()


def token_check(admin=False):
    def wrapper(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            if 'token' not in request.cookies:
                return redirect(url_for('login'))

            user = db.check_token(g.sesh,
                                  request.cookies['token'],
                                  admin)

            if user is None:
                if admin:
                    if db.check_token(g.sesh,
                                      request.cookies['token'],
                                      False):
                        abort(401)
                    else:
                        return redirect(url_for('login'))
                else:
                    return redirect(url_for('login'))

            g.user = user
            return func(*args, **kwargs)
        return wrap
    return wrapper


@app.route("/login")
def login():
    return render("login.html")


@app.route("/user", methods=['POST', 'GET'])
@token_check(admin=True)
def add_user():
    if request.method == "POST":
        user = db.User()
        user.name = request.form['name']
        user.admin = 'admin' in request.form
        user.token = db.new_token()
        user.created_by = g.user.id
        g.sesh.add(user)
        g.sesh.commit()
        return render("user_created.html", new_user=db.obj_to_dict(user))
    else:
        return render("add_user.html")


@app.route("/quote", methods=['POST'])
@token_check()
def add_quote():
    if('text' not in request.json or
       'person' not in request.json or
       request.json['text'] == "" or
       request.json['person'] == ""):
        abort(422)

    quote = db.Quote()
    quote.text = request.json['text']
    quote.person = request.json['person']
    quote.date_added = datetime.datetime.now()
    quote.submitter = g.user.id
    g.sesh.add(quote)
    g.sesh.commit()
    return jsonify({'id': quote.id}), 201


@app.route("/", methods=['GET'])
@token_check()
def root():
    query = (g.sesh.query(db.Quote, db.User).
             join(db.User))

    if "user" in request.args:
        query = query.filter(db.User.id == int(request.args['user']))

    result = query.order_by(db.Quote.id.desc()).all()

    quotes = [{'id': q.id,
               'text': q.text,
               'person': q.person,
               'date': q.date_added.isoformat(),
               'submitter': {'id': u.id,
                             'name': u.name}}
              for q, u in result]

    return render("index.html", quotes=quotes)
