import os
import logging
import streamlit as st
import requests

# Endpoint for the backend API
BACKEND_ENDPNT = os.environ.get("BACKEND_ENDPNT", "http://localhost:8000/ask")

# Logging
logging_dir = os.path.join("data", "logs")
os.makedirs(logging_dir, exist_ok=True)
log_file_name = 'Frontend_API.log'
logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(logging_dir, log_file_name),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info(f"Backend URL: {BACKEND_ENDPNT}")

def main():
    # Set page title and layout
    st.set_page_config(page_title="AI Help", layout="wide")
    
    st.balloons()  # Show balloons on page load

    # Title
    # st.title("LLM Assistant", anchor="center")
    st.markdown("<h1 style='text-align: center; color: white; font-size: 36px'>LLM Assistant</h1>", unsafe_allow_html=True)

    # Prompt input
    # st.markdown("<h1 style='text-align: left; color: white; font-size: 20px'>Prompt</h1>", unsafe_allow_html=True)
    prompt_input = st.text_input(label="Enter your prompt:", value="", max_chars=100)

    # Chat container and history container
    response_container = st.container()
    chat_history_container = st.container()

    # Load or initialize the chat history from session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Main logic for handling user input and displaying responses
    with response_container.container():
        try:
            if prompt_input:
                params = {"prompt": prompt_input}  # Set the query parameters
                response = requests.post(BACKEND_ENDPNT, params=params)
                if response.status_code == 200:

                    # Log the request details
                    logging.info(f"Request to {BACKEND_ENDPNT} finished with status code {response.status_code}")

                    response_json = response.json()
                    response_content = response_json.get('response', '')

                    # Append the new chat entry to the session state chat history
                    st.session_state.chat_history.insert(0, {
                        "prompt": prompt_input,
                        "response": response_content
                    })
                    
                    # Display the response using st.code
                    response_container.markdown("#### Response")
                    response_container.code(response_content, language=None, wrap_lines=True, height= 200)
                else:
                    # Log the request details
                    logging.info(f"Request to {BACKEND_ENDPNT} failed with status code {response.status_code}")
                    st.error(f"Request failed with status code {response.status_code}")
                
            else:
                # Display the response
                empty_response_box = "No response available. Please enter a prompt"
                response_container.markdown("#### Response")
                response_container.code(empty_response_box, language=None, wrap_lines=True, height= 200)

        except Exception as e:
            # Log the error
            logging.error(f"Error processing request: {str(e)}")
            st.error(f"Error fetching response: {str(e)}")

        # Display the chat history
        chat_history_container.markdown("#### Chat History")
        response_history = ""
        for entry in st.session_state.chat_history:
            response_history += f"Prompt: {entry['prompt']} \nResponse: {entry['response']} \n----------- \n"
        chat_history_container.code(response_history, language=None, wrap_lines=True, height= 250)

if __name__ == "__main__":
    main()
    # streamlit run frontend/app.py --server.port 8500 --server.address 0.0.0.0