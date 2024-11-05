# Declarative Copilot Agent with authenticated API

To make the API work, add a .env file to the /ApiAgent/api folder with the following content:

```
API_KEY=your_api_key
```

Before running the API, create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r ApiAgent/api/requirements.txt
```

Run the API from the /ApiAgent/api folder:

```bash
python app.py
```

Check the blog post for more information: https://blog.baeke.info/2024/11/05/create-a-copilot-declarative-agent-that-calls-an-api-with-authentication/
