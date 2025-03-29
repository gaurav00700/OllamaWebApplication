## LLM Web application using Ollama


### Introduction

This repository contains a web application that allows users to interact with large language models (LLMs) through an intuitive interface. The application is built using Streamlit. It connects to an Ollama backend server, which provides access to various LLMs. CI/CD is implemented to automate the build and deployment process, ensuring that the application is always up-to-date. Application Orchestration is implemented used Kubernetes

### Features

- **User Interface**: A simple and intuitive interface for users to input queries and receive responses from LLMs.
- **LLM Selection**: Users can select different LLMs available on the [Ollama](https://ollama.com/search) backend server.
- **Inference Speed**: The application leverages Docker Compose to run the frontend and backend services, which can be optimized for faster inference using GPU support if available.
- **Cache**: Redis is used as a caching mechanism to store frequently accessed queries and responses, reducing redundant computations.
- **CI/CD**: Continuous Integration and Continuous Deployment (CI/CD) is implemented using GitHub Actions to automate the build and deployment process.
- **Orchestration**: Application Orchestration is implemented using Kubernetes running on multi node compute environment.

### Preview
Application Architecture |
:-------------------------:
<img src="assets/architecture.png" style="display: block; margin-left: auto; margin-right: auto; max-width: 55%; height: auto;">

Frontend Interface |
:-------------------------:
<img src="assets/frontend.png" style="display: block; margin-left: 415px; margin-right: auto; max-width: 55%; height: auto;" >

### Prerequisites
- Docker
- Docker Compose 
- GPU support for faster inference if you have one available.
  
### Installation and Usage

1. Clone the repository: `git clone git@github.com:gaurav00700/OllamaWebApplication.git`
2. Navigate to the project directory: `cd OllamaWebApplication`
3. Deployment and Orchestration: `kubectl apply -f k8s`
4. (Optional) Run the docker-compose command to start the application: `docker-compose up -d` 
   
   (Change the LLM_NAME in `.env` file according to your preference.)