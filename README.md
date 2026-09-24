# E-commerce Robot Framework capstone (existing-account edition)

The registration suite is preserved as `.disabled` for reference but is **not** required by the assigned business flow. Register your test account manually first. Do not use the registration suite for the main demonstration.

## Windows quick start

1. Open this folder in VS Code, run `py -m venv .venv`, then `.\.venv\Scripts\Activate.ps1` and `pip install -r requirements.txt`.
2. Set `$env:RF_TEST_NAME = "Sayantana Halder"`, `$env:RF_TEST_EMAIL = "your-existing-account@example.com"`, `$env:RF_TEST_PASSWORD = "your-password"` in the **same** PowerShell window. Use the exact name displayed after login.
3. Run `robot --outputdir Results TestSuites/02_login_tests.robot`.
4. Run `robot --outputdir Results --test "Complete Purchase Journey For One Product" TestSuites/03_ecommerce_business_flow.robot`.
5. Run `robot --outputdir Results TestSuites/02_login_tests.robot TestSuites/03_ecommerce_business_flow.robot` or `run_tests.bat`.
6. Open `Results/report.html` and `Results/log.html`.

The data-driven test reads `TestData/search_products.csv`. It loops over CSV rows in one reported Robot test; for separate test results per row, use a test-template/data-driver library. The cart is emptied before each journey and verifies the exact chosen product name.

RIDE: install a compatible RIDE version in a supported Python environment, open `TestSuites` and run the tests. Jenkins: use the supplied Windows `Jenkinsfile` with a Windows-labelled agent, Python, Chrome, the Robot Framework Jenkins plugin and Jenkins secret-text credentials IDs `automationexercise-test-email` and `automationexercise-test-password`. Change the agent label if yours differs.

**Verification:** Static review only; no live website browser test was performed in the authoring environment. Inspect `Results/log.html` if the live site's UI or selectors have changed.
