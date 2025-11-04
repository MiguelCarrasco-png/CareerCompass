# CareerCompass

The project scrapes and analyzes job postings from SHPE sponsor companies to provide actionable career insights.

## 🚀 Core Features

1.  **In-Demand Skills Dashboard**: Automatically scrapes internship and job postings from sponsor companies and uses NLP (Natural Language Processing) to extract and visualize the most frequently required technical skills.
2.  **Resume Matcher**: Allows a user to upload their resume (PDF or TXT) and select a job posting. The tool then calculates a "match score" and shows which required skills they have and which they are missing.

## 🛠️ Tech Stack

* **Language**: Python
* **Web Framework**: Streamlit
* **NLP**: spaCy (or Hugging Face)
* **Data Scraping**: `requests` & `BeautifulSoup`
* **Data Visualization**: Plotly
* **File Handling**: `pandas`, `PyPDF2`

## 📁 Project Structure

```
├── CareerCompass.gitignore # Ignores files like venv and pycache.

├── README.md # You are here! 

├── requirements.txt # All Python libraries needed 

├── app.py # The main Streamlit app file to run 

├── notebooks/ # Jupyter notebooks for testing/EDA 

└── src/init.py  # Main source code  

├── src/scraper.py # Functions for scraping job data 

└── src/nlp_processor.py # Functions for NLP (skill extraction, matching)
```

## 🏁 How to start working on the project (Cloning)

Follow these steps to get a copy of the project running on your local machine for development and testing.

### 1. Clone the Repository

Since you are a collaborator, you can clone the repository directly using HTTPS (through the vscode terminal):

```bash
# Clone the repo into your desired IDE. 
# To use the terminal in vscode go to the terminal tab on the top and click new terminal.
git clone https://github.com/[YOUR-USERNAME]/CareerCompass.git
```

### 2. Create a Virtual Environment
It is highly recommended to use a virtual environment to keep project dependencies separate.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

```bash
# Need to put them in the library :(), haven't done so yet
pip install -r requirements.txt
```
 
### 4. Run the Application
Once everything is installed, you can run the Streamlit app.

```bash
streamlit run app.py
```

Your web browser should automatically open to the application's local address (usually http://localhost:8501).

## 🤝 Team Workflow and Git rule book (**REALLY IMPORTANT**)

We use a protected main branch. You cannot push code directly to main. All code must be submitted through a Pull Request (PR).

### Step 1: Get the latest code ###
 Always make sure your local main branch is up-to-date before starting a new feature.

```bash
git checkout main
git pull origin main
```

### Step 2: Create a new feature branch ###
 Create a new branch for your task. Name it descriptively.

```bash

# Example: If you are building the scraper
git checkout -b feature/build-scraper
```

### Step 3: Write your code ###
 Make your changes, write your code, and commit your work in small, logical steps.

```bash
# After making some changes...
git add .
git commit -m "Adds scraper function for Company X"
```

### Step 4:** Push your feature branch ###
Push your new branch up to the remote repository on GitHub.

```bash
# The -u flag sets your branch to "track" the remote branch
git push -u origin feature/build-scraper
```

### Step 5:** Open a Pull Request (PR) ###
Go to the repository on GitHub. You will see a prompt to "Compare & pull request". Click it, write a short description of what you did, and tag your teammates to review it.