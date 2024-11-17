-- Create the database
CREATE DATABASE HealthAndWellnessTracker;
USE HealthAndWellnessTracker;
set foreign_key_checks=0;


-- Creating the User table
CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Fname VARCHAR(50),
    Lname VARCHAR(50),
    Age INT,
    Gender VARCHAR(10),
    DOB DATE,
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(15),
    Password VARCHAR(255)
);

-- Creating the Friends table
CREATE TABLE Friends (
    UserID1 INT,
    UserID2 INT,
    FriendshipStatus VARCHAR(20),
    PRIMARY KEY (UserID1, UserID2),
    FOREIGN KEY (UserID1) REFERENCES User(UserID),
    FOREIGN KEY (UserID2) REFERENCES User(UserID)
);

-- Creating the Goal table
CREATE TABLE Goal (
    GoalID INT PRIMARY KEY AUTO_INCREMENT,
    GoalType VARCHAR(100),
    TargetValue DECIMAL(10, 2),
    CurrentValue DECIMAL(10, 2),
    Status VARCHAR(50),
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Creating the MentalHealthCheck table
CREATE TABLE MentalHealthCheck (
    CheckID INT PRIMARY KEY AUTO_INCREMENT,
    MoodRating INT CHECK (MoodRating BETWEEN 1 AND 10),
    StressLevel INT CHECK (StressLevel BETWEEN 1 AND 10),
    Date DATE,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);


-- Creating the Meal table
CREATE TABLE Meal (
    MealID INT PRIMARY KEY AUTO_INCREMENT,
    MealName VARCHAR(100),
    Serving DECIMAL(10, 2) CHECK (Serving > 0) -- Ensuring positive serving size
);

-- Creating the DietLog table
CREATE TABLE DietLog (
    DietLogID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE,
    MealID INT,
    UserID INT,
    FOREIGN KEY (MealID) REFERENCES Meal(MealID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Creating the Activity table
CREATE TABLE Activity (
    ActivityID INT PRIMARY KEY AUTO_INCREMENT,
    ActivityName VARCHAR(100),
    CaloriesBurnedPerHour DECIMAL(10, 2)
);

-- Creating the ExerciseLog table
CREATE TABLE ExerciseLog (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE,
    Duration INT,  -- Duration in minutes
    ActivityID INT,
    UserID INT,
    CaloriesBurned DECIMAL(10, 2),
    FOREIGN KEY (ActivityID) REFERENCES Activity(ActivityID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

-- Linking tables with relationships

-- User Pursues Goal
CREATE TABLE Pursues (
    UserID INT,
    GoalID INT,
    PRIMARY KEY (UserID, GoalID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (GoalID) REFERENCES Goal(GoalID)
);

-- Mental Health Logs
CREATE TABLE Logs (
    CheckID INT,
    LogID INT,
    PRIMARY KEY (CheckID, LogID),
    FOREIGN KEY (CheckID) REFERENCES MentalHealthCheck(CheckID),
    FOREIGN KEY (LogID) REFERENCES ExerciseLog(LogID)
);

-- Friendship relationships
CREATE TABLE Friendship (
    UserID1 INT,
    UserID2 INT,
    FriendshipStatus VARCHAR(50),
    PRIMARY KEY (UserID1, UserID2),
    FOREIGN KEY (UserID1) REFERENCES User(UserID),
    FOREIGN KEY (UserID2) REFERENCES User(UserID)
);

-- Insert sample data into the User table
INSERT INTO User (Fname, Lname, Age, Gender, DOB, Email, PhoneNumber, Password)
VALUES 
('John', 'Doe', YEAR(CURDATE()) - 1990, 'Male', '1990-05-15', 'john.doe@example.com', '1234567890', 'password1'),
('Jane', 'Smith', YEAR(CURDATE()) - 1985, 'Female', '1985-10-12', 'jane.smith@example.com', '2345678901', 'password2'),
('Alice', 'Johnson', YEAR(CURDATE()) - 1992, 'Female', '1992-03-22', 'alice.johnson@example.com', '3456789012', 'password3'),
('Bob', 'Brown', YEAR(CURDATE()) - 1995, 'Male', '1995-07-08', 'bob.brown@example.com', '4567890123', 'password4'),
('Charlie', 'Davis', YEAR(CURDATE()) - 2000, 'Male', '2000-11-02', 'charlie.davis@example.com', '5678901234', 'password5'),
('Emma', 'Wilson', YEAR(CURDATE()) - 1988, 'Female', '1988-06-25', 'emma.wilson@example.com', '6789012345', 'password6'),
('David', 'Moore', YEAR(CURDATE()) - 1993, 'Male', '1993-02-17', 'david.moore@example.com', '7890123456', 'password7'),
('Sophia', 'Taylor', YEAR(CURDATE()) - 1991, 'Female', '1991-09-30', 'sophia.taylor@example.com', '8901234567', 'password8'),
('James', 'White', YEAR(CURDATE()) - 1997, 'Male', '1997-12-05', 'james.white@example.com', '9012345678', 'password9'),
('Mia', 'Harris', YEAR(CURDATE()) - 1999, 'Female', '1999-04-18', 'mia.harris@example.com', '0123456789', 'password10');

-- Insert sample data into the Friends table
INSERT INTO Friends (UserID1, UserID2, FriendshipStatus)
VALUES 
(1, 2, 'Friends'),
(1, 3, 'Friends'),
(2, 4, 'Friends'),
(3, 5, 'Friends'),
(4, 6, 'Friends'),
(5, 7, 'Friends'),
(6, 8, 'Friends'),
(7, 9, 'Friends'),
(8, 10, 'Friends'),
(9, 1, 'Friends');

-- Insert sample data into the Goal table
INSERT INTO Goal (GoalType, TargetValue, CurrentValue, Status, UserID)
VALUES 
('Lose Weight', 5.0, 1.5, 'In Progress', 1),
('Run 5k', 5.0, 3.0, 'In Progress', 2),
('Read Books', 10.0, 4.0, 'In Progress', 3),
('Save Money', 1000.0, 500.0, 'In Progress', 4),
('Gain Muscle', 3.0, 1.0, 'In Progress', 5),
('Run Marathon', 42.0, 25.0, 'In Progress', 6),
('Meditate Daily', 30.0, 10.0, 'In Progress', 7),
('Write Journal', 50.0, 20.0, 'In Progress', 8),
('Quit Smoking', 30.0, 15.0, 'In Progress', 9),
('Complete Coding Challenge', 100.0, 50.0, 'In Progress', 10);

INSERT INTO MentalHealthCheck (MoodRating, StressLevel, Date, UserID)
VALUES 
(7, 5, '2024-10-20', 1),
(6, 6, '2024-10-20', 2),
(8, 3, '2024-10-20', 3),
(4, 7, '2024-10-20', 4),
(5, 8, '2024-10-20', 5);



-- Insert sample data into the Meal table
INSERT INTO Meal (MealName, Serving)
VALUES 
('Chicken Salad', 1.5),
('Pasta', 2.0),
('Grilled Cheese', 1.0),
('Fruit Smoothie', 1.0),
('Steak', 2.5),
('Tuna Sandwich', 1.0),
('Rice and Beans', 1.5),
('Omelette', 1.0),
('Pancakes', 3.0),
('Salmon', 2.0);

-- Insert sample data into the DietLog table
INSERT INTO DietLog (Date, MealID, UserID)
VALUES 
('2024-10-15', 1, 1),
('2024-10-15', 2, 2),
('2024-10-14', 3, 3),
('2024-10-14', 4, 4),
('2024-10-13', 5, 5),
('2024-10-13', 6, 6),
('2024-10-12', 7, 7),
('2024-10-12', 8, 8),
('2024-10-11', 9, 9),
('2024-10-11', 10, 10);

-- Insert sample data into the Activity table
INSERT INTO Activity (ActivityName, CaloriesBurnedPerHour)
VALUES 
('Running', 600),
('Swimming', 700),
('Cycling', 500),
('Yoga', 250),
('Weight Lifting', 400),
('Hiking', 450),
('Dancing', 300),
('Boxing', 800),
('Walking', 200),
('Jump Rope', 750);

-- Insert sample data into the ExerciseLog table
INSERT INTO ExerciseLog (Date, Duration, ActivityID, UserID)
VALUES 
('2024-10-15', 60, 1, 1),
('2024-10-15', 45, 2, 2),
('2024-10-14', 30, 3, 3),
('2024-10-14', 90, 4, 4),
('2024-10-13', 60, 5, 5),
('2024-10-13', 120, 6, 6),
('2024-10-12', 30, 7, 7),
('2024-10-12', 45, 8, 8),
('2024-10-11', 60, 9, 9),
('2024-10-11', 30, 10, 10);

-- Insert sample data into the Pursues table
INSERT INTO Pursues (UserID, GoalID)
VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- Insert sample data into the Logs table
INSERT INTO Logs (CheckID, LogID)
VALUES 
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- Add at the end of your SQL file

-- Trigger to automatically update goal progress percentage


DELIMITER //
CREATE TRIGGER CalculateGoalProgress
BEFORE UPDATE ON Goal
FOR EACH ROW
BEGIN
    SET NEW.Progress = (NEW.CurrentValue / NEW.TargetValue) * 100;
    IF NEW.Progress >= 100 THEN
        SET NEW.Status = 'Completed';
    END IF;
END //
DELIMITER ;

-- Drop existing function if it exists
DROP FUNCTION IF EXISTS GetGoalCompletionRate;

-- Create the function with proper return type
DELIMITER //
CREATE FUNCTION GetGoalCompletionRate(userId INT) 
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE total_goals INT;
    DECLARE completed_goals INT;
    DECLARE completion_rate DECIMAL(5,2);
    
    SELECT COUNT(*) INTO total_goals
    FROM Goal
    WHERE UserID = userId;
    
    SELECT COUNT(*) INTO completed_goals
    FROM Goal
    WHERE UserID = userId AND Status = 'Completed';
    
    IF total_goals > 0 THEN
        SET completion_rate = (completed_goals / total_goals) * 100;
    ELSE
        SET completion_rate = 0;
    END IF;
    
    RETURN completion_rate;
END //
DELIMITER ;

-- Drop existing procedure
DROP PROCEDURE IF EXISTS GetUserGoalSummary;

-- Create updated stored procedure
DELIMITER //
CREATE PROCEDURE GetUserGoalSummary(IN userId INT)
BEGIN
    SELECT 
        GoalID,
        GoalType,
        Status,
        CurrentValue,
        TargetValue,
        Progress
    FROM Goal
    WHERE UserID = userId
    ORDER BY Status DESC, Progress DESC;
END //
DELIMITER ;







-- Add Progress column to Goal table
ALTER TABLE Goal ADD COLUMN Progress DECIMAL(5,2) DEFAULT 0;

-- Update existing goals' progress
UPDATE Goal 
SET Progress = (CurrentValue / TargetValue * 100) 
WHERE TargetValue > 0;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS UpdateGoalProgress;

-- Create the corrected trigger
DELIMITER //
CREATE OR REPLACE TRIGGER UpdateGoalProgress
BEFORE UPDATE ON Goal
FOR EACH ROW
BEGIN
    -- Calculate progress percentage correctly
    IF NEW.TargetValue > 0 THEN
        SET NEW.Progress = (NEW.CurrentValue / NEW.TargetValue) * 100;
    ELSE
        SET NEW.Progress = 0;
    END IF;
    
    -- Update status based on progress
    IF NEW.Progress >= 100 THEN
        SET NEW.Status = 'Completed';
    ELSE
        SET NEW.Status = 'In Progress';
    END IF;
END //
DELIMITER ;

-- Fix existing data in the Goal table
UPDATE Goal
SET Progress = (CurrentValue / TargetValue) * 100
WHERE TargetValue > 0;

-- Add this function to calculate total calories burned
DELIMITER //
CREATE FUNCTION TotalCaloriesBurned(userId INT, exerciseDate DATE) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total_calories DECIMAL(10,2);
    
    SELECT SUM((a.CaloriesBurnedPerHour * e.Duration) / 60) INTO total_calories
    FROM ExerciseLog e
    JOIN Activity a ON e.ActivityID = a.ActivityID
    WHERE e.UserID = userId 
    AND e.Date = exerciseDate;
    
    RETURN COALESCE(total_calories, 0);
END //
DELIMITER ;

-- Update Goal table structure if needed
ALTER TABLE Goal MODIFY TargetValue DECIMAL(10,2);
ALTER TABLE Goal MODIFY CurrentValue DECIMAL(10,2);
ALTER TABLE Goal MODIFY Progress DECIMAL(5,2);