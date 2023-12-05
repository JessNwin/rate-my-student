# TODO: Implement school email verification

# TODO: Implement school email verification
from sqlalchemy import func
from app import app, db, load_user
from app.models import User, Student, Professor, Recommendation, Rating
from app.forms import SignUpForm, SignInForm
from flask import flash, jsonify, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

# sign-in functionality
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    signInForm = SignInForm()

    if signInForm.validate_on_submit():
        userID = signInForm.id.data
        userPass = signInForm.password.data.encode('utf-8')

        checkUser = load_user(userID)
        if checkUser == None:
            return ('<p>No user found</p>')
        

        if bcrypt.checkpw(userPass, checkUser.password):
            login_user(checkUser)
            print("match")
            print("CurrentID: " + current_user.id)

            return redirect('/users/search')
        else:
            return ('<p>Incorrect Password</p>')
    return render_template('signin.html', form=signInForm)

# signup functionality
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    signUp = SignUpForm()

    if signUp.validate_on_submit():
        password = signUp.password.data
        password_confirm = signUp.password_confirm.data

        existing_user = load_user(signUp.id.data)
        if existing_user:
            flash('User already exists, Please choose a different one', 'error')
            return redirect(url_for('users_signup'))

        if password == password_confirm:
            hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            newUser = User(id=signUp.id.data,
                           full_name=signUp.full_name.data,
                           email=signUp.email.data,
                           password=hashedPass,
                           type='student')
            db.session.add(newUser)
            db.session.commit()
            return redirect('/users/signin')
        else:
            return ('<p>Password didn\'t match confirmation</p>')
        
    return render_template('signup.html', form=signUp)

# Signout functionality
@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))

 #Student/Professor search functionality
@login_required
@app.route('/users/search')
def search_page():
    print(isinstance(current_user, Student))
    return render_template('search.html')

#Search suggestion logic for main search bar
@app.route('/search-suggestions')
def search_suggestions():
    
    query = request.args.get('q', '')
    if query:
        # TODO?: Change this to show all students, in CSS make the window show 5 and a scroll bar
        users = User.query.filter(User.full_name.like(f"%{query}%")).limit(10).all()
        suggestions = [{'name': user.full_name, 'id': user.id} for user in users]
    else:
        suggestions = []

    return jsonify(suggestions)

# this is the route to try to include the list of top- rated students 
@app.route('/professor/home', methods=['GET'])
@login_required
def professor_home():
    if current_user.type == 'professor':
        # Calculate the average rating for each student
        students = Student.query.all()
        for student in students:
            avg_rating = db.session.query(func.avg(Rating.rating_overall)).filter_by(student_id=student.id).scalar()
            student.average_rating = avg_rating if avg_rating else 0.0

        # Get the top 5 students based on average rating
        top_students = Student.query.order_by(Student.average_rating.desc()).limit(5).all()

        return render_template('professor_home.html', top_students=top_students)
    else:
        return "Access Denied"

# this is the route for professor are able to recommend students 

@app.route('/recommend/<student_id>', methods=['POST'])
@login_required
def recommend_student(student_id):
    if current_user.type == 'professor':
        description = request.form.get('recommendation_description')
        recommendation = Recommendation(professor_id=current_user.id, student_id=student_id, description=description)
        db.session.add(recommendation)
        db.session.commit()
        flash('Recommendation submitted successfully', 'success')
        return redirect(url_for('professor_home'))
    else:
        return "ACCESS DENIED"

@login_required
@app.route('/users/<userid>', methods=['GET', 'POST'])
def user_profile(userid):
    print("User ID:", userid)
    targetUser = User.query.filter_by(id=userid).first()
    if targetUser.type == 'student':
        print("Student found:", targetUser.full_name)
        return render_template('student_profile.html', student=targetUser)
    elif targetUser.type == 'professor':
        print("Professor found:", targetUser.full_name)
        return render_template('professor_profile.html', professor=targetUser)
    else:
        print("No user found with ID:", userid)
        return redirect(url_for('search_page'))
