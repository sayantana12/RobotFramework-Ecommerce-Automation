
<div align="center">

# 🛒 E-Commerce Automation Framework

### Robot Framework · Python · SeleniumLibrary · Jenkins

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Robot Framework](https://img.shields.io/badge/Robot_Framework-Automation-00C0B5)](https://robotframework.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Web_Testing-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)

**A modular, keyword-driven and CSV-driven web automation project built for a Python for Automation capstone assignment.**

[Overview](#-project-overview) •
[Features](#-key-features) •
[Installation](#-windows-quick-start) •
[Execution](#-running-the-tests) •
[Jenkins](#-jenkins-integration) •
[Results](#-execution-results)

</div>

---

## 📌 Project Overview

This project automates an e-commerce workflow on [Automation Exercise](https://automationexercise.com/) using **Robot Framework**, **Python** and **SeleniumLibrary**.

It follows the **Page Object Model (POM)** design pattern, separating test scenarios from reusable page-specific keywords and locators.

The main business flow uses an **existing test account** and covers:

**Launch Browser → Login → Search Product → Add to Cart → Verify Cart → Logout → Close Browser**

The framework also demonstrates CSV-driven testing, resource files, setup and teardown, command-line execution, RIDE execution, Jenkins integration and automated reporting.

> **Existing-account edition:** Register your test account manually before running the project. The registration suite is preserved as `01_registration_tests.robot.disabled` for reference and is not required for the assigned business flow.

---

## ✨ Key Features

- **Keyword-driven testing:** Reusable Robot Framework keywords.
- **Page Object Model:** Separate resource files for individual website pages.
- **Data-driven testing:** Product search terms loaded from CSV.
- **SeleniumLibrary:** Browser interactions and element verification.
- **Setup and teardown:** Automated browser initialization and cleanup.
- **Existing-account authentication:** Credentials supplied through environment variables.
- **RIDE support:** Graphical test development and execution.
- **Jenkins integration:** Pipeline-based test execution.
- **Reporting:** HTML reports, detailed logs and XML results.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Automation runtime |
| Robot Framework | Test automation framework |
| SeleniumLibrary | Browser automation |
| Selenium WebDriver | Browser interaction |
| CSV | External test data |
| RIDE | Robot Framework IDE |
| Jenkins | Pipeline execution |
| Git & GitHub | Version control |
| VS Code | Development environment |

---

## 📂 Project Structure

```text
EcommerceRobotFramework/
│
├── PageObjects/
│   ├── HomePage.resource
│   ├── LoginPage.resource
│   ├── ProductsPage.resource
│   ├── CartPage.resource
│   └── SignupPage.resource
│
├── Resources/
│   ├── variables.resource
│   └── common.resource
│
├── TestData/
│   └── search_products.csv
│
├── TestSuites/
│   ├── 01_registration_tests.robot.disabled
│   ├── 02_login_tests.robot
│   └── 03_ecommerce_business_flow.robot
│
├── Results/                  # Generated during execution
│   ├── output.xml
│   ├── log.html
│   └── report.html
│
├── .gitignore
├── Jenkinsfile
├── README.md
├── requirements.txt
├── run_tests.bat
└── run_tests.sh
```

### Architecture

```text
           Test Suites
                |
                v
       Page Object Resources
                |
                v
          SeleniumLibrary
                |
                v
          Selenium WebDriver
                |
                v
        Automation Exercise
```

The test suites describe the scenarios. The page-object resource files contain reusable keywords and element locators.

---

## ⚙️ Windows Quick Start

### 1. Clone the Repository

```powershell
git clone https://github.com/sayantana12/RobotFramework-Ecommerce-Automation.git

cd RobotFramework-Ecommerce-Automation
```

Alternatively, open your existing local project folder in VS Code.

### 2. Create and Activate a Virtual Environment

Open **Terminal → New Terminal** in VS Code.

```powershell
py -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

Verify that Robot Framework is installed:

```powershell
python -m robot --version
```

### 4. Configure Your Test Account

Register a dedicated test account manually on Automation Exercise.

In the **same PowerShell terminal** in which you will run the tests, set:

```powershell
$env:RF_TEST_NAME = "Your Exact Account Name"

$env:RF_TEST_EMAIL = "your-existing-account@example.com"

$env:RF_TEST_PASSWORD = "your-password"
```

Replace the placeholders with your test account details.

**Important:** `RF_TEST_NAME` must match the name displayed by the website after login.

Never commit real credentials to GitHub.

---

## ▶️ Running the Tests

Execute the following commands from the project root directory.

### Run Login Tests

```powershell
python -m robot --outputdir Results TestSuites/02_login_tests.robot
```

### Run the Main CSV-Driven Business Flow

```powershell
python -m robot --outputdir Results --test "Complete Purchase Journey For Every Product In The Data File" TestSuites/03_ecommerce_business_flow.robot
```

### Run All Enabled Test Suites

```powershell
python -m robot --outputdir Results TestSuites/
```

### Run Both Main Test Files Explicitly

```powershell
python -m robot --outputdir Results TestSuites/02_login_tests.robot TestSuites/03_ecommerce_business_flow.robot
```

### Run Using the Windows Script

```powershell
.\run_tests.bat
```

The registration file has the `.disabled` extension and is not included in normal `.robot` test execution.

---

## 🔄 Automated Business Flow

```text
       Launch Browser
              |
              v
       Login to Account
              |
              v
        Read CSV Data
              |
              v
       Search for Product
              |
              v
       Add Product to Cart
              |
              v
         Verify Cart
              |
              v
     Process Next CSV Row
              |
              v
            Logout
              |
              v
        Close Browser
```

The main test logs in once, loops through the CSV search terms and logs out at the end.

The cart is cleared before each product iteration to prevent previously added products from affecting the next verification.

The workflow stops at cart verification. It does not process payments or place real orders.

---

## 📊 Data-Driven Testing

The project reads product search data from:

`TestData/search_products.csv`

```csv
search_term,min_expected_results
Dress,1
Top,1
Saree,1
```

### How It Works

1. Read the external CSV file.
2. Process each product search term.
3. Search the website for the product.
4. Select and add a matching product to the cart.
5. Verify the selected product in the cart.
6. Repeat for the remaining CSV rows.

The main CSV-driven scenario is implemented as **one reported Robot Framework test with multiple iterations**.

For separate Robot Framework test results for each CSV row, a test-template or DataDriver-based approach could be introduced.

> The CSV contains a `min_expected_results` column. The current search keyword checks that results are not empty; the threshold should not be described as independently validated unless that assertion is added to the test.

---

## 🧩 Page Object Model

The framework organizes page-specific operations into separate resource files.

| Resource File | Responsibility |
|---|---|
| `HomePage.resource` | Home page interactions |
| `LoginPage.resource` | Login functionality |
| `ProductsPage.resource` | Product search and add-to-cart actions |
| `CartPage.resource` | Cart interactions and verification |
| `SignupPage.resource` | Registration-related interactions |

Common keywords and shared variables are maintained in the `Resources` directory.

### Handling Dynamic Elements

During execution, advertisement overlays sometimes intercepted normal browser clicks.

The products page includes a fallback that attempts a normal Selenium click first and uses a JavaScript click when necessary.

Cart verification also normalizes whitespace in product names before comparison.

---

## 🖥️ RIDE Execution

RIDE provides a graphical environment for developing and executing Robot Framework tests.

Install a RIDE version compatible with your Python environment:

```powershell
python -m pip install robotframework-ride
```

Open the business-flow suite:

```powershell
.\.venv\Scripts\ride.exe .\TestSuites\03_ecommerce_business_flow.robot
```

Use the **Run** tab to execute the test and inspect the results.

---

## 🔧 Jenkins Integration

The project includes a Windows-compatible `Jenkinsfile` for pipeline execution.

### Pipeline Stages

```text
Verify Project Files
         |
         v
Create Virtual Environment
         |
         v
Install Dependencies
         |
         v
Execute Robot Framework Tests
         |
         v
Archive Test Artifacts
```

### Jenkins Requirements

- Jenkins with a compatible Java runtime
- A Windows Jenkins agent
- Python and Google Chrome
- Project files available in the Jenkins workspace
- Required Jenkins plugins for your pipeline configuration
- Jenkins secret-text credentials

### Credential IDs

Configure the following secret-text credentials in Jenkins:

| Credential ID | Purpose |
|---|---|
| `automationexercise-test-email` | Test account email |
| `automationexercise-test-password` | Test account password |

The pipeline injects these credentials into the environment as `RF_TEST_EMAIL` and `RF_TEST_PASSWORD`.

Set the test account name to match the account used during execution.

### Execution and Artifacts

The Jenkins pipeline executes the main business-flow test and archives generated artifacts, including HTML reports and XML results.

The successful capstone run was triggered manually in Jenkins. Automatic GitHub-triggered execution was not configured.

---

## 📈 Execution Results

The main CSV-driven business-flow test was successfully executed using the command line, RIDE and Jenkins.

| Execution Environment | Result |
|---|---|
| Command line | 1 passed, 0 failed |
| RIDE | 1 passed, 0 failed |
| Jenkins | 1 passed, 0 failed |

The successful business-flow execution verified products matching the three CSV search terms.

These results refer to the main business-flow test, not every possible test case in the repository.

### 📸 Execution Screenshots

Add screenshots of your actual execution results to a `Screenshots` directory.

<!-- Uncomment after adding the corresponding screenshot files.

### Terminal Execution

![Terminal Execution](Screenshots/terminal.png)

### RIDE Execution

![RIDE Execution](Screenshots/ride.png)

### Jenkins Pipeline

![Jenkins Pipeline](Screenshots/jenkins.png)

-->

---

## 📄 Test Reports

Robot Framework generates the following files inside the `Results` directory:

| File | Description |
|---|---|
| `report.html` | Overall test results and statistics |
| `log.html` | Detailed keyword execution log |
| `output.xml` | Machine-readable execution results |

Open the reports on Windows:

```powershell
start Results\report.html

start Results\log.html
```

The `Results` directory is excluded from Git tracking because reports are generated during execution.

---

## 📝 Notes and Limitations

- The registration suite is retained as `.disabled` for reference.
- A dedicated test account must be created manually before execution.
- Test credentials must be provided through environment variables.
- The main business flow performs cart verification, not checkout or payment.
- The CSV-driven workflow reports one Robot Framework test containing multiple product iterations.
- The live website may change its UI or selectors. Inspect `Results/log.html` if a test fails after a website update.
- The successful execution results reflect the tested environment and do not guarantee that every future run will pass.

---

## 🚀 Future Improvements

Potential enhancements include:

- Negative login and product-search scenarios
- Additional product categories
- Separate test results for individual CSV rows
- Custom Python keyword libraries
- Cross-browser testing
- Automatic Jenkins execution triggered by GitHub
- Additional reporting and test coverage

---

## 👩‍💻 Author

**Sayantana Halder**  
B.Tech in Computer Science and Engineering  
University of Engineering and Management, Kolkata

**GitHub:** [@sayantana12](https://github.com/sayantana12)

---

<div align="center">

**Built using Robot Framework, Python and SeleniumLibrary.**

⭐ If you find this project useful, consider starring the repository.

</div>