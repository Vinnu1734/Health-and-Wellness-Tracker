from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import mysql.connector
from datetime import datetime
from mysql.connector import Error

# Database configuration
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', '123'),
    'database': os.environ.get('DB_DATABASE', 'HealthAndWellnessTracker')
}

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DATABASE_CONFIG['host'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            database=DATABASE_CONFIG['database']
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Home page route
@app.route('/')
def index():
    return render_template('index.html')  # This will show the home page

# Registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']  # Store password as plain text
        
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO User (Fname, Lname, Email, Password)
                VALUES (%s, %s, %s, %s)
            ''', (first_name, last_name, email, password))
            connection.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve user by email
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT UserID, Fname, Lname, Email, Password FROM User WHERE Email = %s', (email,))
        user = cursor.fetchone()

        print(f"User data: {user}")  # Debugging: Print user object to check what is retrieved

        if user:
            # Check if password is correct
            if user[4] == password:  # Compare plain text passwords
                session['user_id'] = user[0]  # Store user id in session
                flash('Login successful!', 'success')
                cursor.close()
                connection.close()
                return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
            else:
                flash('Invalid password. Please try again.', 'error')
        else:
            flash('User not found. Please register.', 'error')

        cursor.close()
        connection.close()

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get user info
    cursor.execute('SELECT * FROM User WHERE UserID = %s', (session['user_id'],))
    user = cursor.fetchone()

    # Get goal completion rate
    cursor.execute('SELECT GetGoalCompletionRate(%s) as completion_rate', (session['user_id'],))
    result = cursor.fetchone()
    completion_rate = result['completion_rate'] if result else 0

    # Get goals with correct order of fields
    cursor.execute('''
        SELECT 
            GoalType,
            Status,
            CurrentValue,
            TargetValue,
            Progress
        FROM Goal 
        WHERE UserID = %s
        ORDER BY Status, Progress DESC
    ''', (session['user_id'],))
    goals = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('dashboard.html', 
                         user=user, 
                         goals=goals, 
                         completion_rate=completion_rate)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))  # Redirect to login page


@app.route('/mental_health_check', methods=['GET', 'POST'])
def mental_health_check():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        mood_rating = request.form['mood_rating']
        stress_level = request.form['stress_level']
        current_date = datetime.now().date()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO MentalHealthCheck 
                (UserID, MoodRating, StressLevel, Date) 
                VALUES (%s, %s, %s, %s)
            ''', (session['user_id'], mood_rating, stress_level, current_date))
            connection.commit()
            flash('Mental health check recorded successfully!', 'success')
            return redirect(url_for('view_mental_health_history'))
        except Exception as e:
            flash(f'Error recording mental health check: {str(e)}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('mental_health_check.html')

@app.route('/mental_health_history')
def view_mental_health_history():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Updated query to include CheckID
    cursor.execute('''
        SELECT Date, MoodRating, StressLevel, CheckID 
        FROM MentalHealthCheck 
        WHERE UserID = %s 
        ORDER BY Date DESC
    ''', (session['user_id'],))
    history = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('mental_health_history.html', history=history)

@app.route('/exercise_log', methods=['GET', 'POST'])
def exercise_log():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch available activities for dropdown
    cursor.execute('SELECT ActivityID, ActivityName FROM Activity')
    activities = cursor.fetchall()

    if request.method == 'POST':
        date = request.form['date']
        duration = request.form['duration']
        activity_id = request.form['activity_id']
        
        try:
            # First insert the exercise log
            cursor.execute('''
                INSERT INTO ExerciseLog 
                (Date, Duration, ActivityID, UserID) 
                VALUES (%s, %s, %s, %s)
            ''', (date, duration, activity_id, session['user_id']))
            connection.commit()

            # Then calculate and update calories burned
            cursor.execute('SELECT TotalCaloriesBurned(%s, %s)', (session['user_id'], date))
            calories_burned = cursor.fetchone()[0]
            
            # Update the calories burned for this log
            cursor.execute('''
                UPDATE ExerciseLog 
                SET CaloriesBurned = %s 
                WHERE UserID = %s AND Date = %s AND ActivityID = %s
            ''', (calories_burned, session['user_id'], date, activity_id))
            connection.commit()
            
            flash('Exercise logged successfully!', 'success')
            return redirect(url_for('view_exercise_history'))
        except Exception as e:
            flash(f'Error logging exercise: {str(e)}', 'error')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('exercise_log.html', activities=activities)

@app.route('/exercise_history')
def view_exercise_history():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT 
            e.Date, 
            a.ActivityName, 
            e.Duration,
            e.CaloriesBurned,
            (SELECT AVG(e2.CaloriesBurned)
             FROM ExerciseLog e2
             WHERE e2.ActivityID = e.ActivityID) as avg_calories_burned
        FROM ExerciseLog e
        JOIN Activity a ON e.ActivityID = a.ActivityID
        WHERE e.UserID = %s 
        ORDER BY e.Date DESC
    ''', (session['user_id'],))
    
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('exercise_history.html', history=history)

@app.route('/friends')
def friends():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch all confirmed friends
    cursor.execute('''
        SELECT u.UserID, u.Fname, u.Lname, u.Email 
        FROM User u 
        JOIN Friends f ON (u.UserID = f.UserID2 AND f.UserID1 = %s) 
            OR (u.UserID = f.UserID1 AND f.UserID2 = %s)
        WHERE f.FriendshipStatus = 'Confirmed'
    ''', (session['user_id'], session['user_id']))
    friends_list = cursor.fetchall()
    
    # Fetch incoming friend requests (requests sent to current user)
    cursor.execute('''
        SELECT u.UserID, u.Fname, u.Lname, u.Email 
        FROM User u 
        JOIN Friends f ON u.UserID = f.UserID1
        WHERE f.UserID2 = %s AND f.FriendshipStatus = 'Pending'
    ''', (session['user_id'],))
    incoming_requests = cursor.fetchall()
    
    # Fetch outgoing friend requests (requests sent by current user)
    cursor.execute('''
        SELECT u.UserID, u.Fname, u.Lname, u.Email 
        FROM User u 
        JOIN Friends f ON u.UserID = f.UserID2
        WHERE f.UserID1 = %s AND f.FriendshipStatus = 'Pending'
    ''', (session['user_id'],))
    outgoing_requests = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('friends.html', 
                         friends=friends_list, 
                         incoming_requests=incoming_requests,
                         outgoing_requests=outgoing_requests)

@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        friend_email = request.form['friend_email']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if user exists
        cursor.execute('SELECT UserID FROM User WHERE Email = %s', (friend_email,))
        friend = cursor.fetchone()
        
        if friend:
            friend_id = friend[0]
            if friend_id == session['user_id']:
                flash('You cannot add yourself as a friend!', 'error')
            else:
                # Check if friendship already exists
                cursor.execute('''
                    SELECT FriendshipStatus 
                    FROM Friends 
                    WHERE (UserID1 = %s AND UserID2 = %s)
                        OR (UserID1 = %s AND UserID2 = %s)
                ''', (session['user_id'], friend_id, friend_id, session['user_id']))
                
                existing = cursor.fetchone()
                
                if existing:
                    flash('Friend request already exists!', 'warning')
                else:
                    # Send friend request
                    cursor.execute('''
                        INSERT INTO Friends (UserID1, UserID2, FriendshipStatus)
                        VALUES (%s, %s, 'Pending')
                    ''', (session['user_id'], friend_id))
                    connection.commit()
                    flash('Friend request sent!', 'success')
        else:
            flash('User not found!', 'error')
        
        cursor.close()
        connection.close()
        return redirect(url_for('friends'))
    
    return render_template('add_friend.html')

@app.route('/respond_friend_request/<int:friend_id>/<action>')
def respond_friend_request(friend_id, action):
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    
    if action == 'accept':
        cursor.execute('''
            UPDATE Friends 
            SET FriendshipStatus = 'Confirmed'
            WHERE UserID1 = %s AND UserID2 = %s
        ''', (friend_id, session['user_id']))
        flash('Friend request accepted!', 'success')
    elif action == 'reject':
        cursor.execute('''
            DELETE FROM Friends 
            WHERE UserID1 = %s AND UserID2 = %s
        ''', (friend_id, session['user_id']))
        flash('Friend request rejected!', 'success')
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('friends'))

@app.route('/goals', methods=['GET', 'POST'])
def goals():
    if 'user_id' not in session:
        flash('You need to log in first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        if 'action' in request.form:
            goal_id = request.args.get('goal_id')
            if request.form['action'] == 'update_progress':
                try:
                    new_value = float(request.form['current_value'])
                    
                    # Get the target value
                    cursor.execute('''
                        SELECT TargetValue 
                        FROM Goal 
                        WHERE GoalID = %s AND UserID = %s
                    ''', (goal_id, session['user_id']))
                    result = cursor.fetchone()
                    
                    if result:
                        target_value = float(result['TargetValue'])
                        if new_value > target_value:
                            flash('Current value cannot exceed target value!', 'error')
                        else:
                            # Update current value and recalculate progress
                            cursor.execute('''
                                UPDATE Goal 
                                SET CurrentValue = %s,
                                    Progress = (%s / TargetValue) * 100
                                WHERE GoalID = %s AND UserID = %s
                            ''', (new_value, new_value, goal_id, session['user_id']))
                            connection.commit()
                            flash('Goal progress updated successfully!', 'success')
                    else:
                        flash('Goal not found!', 'error')
                except ValueError:
                    flash('Please enter a valid number', 'error')
        else:
            # Handle new goal creation
            try:
                goal_name = request.form['goal_name']
                target_value = float(request.form['target_value'])
                current_value = float(request.form.get('current_value', 0))
                
                if current_value > target_value:
                    flash('Current value cannot exceed target value!', 'error')
                else:
                    # Calculate initial progress
                    progress = (current_value / target_value * 100) if target_value > 0 else 0
                    
                    cursor.execute('''
                        INSERT INTO Goal (UserID, GoalType, Status, TargetValue, CurrentValue, Progress)
                        VALUES (%s, %s, 'In Progress', %s, %s, %s)
                    ''', (session['user_id'], goal_name, target_value, current_value, progress))
                    connection.commit()
                    flash('New goal added successfully!', 'success')
            except ValueError:
                flash('Please enter valid numbers for target and current values', 'error')

    # Fetch all goals for display
    cursor.execute('''
        SELECT 
            GoalID,
            GoalType,
            Status,
            TargetValue,
            CurrentValue,
            Progress
        FROM Goal 
        WHERE UserID = %s
        ORDER BY Status, Progress DESC
    ''', (session['user_id'],))
    goals = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return render_template('goals.html', goals=goals)

# Add this new route for delete operation
@app.route('/delete_mental_health_check/<int:check_id>', methods=['POST'])
def delete_mental_health_check(check_id):
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # First check if there are any records in the Logs table referencing this CheckID
        cursor.execute('''
            DELETE FROM Logs 
            WHERE CheckID = %s
        ''', (check_id,))
        
        # Then delete the mental health check
        cursor.execute('''
            DELETE FROM MentalHealthCheck 
            WHERE CheckID = %s AND UserID = %s
        ''', (check_id, session['user_id']))
        
        # Print the number of rows affected
        rows_affected = cursor.rowcount
        print(f"Rows affected by delete: {rows_affected}")
        
        if rows_affected > 0:
            connection.commit()
            flash('Mental health check deleted successfully!', 'success')
        else:
            flash('No record found to delete.', 'error')
            
    except Exception as e:
        connection.rollback()
        print(f"Error in deletion: {str(e)}")  # Print the error for debugging
        flash(f'Error deleting mental health check: {str(e)}', 'error')
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('view_mental_health_history'))





if __name__ == '__main__':
    app.run(debug=True)