# TODO: Implement school email verification

from app import app, db, load_user
from app.models import User, Student, Professor, Recommendation, Rating
from app.forms import RatingForm, SignUpForm, SignInForm
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

# Student/Professor search functionality
@login_required
@app.route('/users/search')
def search_page():
    print(isinstance(current_user, Student))
    return render_template('search.html')

# Search suggestion logic for main search bar
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

@login_required
@app.route('/users/<userid>', methods=['GET', 'POST'])
def user_profile(userid):
    targetUser = User.query.filter_by(id=userid).first()
    if not targetUser:
        print("No user found with ID:", userid)
        return redirect(url_for('search_page'))

    if targetUser.type == 'student':
        student = Student.query.get(userid)
        total_rating = sum(rating.rating_overall for rating in student.ratings)
        if student.ratings:
            average_rating = "{:.2f}".format(total_rating / len(student.ratings))
        else:
            average_rating = "No Ratings"  # Default value when there are no ratings

        print(average_rating)
        return render_template('student_profile.html', student=student, averagerating=average_rating)
    elif targetUser.type == 'professor':
        # Handle professor profile
        professor = Professor.query.get(userid)
        print("Professor found:", professor.full_name)

        return render_template('professor_profile.html', professor=professor)
    else:
        print("Unrecognized user type for ID:", userid)
        return redirect(url_for('search_page'))

@login_required
@app.route('/rate_student/<student_id>', methods=['GET', 'POST'])
def rate_student(student_id):
    if student_id == current_user.id:
        # Redirect or show an error if the user tries to rate themselves
        flash('You cannot rate yourself.', 'error')
        return redirect(url_for('user_profile', userid=student_id))

    student = Student.query.get_or_404(student_id)
    form = RatingForm()

    existing_rating = Rating.query.filter_by(reviewer_id=current_user.id, student_id=student_id).first()
    if existing_rating:
        # Redirect or show an error if the user has already rated this student
        flash('You have already rated this student.', 'error')
        return redirect(url_for('user_profile', userid=student_id))

    if form.validate_on_submit():
        # Retrieve form data
        rating_participation = float(form.rating_participation.data)
        rating_communication = float(form.rating_communication.data)
        rating_skill = float(form.rating_skill.data)
        description = form.description.data

        # Calculate overall rating
        rating_overall = (rating_participation + rating_communication + rating_skill) / 3
        rating_overall = float("{:.2f}".format(rating_overall))

        # Create new Rating object
        new_rating = Rating(
            rating_overall=rating_overall,
            rating_participation=rating_participation,
            rating_communication=rating_communication,
            rating_skill=rating_skill,
            description=description,
            reviewer_id=current_user.id, 
            student_id=student_id
        )

        # Add new Rating to the database
        db.session.add(new_rating)
        db.session.commit()

        # Redirect to the student's profile page after submission
        return redirect(url_for('user_profile', userid=student_id))

    return render_template('rate_student.html', form=form, student=student)