# 🩸 BloodBank
*Blood Donation Camp Organizer & Donor Management System* 

**Domain:** HealthTech
**Backend:** Django 5
**Database:** MongoDB
**API:** Django REST Framework (DRF)
**Frontend:** HTML5, CSS3, Bootstrap 5

## 📌 Project Overview

BloodBank is a web-based HealthTech application developed using Django and MongoDB. The system helps manage blood donors, organize blood donation camps, and process emergency blood requests from hospitals. It automatically matches donors based on blood group compatibility and location and sends notifications to matched donors using multithreading.

This project demonstrates Python programming concepts including OOP, Regex, Threading, MongoDB CRUD operations, Django web development, and REST API development.

## 🎯 Objectives
- Register blood donors online.
- Organize blood donation camps.
- Allow hospitals to post blood requirements.
- Match donors based on blood group and location.
- Validate user input using Regex.
- Store donor and request data in MongoDB.
- Send notifications using multithreading.
- Provide REST APIs for hospitals.

## ✨ Features
- 👤 Donor Registration
- 🩸 Blood Group Validation
- 📍 Location-wise Donor Search
- 🏥 Hospital Blood Request Board
- 🎪 Blood Donation Camp Management
- 🔍 Smart Donor Matching
- 📧 Notification System (Threading)
- 📊 Camp-wise Donor Report
- 🔐 Admin Panel
- 🌐 REST API

## 🛠 Technology Stack
**Technology	Purpose**
- Python	Programming Language
- Django	Web Framework
- Django REST Framework	REST APIs
- MongoDB	Database
- PyMongo	MongoDB Connection
- HTML5	Frontend
- CSS3	Styling
- Bootstrap 5	Responsive UI
- Regex	Input Validation
- Threading	Notifications


## 📂 Project Structure
bloodbank/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── bloodbank/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── mongo.py
│
├── donors/
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── validators.py
│   ├── compatibility.py
│   ├── notifications.py
│   ├── core.py
│   ├── documents.py
│   ├── forms.py
│   └── templates/
│
└── static/


## 🔄 Project Workflow
Donor Registration
        │
        ▼
MongoDB Database
        │
        ▼
Hospital Posts Blood Request
        │
        ▼
MatchEngine Finds Compatible Donors
        │
        ▼
Thread Sends Notifications
        │
        ▼
Camp-wise Report Generated

## 💾 Installation

**Step 1**
git clone https://github.com/yourusername/bloodbank.git

**Step 2**
cd bloodbank

**Step 3**
*Create Virtual Environment*
python -m venv venv

**Step 4**
Activate Environment

*Windows*
venv\Scripts\activate

*Linux/Mac*
source venv/bin/activate

**Step 5**
*Install Packages*
pip install -r requirements.txt

**Step 6**
*Run Django*
python manage.py migrate
python manage.py runserver

## 🌐 API Endpoints
**Method	Endpoint	Description**
POST	/api/donors/	Register Donor
GET	/api/donors/	View Donors
POST	/api/camps/	Create Camp
GET	/api/camps/	View Camps
POST	/api/requests/	Blood Request
GET	/api/reports/	Camp Report

## 📊 Database Collections
**Donors**
**Camps**
**Blood Requests**

## 🔮 Future Scope
- SMS Notification
- Email Notification
- Mobile Application
- GPS-based Donor Search
- AI-based Donor Recommendation
- QR Code for Donor Registration

## 👨‍💻 Author

Name: Aamrapali Mahajan

Course: Master of Computer Applications (MCA)

Project: BloodBank – Blood Donation Camp Organizer & Donor Management System

## 📜 License

This project is developed for educational purposes as part of the MCA curriculum.
