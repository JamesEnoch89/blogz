from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "abc"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(46))
    content = db.Column(db.String(140))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def is_valid(self):
        if self.title and self.content:
            return True
        else:
            return False



@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()

    return render_template('index.html',
          title="BLOG",
          blogs=blogs,
          )

@app.route('/new_post', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':

        blog_name = request.form['blog']
        blog_content = request.form['content']

        new_blog = Blog(blog_name, blog_content)

        if new_blog.is_valid():
            db.session.add(new_blog)
            db.session.commit()

            url = "/single_template?id=" + str(new_blog.id)

            return redirect(url)

        else:
            flash("Your posts must contain content AND a title. Please try again!")

            return render_template('new_post.html',
                                    blog_name=blog_name,
                                    blog_content=blog_content)


    else:
        return render_template('new_post.html')



@app.route('/single_template', methods=['GET'])
def single_template():

    blog_id = request.args.get('id')
    blogs = Blog.query.filter_by(id=blog_id).first()

    return render_template('single_template.html', blogs=blogs)


if __name__ == "__main__":
    app.run()