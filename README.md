# Cyberbullying Detection System 

A machine learning–based web application that detects cyberbullying in user-submitted text and enforces automated moderation using warnings, user blocking, and reporting.

##  Project Overview

The Cyberbullying Detection System analyzes online comments in real time using Natural Language Processing (NLP) and a trained Logistic Regression model. It identifies abusive content, tracks user offenses, blocks repeat offenders, and generates downloadable PDF reports for administrators.

## Features

- Real-time cyberbullying detection  
- NLP preprocessing with TF-IDF vectorization  
- 3-strike warning and auto-blocking system  
- User offense tracking using JSON storage  
- Admin dashboard with statistics  
- PDF report generation  
- Lightweight FastAPI backend  

## Technologies Used

- **Programming Language: Python  
- **Framework: FastAPI  
- **Machine Learning:  Scikit-learn (Logistic Regression)  
- **NLP:  TF-IDF Vectorizer  
- **Frontend:  HTML, CSS, JavaScript  
- **Data Storage:  JSON files  
- **Report Generation:  ReportLab  

##  Project Structure

cyber_bullying_detection/
│
├── api/
│   └── app.py
│
├── src/
│   ├── train_model.py
│   ├── predict.py
│   ├── features.py
│   ├── data_utils.py
│   ├── evaluate.py
│   └── __init__.py
│
├── models/
│   ├── model.joblib
│   └── vectorizer.joblib
│
├── data/
│   └── sample_dataset.json
│
├── requirements.txt
├── README.md
└── .gitignore


## How It Works

1. User submits a text comment  
2. Text is cleaned and vectorized using NLP  
3. ML model predicts bullying or safe content  
4. Warnings are issued for violations  
5. User is blocked after 3 offenses  
6. Reports are logged and exported as PDF 
 

##  How to Run the Project

1. Clone the repository from **:contentReference[oaicite:0]{index=0}**
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3.Start the FastAPI server:
	uvicorn api.app:app --reload
4.Open browser and visit:

http://127.0.0.1:8000/docs

## Screenshots

### Output 1
![Output 1](assets/output1.png)

### Output 2
![Output 2](assets/output2.png)

### Output 3
![Output 3](assets/output3.png)

### Output 4
![Output 4](assets/output4.png)

### Output 5
![Output 5](assets/output5.png)

### Output 6
![Output 6](assets/output6.png)


