## Streamlit Chatbot with Hugging Face LLM and Tool Support

This project is a conversational chatbot built using Streamlit and the Hugging Face Mistral-7B-Instruct-v0.3 language model. The chatbot has enhanced capabilities, including integrating external tools for web searching via SerpAPI. Users can control whether the chatbot uses these tools, and the usage of tools is dynamically displayed in the interface. The application is containerized using Docker and can be deployed with Kubernetes.

### Features

- **LLM-based chatbot**: Powered by Hugging Face's `Mistral-7B-Instruct-v0.3` model.
- **Tool integration**: The chatbot can use external tools (e.g., web search through SerpAPI) to assist with answering questions.
- **Dynamic tool usage control**: The user can instruct the chatbot to either use or avoid external tools.
- **Streamlit GUI**: A user-friendly web interface where users can interact with the chatbot.
- **Docker support**: Easily deploy the chatbot in a containerized environment using Docker.
- **Kubernetes support**: Scale and manage the application using Kubernetes.

### Requirements

- Docker
- Kubernetes
- Python 3.10 or higher
- Hugging Face API token (required for accessing gated models)
- SerpAPI key (required for web search functionality)

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/streamlit-chatbot.git
cd streamlit-chatbot
```
#### 2. Set up your environment
You can use a virtual environment or conda to isolate the project dependencies.
```bash
python3 -m venv chatenv
source chatenv/bin/activate
```
#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Get your Hugging Face API token
This project uses Hugging Face’s Mistral-7B-Instruct-v0.3 model, which is gated. You need to get an API token:

	- Visit Hugging Face.
	- Log in or create an account.
	- Navigate to your profile settings and generate an API token.
	- Copy your token.

#### 5. Get your SerpAPI key
SerpAPI is used to perform web searches in the chatbot. You need to generate an API key from SerpAPI:

	- Visit SerpAPI.
	- Log in or sign up for an account.
	- Navigate to your account dashboard and generate an API key.
	- Copy your SerpAPI key.

#### 6. Add your API keys
You need to set the environment variables `HUGGINGFACEHUB_API_TOKEN` and `SERPAPI_KEY` to authenticate with Hugging Face and SerpAPI.
#### Using the `.env` file (optional)
Create a `.env` file in the project directory:
```bash
echo "HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here" > .env
echo "SERPAPI_KEY=your_serpapi_key_here" >> .env
```
Or, export the tokens directly in your shell (replace your_huggingface_token_here and `your_serpapi_key_here` with your actual tokens):
```bash
export HUGGINGFACEHUB_API_TOKEN="your_huggingface_token_here"
export SERPAPI_KEY="your_serpapi_key_here"
```
         
### Running the Project
#### 1. Run locally with Streamlit
Once everything is set up, you can run the app locally using Streamlit:
```bash
streamlit run app.py
```
Open your browser and go to `http://localhost:8501` to interact with the chatbot.
       
#### 2. Run with Docker
Build the Docker image
```bash
docker build -t streamlit-chatbot .
```
Run the Docker container
```bash
docker run -p 8501:8501 streamlit-chatbot
```
Access the app on `http://localhost:8501` from your browser.
       
### Kubernetes Deployment
To scale the app and run it across multiple containers, you can deploy it using Kubernetes.

#### Prerequisites
- Kubernetes cluster set up (e.g., Minikube or cloud provider)
- `kubectl` installed and configured

### Steps
#### 1. Build and push your Docker image to a container registry (like Docker Hub).
```bash
docker tag streamlit-chatbot your-dockerhub-username/streamlit-chatbot
docker push your-dockerhub-username/streamlit-chatbot
```
#### 2. Create Kubernetes `deployment` & `service` files (deployment.yaml).
#### 3. Create Kubernetes secrets for your Hugging Face and SerpAPI tokens:
```bash
kubectl create secret generic huggingface-secret --from-literal=HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
kubectl create secret generic serpapi-secret --from-literal=SERPAPI_KEY=your_serpapi_key_here
```

#### 4. Deploy the application
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```             

#### 5. Deploy the secret:
```bash
kubectl apply -f secret.yml
```

#### 6. Expose the deployment as a service:
```bash
kubectl expose deployment streamlit-chatbot --type=LoadBalancer --port=80 --target-port=8501
``` 
Now you can access your app through the `Kubernetes service URL`.




