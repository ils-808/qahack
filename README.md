# QA Hackaton at https://qahack.net/

### Local Test Run
#### To run the tests in the CLI:
1. Pull the project
2. Install the latest version of Python. During installation, select Add python to PATH
3. Open the project in the CLI
4. Perform the steps below
##### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest --env=prod -n=2 --alluredir=./allure-results
```
##### *nix
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pytest --env=prod -n=2 --alluredir=./allure-results
```
> **Allowed variable values are:**<br>
> **env** - specifies the test execution environment: development(dev-gs.qa-playground.com) and production(release-gs.qa-playground.com).
> **n** - the number of parallel threads during execution.

#### To view the allure report, run in the CLI::
`allure serve`

### Running Tests in Github CI/CD
> write me to Discord, user: doingmybest_123. I'll add you as contributor, so you could run pipeline.

1. Open the  <a target="_blank" href="https://github.com/ils-808/qahack/actions/workflows/allure-report.yml">workflow</a> section
2. Click on `Run workflow'
3. In the `Environment to run the tests (dev or prod)`field, specify `dev` or `prod`
4. Click on `Run workflow'
5. Wait for the execution of both <a target="_blank" href="https://github.com/ils-808/qahack/actionsl">workflows</a>
   1. The first workflow - test execution
   2. The second workflow - generation of the allure report (GitHub Pages)
6. View the report in the published <a target="_blank" href="https://ils-808.github.io/qahack/">page</a>

> When the first workflow is executed, an allure report is also generated as artifact, TTL = 1 day.
> It can be downloaded and run with the command `allure generate ./allure-results -o ./allure-report --clean`
