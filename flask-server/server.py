from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
db = pymysql.connect(host='127.0.0.1', user='root', password='shajuly3', db='bulletboard', charset='utf8')
cursor = db.cursor()


@app.route('/')
def default():
    return "<h1 style='color:blue'>Hello, world!</h1>"



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
        ret['posts'].append({
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


@app.route('/user/username/<string:username>', methods=['GET'])
def user_by_name(username):
    cursor.execute(f'SELECT * FROM users WHERE username=\'{username}\';')
    user = cursor.fetchone()
    if not user:
        return {'error':'User not found.'}, 404
    posts, comments = get_posts_comments(user)
    return return_user_view(user, posts, comments), 200

@app.route('/user/id/<int:id>', methods=['GET'])
def user_by_id(id):
    cursor.execute(f'SELECT * FROM users WHERE id={id};')
    user = cursor.fetchone()
    if not user:
        return {'error':'User not found.'}, 404
    posts, comments = get_posts_comments(user)
    return return_user_view(user, posts, comments), 200

@app.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()
    print(f'User add request: {data}')
    if not data:
        return jsonify({'error':'Invalid JSON data'}), 400

    username = data.get('username')
    school_year = data.get('school_year')
    pw_hash = data.get('pw_hash')
    additional_info = data.get('additional_info')

    if not (username and school_year and pw_hash):
        return jsonify({'error':'Missing user data.'}), 400
    if not additional_info:
        cursor.execute(f'INSERT INTO users (username, school_year, pw_hash) VALUES (\'{username}\', {school_year}, \'{pw_hash}\');')
    else:
        cursor.execute(f'INSERT INTO users (username, school_year, pw_hash, additional_info) VALUES (\'{username}\', {school_year}, \'{pw_hash}\', \'{additional_info}\');')
    return jsonify({'message':'User added successfully.'}), 201
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
            'comments': []
            }
    for comment in comments:
        ret['comments'].append({
            'user_id': comment[0],
            'content': comment[1],
            'creation_time': comment[2]
            })
    return jsonify(ret)
    

def get_comments(post):
    cursor.execute(f'SELECT user_id, content, created_at FROM comments WHERE post_id={post[0]} ORDER BY id;')
    return cursor.fetchall()

@app.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
    cursor.execute(f'SELECT * FROM posts WHERE id={post_id};')
    post = cursor.fetchone()
    if not post:
        return jsonify({'error':'Post not found.'}), 404
    return return_post_view(post, get_comments(post)), 200

@app.route('/post/add', methods=['POST'])
def add_post():
    data = request.get_json()
    print(f'Post add request: {data}')
    if not data:
        return jsonify({'error':'Invalid JSON data'}), 400

    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')

    if not (user_id and title and content):
        return jsonify({'error':'Missing post data.'}), 400
    cursor.execute(f'INSERT INTO posts (user_id, title, content) VALUES ({user_id}, \'{title}\', \'{content}\');')
    return jsonify({'message':'Post added successfully'}), 201



if __name__ == "__main__":
    app.run(host='0.0.0.0')
