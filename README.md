# Supabase Inactive Fix

![GitHub stars](https://img.shields.io/github/stars/travisvn/supabase-inactive-fix?style=social)
![GitHub forks](https://img.shields.io/github/forks/travisvn/supabase-inactive-fix?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/travisvn/supabase-inactive-fix)
![GitHub top language](https://img.shields.io/github/languages/top/travisvn/supabase-inactive-fix)
![GitHub last commit](https://img.shields.io/github/last-commit/travisvn/supabase-inactive-fix?color=red)

This project helps prevent Supabase projects from pausing due to inactivity by periodically inserting, monitoring, and deleting entries in the specified tables of multiple Supabase databases. The project uses a configuration file (`config.json`) to define multiple databases and automate the keep-alive actions.

## Features ⭐️

- Insert a random string into a specified table for each Supabase database.
- Monitor the number of entries in the table.
- Automatically delete entries if the table contains more than a specified number of records.
- Log successes and failures, and generate a detailed status report.

## Setup 🚀

> **💡 Quick Start:** For the easiest setup, skip to [Deployment Options](#deployment-options-) and use **GitHub Actions** (serverless, no installation required).

### Local Development Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/travisvn/supabase-inactive-fix.git
    cd supabase-inactive-fix
    ```
    
2. Install the required dependencies:
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    
3. Create a `config.json` file in the project root. This file defines your Supabase databases. 

   
    Example configuration:
    
    ```json
    [
      {
        "name": "Database1",
        "supabase_url": "https://your-supabase-url-1.supabase.co",
        "supabase_key_env": "SUPABASE_KEY_1",  // Use environment variable for the key
        "table_name": "KeepAlive"
      },
      {
        "name": "Database2",
        "supabase_url": "https://your-supabase-url-2.supabase.co",
        "supabase_key": "your-direct-supabase-key",  // Directly define the key
        "table_name": "keep-alive"
      }
    ]
    ```

    [See the section below for how to easily configure your database](#supabase-database-setup-)
    
    ### Environment Variables Explained
    
    In the `config.json` file, you can define either:
    
    - **Direct API Key**: Use the `"supabase_key"` field to directly specify your Supabase API key.
    - **Environment Variable**: Use the `"supabase_key_env"` field to reference an environment variable where the key is stored. This is more secure, especially when running the script in different environments.
    
    #### Example:
    
    - `"supabase_key_env": "SUPABASE_KEY_1"`: This tells the script to look for an environment variable called `SUPABASE_KEY_1` that contains the actual API key.
    - `"supabase_key": "your-direct-supabase-key"`: This directly provides the API key within the `config.json` file, which is less secure but simpler for local setups.

4. Set up your environment variables _if you're using them_:
    
    Create a `.env` file and store variables there
    
    ```
    SUPABASE_KEY_1="your-supabase-key-1"
    SUPABASE_KEY_2="your-supabase-key-2"
    ```
    
5. Run the script:
    
    ```bash
    python main.py
    ```

## Deployment Options 🚀

### Option 1: GitHub Actions (Recommended - Serverless)

The easiest way to deploy this project is using GitHub Actions, which runs completely serverless and free on GitHub's infrastructure.

#### Steps:

1. **Fork this repository** to your GitHub account.

2. **Create your `config.json`** file:
   - Copy `config.example.json` to `config.json`
   - Update with your Supabase project URLs and table names
   - Use `supabase_key_env` (not `supabase_key`) to reference environment variables

   ```json
   [
     {
       "name": "MyProject",
       "supabase_url": "https://your-project-id.supabase.co",
       "supabase_key_env": "SUPABASE_KEY_1",
       "table_name": "keep-alive"
     }
   ]
   ```

3. **Commit and push your `config.json`** to your forked repository.

4. **Set up GitHub Secrets and Variables**:
   - Go to your forked repository on GitHub
   - Navigate to **Settings** > **Secrets and variables** > **Actions**

   **First, enable the workflow (Variables tab):**
   - Click the **Variables** tab
   - Click **New repository variable**
   - Name: `ENABLE_GITHUB_ACTIONS`
   - Value: `true`

   **Then, add your API keys (Secrets tab):**
   - Click the **Secrets** tab
   - Click **New repository secret**
   - Add secrets for each database (matching the env var names in your `config.json`):
     - Name: `SUPABASE_KEY_1`
     - Value: Your Supabase API key
   - Repeat for all your databases (`SUPABASE_KEY_2`, `SUPABASE_KEY_3`, etc.)

5. **Enable GitHub Actions**:
   - Go to the **Actions** tab in your forked repository
   - Click "I understand my workflows, go ahead and enable them"

6. **Test the workflow**:
   - In the Actions tab, select "Supabase Keep-Alive"
   - Click "Run workflow" to test it manually
   - Check the logs to ensure everything works

**That's it!** The workflow will automatically run every Monday and Thursday at midnight UTC, keeping your Supabase databases active.

> **📝 Note for Existing Users:** If you're currently using a local cron job and pull this update, the GitHub Actions workflow will NOT run automatically. It only activates when you explicitly set the `ENABLE_GITHUB_ACTIONS` variable to `true`. You can:
> - **Keep using your cron job**: Do nothing, the workflow stays disabled
> - **Switch to GitHub Actions**: Follow the setup steps above and disable your cron job
> - **Use both** (not recommended): Enable both, but adjust schedules to avoid conflicts

#### Customizing the Schedule

Edit `.github/workflows/keep-alive.yml` and modify the cron expression:

```yaml
schedule:
  - cron: '0 0 * * 1,4'  # Currently: Monday and Thursday at midnight UTC
```

### Option 2: Local Cron Job

If you prefer to run the script on your own machine or server, you can set up a cron job.

1. Follow the initial setup steps 1-4 from the main [Setup](#setup-) section above.

2. Set up a cron job (see [Cron Job Setup](#cron-job-setup-%EF%B8%8F) below for details).

## Supabase Database Setup 🔧

This project is predicated on accessing a `keep-alive` table in your Postgres database on Supabase. 

### Sample SQL 

Here's a SQL query for a `keep-alive` table 

```sql
CREATE TABLE "keep-alive" (
  id BIGINT generated BY DEFAULT AS IDENTITY,
  name text NULL DEFAULT '':: text,
  random uuid NULL DEFAULT gen_random_uuid (),
  CONSTRAINT "keep-alive_pkey" PRIMARY key (id)
);

INSERT INTO
  "keep-alive"(name)
VALUES
  ('placeholder'),
  ('example');
```
    

## Cron Job Setup ⏱️

To automate this script, you can create a cron job that runs the script periodically. Below are instructions for setting this up on macOS, Linux, and Windows.

### macOS/Linux

1. Open your crontab file for editing:
    
    ```bash
    crontab -e
    ```
    
2. Add a new cron job to run the script every Monday and Thursday at midnight:
    
    ```bash
    0 0 * * 1,4 cd /path/to/your/project && /path/to/your/project/venv/bin/python main.py >> /path/to/your/project/logfile.log 2>&1
    ```
    

This example cron job will:

- Navigate to the project directory.
- Run the Python script using the virtual environment.
- Append the output to a logfile.

For reference, here’s an example used in development:

```bash
0 0 * * 1,4 cd /Users/travis/Workspace/supabase-inactive-fix && /Users/travis/Workspace/supabase-inactive-fix/venv/bin/python main.py >> /Users/travis/Workspace/supabase-inactive-fix/logfile.log 2>&1
```

### Windows (Task Scheduler)

Windows does not have cron jobs, but you can achieve similar functionality using Task Scheduler.

1. Open **Task Scheduler** and select **Create Basic Task**.
    
2. Name the task and set the trigger to run weekly.
    
3. Set the days (e.g., Monday and Thursday) and time (e.g., midnight) when the script should run.
    
4. In the **Action** step, select **Start a Program**, and point it to your Python executable within your virtual environment. For example:
    
    ```vbnet
    C:\path\to\your\project\venv\Scripts\python.exe
    ```
    
5. In the **Arguments** field, specify the path to the script:
    
    ```vbnet
    C:\path\to\your\project\main.py
    ```
    
6. Save the task. The script will now run automatically according to the schedule you specified.
    

## Contribution

Feel free to open an issue or submit a pull request if you'd like to contribute to this project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
