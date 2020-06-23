from flask import render_template,request,Blueprint
from flaskblog.models import Post
main = Blueprint('main', __name__)

@main.route('/')
# route for index and home page
@main.route('/home')
def home():
    page = request.args.get('page',default=1,type=int)
    posts =Post.query.order_by(Post.date_posted.desc()).paginate(page = page ,per_page = 5)
    return render_template('home.html', posts= posts)
# another route for about page
@main.route('/about')
def about():
    return render_template('about.html',title='About')
    
    
@main.route('/stop')
def stop():
    return render_template('stop.html')
        
