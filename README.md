# Smart AI-Enabled Campus Management System

A full-stack web-based **Campus Management and Intelligence System** built using **Python (Flask)**, **SQLite**, **Bootstrap**, and **Chart.js**.

This system manages campus infrastructure and academic entities while providing real-time analytics, utilization insights, and intelligent recommendations.

---

## Project Overview

The **Smart AI-Enabled Campus Management System** is designed to:

- Manage campus blocks and classrooms  
- Manage courses, faculty, and students  
- Calculate classroom capacity utilization  
- Analyze faculty workload distribution  
- Detect overloaded and underutilized classrooms  
- Provide smart redistribution recommendations  
- Present analytical insights via dashboards and charts  

This project demonstrates how data-driven decision-making can improve institutional resource management.

---

## Objectives

- Implement full CRUD functionality for all campus entities  
- Compute real-time resource utilization  
- Detect inefficiencies automatically  
- Provide intelligent suggestions using rule-based logic  
- Build a responsive, professional dashboard UI  
- Maintain clean backend architecture using Flask  

---

## System Architecture

```
Flask (Backend)
│
├── SQLite Database
│
├── Templates (Jinja2 + Bootstrap)
│
└── Chart.js (Visualization)
```

---

## Core Features

### 1. Authentication
- Admin login system  
- Session-based access control  

### 2. Infrastructure Management
- Add / View / Delete Blocks  
- Add / View / Delete Classrooms  
- Assign classrooms to blocks  
- Set capacity and current occupancy  

### 3. Academic Management
- Manage Courses  
- Manage Faculty  
- Manage Students  
- Assign students to courses and classrooms  

### 4. Analytics & Intelligence

#### Classroom Utilization

```
Utilization (%) = (Current Students / Capacity) × 100
```

- Overloaded detection (> 90%)  
- Underutilized detection (< 40%)  

#### Campus Utilization

```
Campus Utilization = (Total Students / Total Capacity) × 100
```

#### Faculty Workload

```
Workload = Number of Courses Assigned
```

- Faculty overload detection (> 3 courses)  

---

## Smart Recommendation Engine

If overloaded and underutilized rooms exist:

```
Recommend moving students from overloaded room to underutilized room
```

---

## Dashboard Features

- Total Blocks  
- Total Classrooms  
- Total Students  
- Total Faculty  
- Campus Utilization %  
- Overloaded Room Card (Clickable Modal)  
- Underutilized Room Card (Clickable Modal)  
- Classroom Utilization Chart  
- Block Utilization Chart  
- Smart Recommendation Panel  
- Faculty Overload Alerts  

---

## Technologies Used

- Python 3  
- Flask  
- SQLite  
- Bootstrap 5  
- Chart.js  
- Jinja2 Templating  

---

## Project Structure

```
campus-management/
│
├── app.py
├── database.db
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── blocks.html
│   ├── classrooms.html
│   ├── courses.html
│   ├── faculty.html
│   └── students.html
│
└── static/
```

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-campus-system.git
cd smart-campus-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000/
```

---

## Database Schema Overview

### Blocks
- id  
- block_name  

### Classrooms
- id  
- block_id  
- room_number  
- capacity  
- current_students  

### Courses
- id  
- course_name  
- course_code  

### Faculty
- id  
- name  
- department  

### Students
- id  
- name  
- reg_no  
- course_id  
- classroom_id  

---

## Example Utilization Logic

```python
util = round((room["current_students"] / room["capacity"]) * 100, 2)

if util > 90:
    overloaded.append(room["room_number"])
elif util < 40:
    underutilized.append(room["room_number"])
```

---

## Future Enhancements

- Role-based access control  
- Export analytics as PDF  
- Predictive enrollment forecasting  
- Automated timetable optimization  
- REST API version  
- Deployment on cloud (Render / AWS / Azure)  

---

## Learning Outcomes

This project demonstrates:

- Backend architecture design  
- SQL database interaction  
- Web routing and session management  
- Data analytics implementation  
- Rule-based AI logic  
- Dashboard visualization  
- Full-stack integration  

---

## License

This project is developed for academic and educational purposes.

---

## Author

Developed as part of academic coursework under the project:

Smart AI-Enabled LPU Campus Management System (Web-Based) Using Python Frameworks
