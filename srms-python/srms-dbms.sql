CREATE DATABASE student_system;
USE student_system;

CREATE TABLE students (
    roll INT PRIMARY KEY,
    name VARCHAR(50),
    branch VARCHAR(30),
    year INT,
    cgpa FLOAT,
    phone VARCHAR(15)
);

CREATE TABLE tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    roll INT,
    field_name VARCHAR(20),
    old_value VARCHAR(50),
    new_value VARCHAR(50),
    status VARCHAR(15),
    FOREIGN KEY (roll) REFERENCES students(roll)
);

INSERT INTO students VALUES
(420, 'Thanmayi', 'MECH', 2, 9.10, '9876543210'),
(421, 'Riya', 'CSE', 1, 8.90, '9123456780');

delete from students where roll=421;

INSERT INTO students VALUES
(265, 'Meghana', 'CSE', 3, 9.20, '9876586967'),
(421, 'Videuma', 'CSE', 1, 9.80, '9123456780'),
(168, 'Rushitha', 'CSE', 1, 8.90, '7799498975');
