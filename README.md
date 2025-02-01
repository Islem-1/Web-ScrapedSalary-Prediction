# salary_prediction_prj

## Overview
The **Web-Scraped Salary Prediction** is a web-based application that collects salary-related data from **Indeed** using web scraping techniques. The extracted data, including **job title, experience level, company name, and country**, is processed and used to train a **machine learning model** to predict salary ranges. This project showcases how web scraping and AI can be used to analyze job market trends and provide salary estimates based on real-world data.

## Features
- **Web Scraping**: Extracts job data (title, experience, company, country) from Indeed.
- **Data Processing**: Cleans and structures extracted data for analysis.
- **Salary Prediction**: Uses machine learning to estimate salaries based on job attributes.
- **User-Friendly Interface**: Simple design for inputting job details and getting salary predictions.


## Technologies Used
- **Python**: Main programming language for development.
- **Flask**: Lightweight web framework for building the application.
- **BeautifulSoup & Selenium (WebDriver)**: Used for web scraping Indeed job listings.
- **Pandas & NumPy**: Data processing and manipulation.
- **Scikit-learn**: Machine learning model for salary prediction.

## Getting Started
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Flask
- BeautifulSoup
- Selenium (with WebDriver)
- Pandas, NumPy, Scikit-learn

### Installation
#### 1. Clone the Repository
```bash
git clone https://github.com/Islem-1/Web-ScrapedSalary-Prediction.git
cd Web-ScrapedSalary-Prediction
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run the Application
```bash
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000/` to use the application.

## Usage
1. Enter the **job title**, **experience level**, **company name**, and **country**.
2. Click the "Predict Salary" button.
3. View the predicted salary range and insights.

## License
This project is open-source and available under the MIT License.

---

### **Contributions & Feedback**
Feel free to contribute by submitting pull requests or reporting issues. Your feedback is highly appreciated!


 
