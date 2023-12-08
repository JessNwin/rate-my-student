import bcrypt
from app import app, db
from app.models import User, Professor, Administrator

testPasswords = "1"
testPasswords = bcrypt.hashpw(testPasswords.encode('utf-8'), bcrypt.gensalt())

def makeStudents():
    newStudent0 = User(id="vin",
                   full_name="Vincent Cordova",
                   email="VincentCordova@gmail.com",
                   password=testPasswords,
                   type='student')
    newStudent1 = User(id="ben",
                   full_name="Ben Fast",
                   email="BenFast@gmail.com",
                   password=testPasswords,
                   type='student')
    newStudent2 = User(id="jes",
                   full_name="Jessica Nguyen",
                   email="JessicaNguyen@gmail.com",
                   password=testPasswords,
                   type='student')
    newStudent3 = User(id="lui",
                   full_name="Luis Paez",
                   email="LuisPaez@gmail.com",
                   password=testPasswords,
                   type='student')
    newStudent4 = User(id="jac",
                   full_name="Jacqueline Hernandez",
                   email="JacquelineHernandez@gmail.com",
                   password=testPasswords,
                   type='student')

    db.session.add(newStudent0)
    db.session.add(newStudent1)
    db.session.add(newStudent2)
    db.session.add(newStudent3)
    db.session.add(newStudent4)
    db.session.commit()
def makeProfessors():
    newProfessor = User(id="gandulamaster",
                   full_name="Thyago Mota",
                   email="ThyagoMota@gmail.com",
                   password=testPasswords,
                   type='professor')
    db.session.add(newProfessor)
    db.session.commit()
def makeAdmin():
    newAdmin = User(id="admin",
               full_name="admin",
               email="admin@gmail.com",
               password=testPasswords,
               type='administrator')
    db.session.add(newAdmin)
    db.session.commit()

def makeTestUser():
    newTestUser = User(id="test",
               full_name="test",
               email="test@gmail.com",
               password=testPasswords,
               type='student')
    db.session.add(newTestUser)
    db.session.commit()
