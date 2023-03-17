# Flask-Pulumi-GitHub-Actions

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Welcome

Hello. Want to get started with Flask, Pulumi and GitHub Actions quickly? Good. You came to the right place. This repository contains the important parts of a GitOps Pipeline, tests, Continuous Integration and Continuous Deployment. All you have to do is input your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and PULUMI_ACCESS_TOKEN.


Project Structure
--------

  ```sh
  .
  ├── LICENSE
  ├── README.md
  ├── appspec.yml
  ├── infrastructure
  │   ├── Pulumi.accure.yaml
  │   ├── Pulumi.yaml
  │   ├── __main__.py
  │   └── requirements.txt
  ├── scripts
  │   └── execute.sh
  └── simple
      ├── accure.service
      ├── app.py
      ├── Dockerfile
      ├── nginx
      │   └── accure
      ├── requirements.txt
      ├── test_app.py
      └── wsgi.py

  ```

### Quick Start

#### Locally

1. Clone the repo
  ```
  $ git clone https://github.com/edeediong/Flask-Pulumi-GitHub-Actions.git
  $ cd Flask-Pulumi-GitHub-Actions
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)


#### Production

1. Clone the repo
  ```
  $ git clone https://github.com/edeediong/Flask-Pulumi-GitHub-Actions.git
  $ cd Flask-Pulumi-GitHub-Actions
  ```

2. Initialize pulumi
  ```
  pulumi stack init stack-name
  pulumi config set aws:region <value>
  ```

3. Create a `.pulumi` folder with a file called `ci.json`. This file is used to tell the Pulumi Action that the GitHub branch `main` is the branch for the stack created.
Below is the content of the file:
  ```JSON
  {
      "main": "<stack-name>"
  }
  ```

4. Also ensure the pip packages needed to execute your code are placed in `requirements.txt`. In this case the only package to be added is `pulumi_aws`.
5. Push code and watch entire GitOps Pipeline executed.

## GitOps Pipeline

### Introduction
This [article](https://www.gitops.tech/) explains the entire idea of GitOps. For this deployment, I used the following tools:
* GitHub Actions for the Continuous Integration part of the project (running tests)
* Pulumi for the Infrastructure as Code part of the project (provisioning the infrastructure)
* AWS CodeDeploy for Continuous Deployment, used in automating the deployment to the server
* AWS S3 to store the source code of the repository and push to AWS EC2.
* AWS EC2 to serve the source code
* AWS IAM to create access keys used by the repository.

