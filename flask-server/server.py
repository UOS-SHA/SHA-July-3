from flask import Flask, request, jsonify
import pymysql
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
db = pymysql.connect(host='127.0.0.1', user='root', password='shajuly3', db='bulletboard', charset='utf8')
cursor = db.cursor()
jwt = JWTManager(app)


##############################################################################################################
# Utils
def log(text):
    print(f'[INTERNAL LOG] {text}')
##############################################################################################################



##############################################################################################################
# Main page
@app.route('/api/main')
@jwt_required(optional=True)
def default():
    cursor = db.cursor()
    try:
        identity = get_jwt_identity()
    except:
        identity = None

    ret = {
            "new_posts": [],
            "top_posts": [],
            "recent_comments": [],
            "logged_in_user_id": 0
           }

    if identity:
        ret['logged_in_user_id'] = identity['id']
    
    cursor.execute('SELECT user_id, title, creation_time, likes, id FROM posts ORDER BY id DESC LIMIT 20;')
    posts = cursor.fetchall()
    for post in posts:
        cursor.execute(f'SELECT username FROM users WHERE id={post[0]};')
        ret['new_posts'].append({
            'user_id': post[0],
            'username': cursor.fetchone(),
            'title': post[1],
            'creation_time': post[2],
            'likes': post[3],
            'id': post[4]
            })
    
    cursor.execute('SELECT user_id, title, likes, id FROM posts WHERE likes >= 5 ORDER BY likes DESC, id DESC LIMIT 5;')
    posts = cursor.fetchall()
    for post in posts:
        cursor.execute(f'SELECT username FROM users WHERE id={post[0]};')
        ret['top_posts'].append({
            'user_id': post[0],
            'username': cursor.fetchone(),
            'title': post[1],
            'likes': post[2],
            'id': post[3]
            })

    cursor.execute('SELECT id, post_id, content, user_id FROM comments ORDER BY id DESC limit 5;')
    comments = cursor.fetchall()
    for comment in comments:
        cursor.execute(f'SELECT username FROM users WHERE id={comment[3]}')
        ret['recent_comments'].append({
            'post_id': comment[1],
            'content': comment[2],
            'username': cursor.fetchone()
            })

    db.commit()
    return ret, 200
##############################################################################################################


##############################################################################################################
# User
def return_user_view(user, posts, comments):
    ret = {
            'id': user[0],
            'username': user[1],
            'school_year': user[2],
            'creation_date': user[3],
            'pw_hash': user[4],
            'additional_info': user[5],
            'posts': [],
            'comments': []
            }
    for post in posts:
        cursor.execute(f'SELECT id FROM posts WHERE title=\'{post[0]}\';')
        ret['posts'].append({
            'id': cursor.fetchone(),
            'title': post[0],
            'creation_time': post[1],
            'likes': post[2]
            })
    for comment in comments:
        ret['comments'].append({
            'original_post_id': comment[0],
            'content': comment[1],
            'creation_time': comment[2]
            })
    return jsonify(ret)

def get_posts_comments(user):
    cursor.execute(f'SELECT title, creation_time, likes FROM posts WHERE user_id={user[0]} ORDER BY id DESC LIMIT 5;')
    posts = cursor.fetchall()
    cursor.execute(f'SELECT post_id, content, created_at FROM comments WHERE user_id={user[0]} ORDER BY id DESC LIMIT 5;')
    comments = cursor.fetchall()
    return (posts, comments)

@app.route('/api/user/username/<string:username>', methods=['GET'])
def user_by_name(username):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM users WHERE username=\'{username}\';')
    user = cursor.fetchone()
    if not user:
        return {'error':'User not found.'}, 404
    posts, comments = get_posts_comments(user)
    db.commit()
    return return_user_view(user, posts, comments), 200

@app.route('/api/user/id/<int:id>', methods=['GET'])
def user_by_id(id):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM users WHERE id={id};')
    user = cursor.fetchone()
    if not user:
        return {'error':'User not found.'}, 404
    posts, comments = get_posts_comments(user)
    db.commit()
    return return_user_view(user, posts, comments), 200

@app.route('/api/user/add', methods=['POST'])
def add_user():
    cursor = db.cursor()
    data = request.get_json()
    log(f'User add request: {data}')
    if not data:
        log('User add request has failed')
        return jsonify({'error':'Invalid JSON data'}), 400

    username = data.get('username')
    school_year = data.get('school_year')
    pw_hash = data.get('pw_hash')
    additional_info = data.get('additional_info')

    if not (username and school_year and pw_hash):
        log('User add request has failed')
        return jsonify({'error':'Missing user data.'}), 400
    if not additional_info:
        cursor.execute(f'INSERT INTO users (username, school_year, pw_hash) VALUES (\'{username}\', {school_year}, \'{pw_hash}\');')
    else:
        cursor.execute(f'INSERT INTO users (username, school_year, pw_hash, additional_info) VALUES (\'{username}\', {school_year}, \'{pw_hash}\', \'{additional_info}\');')

    log('User add request was successful')
    db.commit()
    return jsonify({'message':'User added successfully.'}), 201

@app.route('/api/user/login', methods=['POST'])
def login():
    cursor = db.cursor()
    data = request.get_json()
    username = data.get('username')
    pw_hash = data.get('pw_hash')
    
    cursor.execute('SELECT pw_hash, id FROM users WHERE username=\'{username}\';')
    data = cursor.fetchone()

    db.commit()
    if data and pw_hash == data[0]:
        return jsonify({'token': create_access_token(identity={'id': data[1]})}), 201
    return jsonify({'error':'Invalid credentials.'}), 401
##############################################################################################################



##############################################################################################################
# Post
def return_post_view(post, comments):
    ret = {
            'id': post[0],
            'user_id': post[1],
            'title': post[2],
            'content': post[3],
            'creation_time': post[4],
            'likes': post[5],
            'username': None,
            'comments': []
            }
    cursor.execute(f'SELECT username FROM users WHERE id={post[1]};')
    ret['username'] = cursor.fetchone()

    for comment in comments:
        cursor.execute(f'SELECT username FROM users WHERE id={comment[0]};')
        ret['comments'].append({
            'user_id': comment[0],
            'username': cursor.fetchone(),
            'content': comment[1],
            'creation_time': comment[2]
            })
    return jsonify(ret)
    
def get_comments(post):
    cursor.execute(f'SELECT user_id, content, created_at FROM comments WHERE post_id={post[0]} ORDER BY id;')
    db.commit()
    return cursor.fetchall()

@app.route('/api/post/<int:post_id>', methods=['GET'])
def post(post_id):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM posts WHERE id={post_id};')
    post = cursor.fetchone()
    if not post:
        return jsonify({'error':'Post not found.'}), 404
    db.commit()
    return return_post_view(post, get_comments(post)), 200

@app.route('/api/post/add', methods=['POST'])
def add_post():
    cursor = db.cursor()
    data = request.get_json()
    print(f'Post add request: {data}')
    if not data:
        return jsonify({'error':'Invalid JSON data'}), 400

    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')

    db.commit()
    if not (user_id and title and content):
        return jsonify({'error':'Missing post data.'}), 400
    cursor.execute(f'INSERT INTO posts (user_id, title, content) VALUES ({user_id}, \'{title}\', \'{content}\');')
    return jsonify({'message':'Post added successfully'}), 201



if __name__ == "__main__":
    app.run(host='0.0.0.0')
