CREATE DATABASE IF NOT EXISTS ticket_management;
USE ticket_management;

CREATE TABLE roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(30) UNIQUE NOT NULL,
  created_at DATETIME,
  updated_at DATETIME
);

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role_id INT NOT NULL,
  is_active_user BOOLEAN DEFAULT TRUE,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE teams (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(80) UNIQUE NOT NULL,
  created_at DATETIME,
  updated_at DATETIME
);

CREATE TABLE user_teams (
  user_id INT NOT NULL,
  team_id INT NOT NULL,
  PRIMARY KEY (user_id, team_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) UNIQUE NOT NULL,
  created_at DATETIME,
  updated_at DATETIME
);

CREATE TABLE tickets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  parent_ticket_id INT NULL,
  project_id INT NOT NULL,
  subject VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  priority ENUM('Low','Medium','High','Critical') NOT NULL,
  estimated_hours DECIMAL(8,2) NOT NULL,
  start_at DATETIME NOT NULL,
  end_at DATETIME NOT NULL,
  received_department VARCHAR(100) NOT NULL,
  status ENUM('New','Assigned','WIP','On Hold','Completed','Closed','Reopened') NOT NULL DEFAULT 'New',
  created_by INT NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (parent_ticket_id) REFERENCES tickets(id),
  FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE ticket_assignments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ticket_id INT NOT NULL,
  team_id INT NULL,
  user_id INT NULL,
  assignment_type ENUM('TEAM','USER') NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (ticket_id) REFERENCES tickets(id),
  FOREIGN KEY (team_id) REFERENCES teams(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE activities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE work_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ticket_id INT NOT NULL,
  user_id INT NOT NULL,
  work_date DATE NOT NULL,
  hours_spent DECIMAL(5,2) NOT NULL,
  activity_id INT NOT NULL,
  comments TEXT,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (ticket_id) REFERENCES tickets(id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (activity_id) REFERENCES activities(id)
);

CREATE TABLE notifications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  message TEXT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE attachments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ticket_id INT NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  FOREIGN KEY (ticket_id) REFERENCES tickets(id)
);

CREATE TABLE audit_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  action VARCHAR(255) NOT NULL,
  metadata JSON,
  created_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
