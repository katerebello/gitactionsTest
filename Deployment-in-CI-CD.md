# Deployment in CI/CD

You can use a variety of events to trigger your deployment workflow. Some of the most common are: `pull_request`, `push`, and `workflow_dispatch`.

Deployment platforms-

- **GitHub Pages** is suitable for **static websites** built with HTML, CSS, JavaScript, or frameworks like **React** (since React apps can be built into static files).
- **GitHub Pages does not support server-side code** like Python, PHP, or Node.js, so it cannot directly run server-based applications. Need a platform that supports running server code.
- For server-side applications, options like **Heroku**, **Pythonanywhere, Render**, **Vercel** (for Node.js), and **DigitalOcean** are good alternatives because they support running backend code in Python, Node.js, and other languages.

## PythonAnywhere-

### Steps to Deploy a Flask App on PythonAnywhere

### Step 1: Sign Up or Log In to PythonAnywhere

1. Visit [PythonAnywhere](https://www.pythonanywhere.com/) and log in (or create a new account if you don’t have one).
2. After logging in, go to your **Dashboard**.

### Step 2: Create a New Web App

1. In the top menu, click the **Web** tab (note that with the free version, you can only create one app).
2. Click **Add a new web app**.
3. When prompted, choose **Flask** as the framework and select the Python version that matches the version used for your Flask app.
4. Proceed by clicking **Next** without making any other changes.

### Step 3: Set Up Your Flask App

1. Navigate to the **Files** tab to view the default files.
2. Open a **Bash console** and clone your Flask app’s Git repository.
3. Once the repository is cloned, go to the **Web** tab and change the **Source Code** path to point to the directory where your repository was cloned, instead of the default `mysite` folder.
4. Leave the **Working Directory** as the default.
5. Edit the **WSGI configuration file**:
    - Update the path to use your project’s folder instead of `mysite`.
    - In the WSGI file, change the import statement to reflect your app’s name (e.g., change `flask_app` to `app`, depending on your file name).
6. Click **Reload** to deploy the app.

### Step 4: Set Up Continuous Deployment (Workaround for Free Version)

1. With the free version of PythonAnywhere, SSH access isn’t available, so you can’t execute commands directly via GitHub Actions.
2. Instead, set up the GitHub Actions workflow to trigger on code pushes:
    - Create a GitHub Actions `.yml` file that will automatically pull the latest code and push it to PythonAnywhere after changes are made.
    - Use a workaround where you manually pull the latest code from PythonAnywhere to trigger the workflow, making the necessary changes and pushing them back.

Here’s an example GitHub Actions workflow for continuous deployment:

```yaml

name: Deploy PythonAnywhere Web App

on:
  push:
    branches:
      - main  # or your preferred branch

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      # Upload files here (if needed)

      - name: Reload web app
        uses: jensvog/pythonanywhere-webapp-reload-action@v1
        with:
          host: 'www.pythonanywhere.com'
          username: ${{ secrets.PYTHONANYWHERE_USERNAME }}
          api-token: ${{ secrets.PYTHONANYWHERE_API_TOKEN }}
          domain-name: ${{ secrets.PYTHONANYWHERE_DOMAIN_NAME }}
```

### Step 5: Get PythonAnywhere API Tokens

1. To use the PythonAnywhere API in your GitHub Actions workflow, you need an **API token**.
2. **Generate the token**:
    - Log in to your PythonAnywhere account.
    - Go to the **Account** page from the **Dashboard**.
    - Scroll down to the **API token** section and click on **Create a new API token**.
    - Copy the API token that is generated.
3. **Add the API token to GitHub Secrets**:
    - Go to your GitHub repository.
    - Under **Settings**, click **Secrets** in the left sidebar.
    - Click **New repository secret**.
    - Add a new secret with the name `PYTHONANYWHERE_API_TOKEN` and paste the token you copied from PythonAnywhere.
4. Also, add your **username** and **domain name** as secrets (`PYTHONANYWHERE_USERNAME` and `PYTHONANYWHERE_DOMAIN_NAME`), following the same process as above.

## Heroku - 

To deploy a Flask app to Heroku using GitHub Actions, follow these steps:

### 1. Prepare Your Flask App for Deployment

1. **Add a `Procfile`** in the root directory of your project to specify the command to run the app on Heroku:
    
    ```
    web: gunicorn app:app
    ```
    
    - Replace `app:app` with the path to your main Flask app file. For example, if your file is named `main.py`, this would be `web: gunicorn main:app`.
2. **Update `requirements.txt`** with all dependencies:
    - Run the following to update:
        
        ```bash
        pip freeze > requirements.txt
        ```
        
3. **Create a `runtime.txt`** file to specify the Python version:
    
    ```
    python-3.9.7
    ```
    
    - Replace the version with the one you’re using.

### 2. Set Up Heroku

1. **Create a Heroku Account** (if you don’t already have one) and install the Heroku CLI.
2. **Create a new Heroku app**:
    
    ```bash
    heroku create your-app-name
    ```
    
3. **Get the Heroku API Key**:
    - Go to **Heroku Dashboard > Account Settings**.
    - Under "API Key," click **Reveal** and copy the key.

### 3. Set Up GitHub Repository Secrets

1. **Go to your GitHub repository** and navigate to **Settings > Secrets and variables > Actions**.
2. Add the following secrets:
    - `HEROKU_API_KEY`: The API key you copied from Heroku.
    - `HEROKU_EMAIL`: Your Heroku account email.
    - `HEROKU_APP_NAME`: The name of your Heroku app.

### 4. Create GitHub Actions Workflow File

In your GitHub repository, create a new file at `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Heroku

on:
  push:
    branches:
      - main  # Deploys when changes are pushed to the main branch

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Check out the code
        uses: actions/checkout@v3

      - name: Deploy to Heroku
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
          HEROKU_EMAIL: ${{ secrets.HEROKU_EMAIL }}
          HEROKU_APP_NAME: ${{ secrets.HEROKU_APP_NAME }}
        run: |
          git remote add heroku https://git.heroku.com/${{ secrets.HEROKU_APP_NAME }}.git
          git push heroku main -f
```

### 5. Commit and Push

Commit your changes and push to the main branch (or whichever branch you’ve specified in the workflow). This will trigger the GitHub Action, which will then deploy your Flask app to Heroku.

### Additional -

- **Adjust Workflow Triggers**: If you want to deploy on different triggers (e.g., pull requests, tags), adjust the `on` section of the workflow file accordingly.
- **Check Deployment Logs**: In case of errors, check the logs in GitHub Actions and Heroku’s activity logs to troubleshoot.