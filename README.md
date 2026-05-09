# OCM LLM Chat Application

This is a minimal Organizational Change Management chat application that uses an LLM with a research-based OCM system prompt.

## Setup

1. Install Python 3.10+.
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Set your OpenAI API key in an environment file or directly in your environment:
   ```powershell
   $env:OPENAI_API_KEY = "your_api_key"
   ```

## Run

```powershell
python app.py
```
### Run the web app locally

```powershell
py -3 web.py
```

Then open `http://127.0.0.1:5000` in your browser.

> Note: `web.py` binds to `0.0.0.0` and uses the `PORT` environment variable, so it is ready for deployment to public hosting services.

Type a prompt and press Enter. Type `exit` or `quit` to stop.

## Behavior

The assistant answers using evidence-based research from I/O psychology, Prosci, ACMP, Kotter, ADKAR, Bridges, Lewin, and similar research-backed frameworks.

When asked for sources, it will cite the relevant framework or research foundation.

## Deploy to the web

To make this accessible with a public link, deploy `web.py` to a hosting service such as Render, Railway, or Fly.

1. Install dependencies locally:
   ```powershell
   py -3 -m pip install -r requirements.txt
   ```
2. Create a `.env` file with your API key:
   ```text
   OPENAI_API_KEY=your_api_key_here
   ```
3. Push the project to GitHub.
4. Use a platform like Render, Railway, or any container host and configure the start command:
   ```text
   py -3 web.py
   ```
5. Set `OPENAI_API_KEY` as an environment variable in the host settings.

### Public deployment options
- Render: create a Web Service, connect the GitHub repo, set `py -3 web.py` as the start command, and add `OPENAI_API_KEY` in Environment.
- Railway: create a new project, deploy from GitHub, set `py -3 web.py` as the start command, and add `OPENAI_API_KEY` in Environment.
- Docker hosts: build the included `Dockerfile`, then run the container with `PORT` and `OPENAI_API_KEY` configured.
- DigitalOcean App Platform: use the included `app.yaml` spec to deploy the repo.

## Deploy on DigitalOcean App Platform
1. Push this project to GitHub.
2. Install `doctl` and authenticate with your DigitalOcean account:
   ```powershell
   doctl auth init
   ```
3. Create a DigitalOcean API token and set it during authentication.
4. Edit `app.yaml` and replace `YOUR_GITHUB_USERNAME/REPO_NAME` with your actual GitHub repo path.
5. Deploy the app using DigitalOcean App Platform:
   ```powershell
   doctl apps create --spec app.yaml
   ```
6. In the DigitalOcean dashboard or `app.yaml`, ensure `OPENAI_API_KEY` is set as a runtime environment variable.

> Note: DigitalOcean App Platform has limited free support for dynamic apps. If you are using the free tier, you may need trial credit or a low-cost Starter/Basic instance to run this Flask application publicly.
