# QA Hackaton at https://qahack.net/

### Local Test Run
#### To run the tests in the CLI:
1. Pull the project
2. Install Python 3.12 During installation, select Add python to PATH
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
sudo apt install -y python3-pip
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
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

1. Open the  <a target="_blank" href="https://github.com/ils-808/qahack/actions/workflows/allure-report.yml">workflow</a> `.github/workflows/allure-report.yml` section
2. Click on `Run workflow'
3. In the `Environment to run the tests (dev or prod)`field, specify `dev` or `prod`
4. Click on `Run workflow'
5. Wait for the execution of both <a target="_blank" href="https://github.com/ils-808/qahack/actions">workflows</a>
   1. The `.github/workflows/allure-report.yml` - executes test
   2. The `pages-build-deployment` - publihes the allure report (via GitHub Pages)
6. View the report in the published <a target="_blank" href="https://ils-808.github.io/qahack/">page</a>

> When the first workflow is executed, an allure report is also generated as artifact, TTL = 1 day.
> It can be downloaded and run with the command `allure generate ./allure-results -o ./allure-report --clean`

##### Example of pipeline runned successfully on PROD env
 <a target="_blank" href="https://github.com/ils-808/qahack/actions/runs/12120259622">Test Execution pipeline</a> <br>
 <a target="_blank" href="https://github.com/ils-808/qahack/actions/runs/12120278025">Report publishing pipeline</a> <br>
 <a target="_blank" href="https://ils-808.github.io/qahack/98/index.html">Generated report</a> <br>
 
 
##### Example of pipeline runned unsuccessfully on DEV env
 <a target="_blank" href="https://github.com/ils-808/qahack/actions/runs/12120341148">Test Execution pipeline</a> <br>
 <a target="_blank" href="https://github.com/ils-808/qahack/actions/runs/12120360228">Report publishing</a> <br>
 <a target="_blank" href="https://ils-808.github.io/qahack/100/index.html">Generated report</a> <br>
