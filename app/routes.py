# TODO: Implement school email verification

from sqlalchemy import func
from app import app, db, load_user, makeTestUsers
from app.models import User, Student, Professor, Recommendation, Rating, Report, Administrator
from app.forms import RatingForm, RecommendationForm, SignUpForm, SignInForm, ReportForm
from flask import flash, jsonify, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    if load_user('admin') == None:
        makeTestUsers.makeAdmin()
        makeTestUsers.makeProfessors()
        makeTestUsers.makeStudents()
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
        
        #Check box handeling: If box is checked, change user type to professor
        if signUp.professor_check.data == True:
            userType = 'professor'
        else: 
            userType = 'student'

        if password == password_confirm:
            hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            newUser = User(id=signUp.id.data,
                           full_name=signUp.full_name.data,
                           email=signUp.email.data,
                           password=hashedPass,
                           type=userType)
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
            average_rating = total_rating / len(student.ratings)
        else:
            average_rating = 0  # Default value when there are no ratings

        print(average_rating)
        print(student.recommendations)

        return render_template('student_profile.html', student=student, averagerating=average_rating, )
    
    elif targetUser.type == 'professor':
        # Handle professor profile
        professor = Professor.query.get(userid)
        print("Professor found:", professor.full_name)
        print(professor.recommendations)
        return render_template('professor_profile.html', professor=professor, professor_recommendations=professor.recommendations)
    
    elif targetUser.type == 'administrator':
        # Handle administrator profile
        administrator = Administrator.query.get(userid) #Changed this from Administrator.query() ->  User.query() because the administrator table is not population
        print("Administrator found:", administrator.full_name)
        return render_template('administrator_profile.html', administrator=administrator)
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


# Report functionality
@login_required
@app.route('/report_rating/<int:rating_id>', methods=['GET', 'POST'])
def report_rating(rating_id):
    form = ReportForm()

    if form.validate_on_submit():
        # Create a report entry in the database
        report = Report(
            description=form.report_description.data,
            rating_id=rating_id,
            reporter_id=current_user.id
        )

        db.session.add(report)
        db.session.commit()
        flash('Rating successfully Reported for Admin Review', 'success')

        # Redirect to the student's profile page after submission
        rating = Rating.query.get(rating_id)
        return redirect(url_for('user_profile', userid=rating.student_id))

    return render_template('report_rating.html', form=form)

# View reported ratings functionality
@app.route('/admin/reported_ratings')
def reported_ratings():
    if current_user.type != 'administrator':
        return redirect(url_for('search_page'))
    reported_ratings = db.session.query(Report, Rating).join(Rating).all()
    print(reported_ratings) 
    return render_template('reported_ratings.html', reported_ratings=reported_ratings)

#This route allows the admin to review the original reported rating
@app.route('/admin/reported_ratings/<rating_id><report_id>')
def review_reported_ratings(rating_id, report_id):
    reported_rating = db.session.query(Rating).filter_by(id=rating_id).first() 
    return render_template('review_reported_ratings.html', rating_id=rating_id, report_id=report_id, reported_rating=reported_rating)

#This route handles the action the admin chose to take. Either deleting the review or removing the report
@app.route('/admin/reported_ratings/<rating_id><report_id>/<delete>')
def reported_ratings_action(rating_id, report_id, delete):
    if delete == 'rating':
        ratingToDelete = db.session.query(Rating).filter_by(id=rating_id).first()
        print(ratingToDelete)
        db.session.delete(ratingToDelete)
        db.session.commit()

    elif delete == 'report':
        reportToDelete = db.session.query(Report).filter_by(id=report_id).first()
        print(reportToDelete)
        db.session.delete(reportToDelete)
        db.session.commit()

    return redirect('/admin/reported_ratings')


# this is the route for professor are able to recommend students
@app.route('/recommend/<student_id>', methods=['GET','POST'])
@login_required
def recommend_student(student_id):
    if current_user.type != 'professor':
        return redirect(url_for('/users/search')) 

    form = RecommendationForm()
    existing_recommendation = Recommendation.query.filter_by(professor_id=current_user.id, student_id=student_id).first()

    if existing_recommendation:
        return redirect(url_for('user_profile', userid=student_id))

    if form.validate_on_submit():
        new_recommendation = Recommendation(
            professor_id=current_user.id, 
            student_id=student_id, 
            description=form.description.data
        )
        db.session.add(new_recommendation)
        db.session.commit()
        return redirect(url_for('user_profile', userid=student_id))

    return render_template("recommend.html", form=form)

# this is the route to try to include the list of top-rated students
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

        return render_template('professor_profile.html', top_students=top_students)
    else:
        return "Access Denied"

