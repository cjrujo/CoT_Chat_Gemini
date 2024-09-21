# Chain-of-Thought Chat App

This is a Streamlit-based chat application that uses a sequential chain of four specialized agents to create a Chain-of-Thought conversation using the Gemini-1.5-flash-latest model.

## Features

1. Four agents in a sequential workflow, each with a specific role and comprehensive system prompt:
   - Agent 1: Initial problem analyzer
   - Agent 2: Creative solution strategist
   - Agent 3: Critical evaluator and refiner
   - Agent 4: Final answer synthesizer
2. Customizable system prompts for each agent via the sidebar.
3. Main window chatbox for user input and final AI responses.
4. Display of the final consolidated answer in the same language as the user's question.
5. Ability to ask follow-up questions with context from previous interactions.
6. Expandable section to view the full inference process from all agents.
7. Retry mechanism with exponential backoff for API calls to handle temporary connection issues.

## Workflow

The application uses a sequential chain of agents, each building upon the work of the previous:

1. Agent 1: Analyzes and breaks down the original question, identifying key components and requirements.
2. Agent 2: Proposes potential solution approaches based on the initial analysis.
3. Agent 3: Evaluates and refines the proposed solutions, ensuring technical accuracy and practicality.
4. Agent 4: Synthesizes all previous inputs into a comprehensive final answer that directly addresses the original question.

Each agent receives the original question along with the previous agent's analysis and the chat history, ensuring a coherent chain of thought and context-aware responses.

## Key Improvements

- The final answer is provided in the same language as the user's original question.
- Python code is only included in the response if explicitly requested in the original question.
- The final answer directly addresses the original question, rather than just reviewing previous agents' inputs.
- Follow-up questions are now handled with full context from previous interactions.
- Implemented a retry mechanism with exponential backoff for API calls to handle temporary connection issues.

## Setup

1. Make sure you have Python 3.11 installed on your system.

2. Clone this repository and navigate to the project directory:

   ```
   git clone <repository-url>
   cd cot_chat_app
   ```

3. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Set up your Google API key:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Gemini API for your project.
   - Create credentials (API key) for the Gemini API.
   - Copy your API key.

6. Create a .env file in the project root and add your Google API key:

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

   **Important:** Replace `your_api_key_here` with your actual Google API key. The application will not work without a valid API key.

   Alternatively, you can set the GOOGLE_API_KEY as an environment variable in your system.

## Running the Application

To run the Streamlit app, execute the following command in your terminal:

```
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Usage

1. Enter your questions or prompts in the chat input at the bottom of the main window.
2. View the AI's final consolidated answer in the chat area, properly formatted and in the same language as your question.
3. Ask follow-up questions naturally, and the AI will consider the context from previous interactions.
4. To see the full inference process, including responses from all agents, click on the "See inference process" expander below the chat.
5. Customize agent system prompts using the sidebar on the left.
6. Use the "Set Agent" buttons to update individual agent prompts.
7. Click "Restore Defaults" to reset all agent prompts to their original, comprehensive versions.

## Error Handling and Retry Mechanism

The application now includes a retry mechanism with exponential backoff for API calls. If there's a temporary connection issue or the API fails to respond:

1. The app will automatically retry the API call up to 3 times.
2. There will be an increasing delay between retry attempts to avoid overloading the API.
3. If the API still fails after 3 attempts, you'll see an error message asking you to try again later.
4. In case of persistent issues, you'll be advised to check your internet connection or contact support.

## Verification

To verify that your setup is correct and the application is working as expected, follow these steps:

1. Run the application using `streamlit run app.py`.
2. If you see the chat interface without any error messages, your basic setup is correct.
3. Try entering a complex question that requires multi-step reasoning, like "What are the potential long-term effects of artificial intelligence on global job markets, and how can societies prepare for these changes?"
4. If you receive a response from the AI that directly answers your question without unnecessary code and in the same language you used, your setup is working correctly.
5. Ask a follow-up question related to the previous answer to verify that the context is maintained.
6. Check the "See inference process" expander to verify that all four agents are contributing to the response in sequence, each building upon the previous agent's output.
7. If you encounter any API connection issues, observe if the app attempts to retry the connection before showing an error message.

## Troubleshooting

If you encounter any issues, try the following:

1. **API Key Error**: 
   - Ensure your Google API key is correctly set in the .env file or as an environment variable.
   - Verify that you've activated the Gemini API for your Google Cloud project.
   - Check if your API key has the necessary permissions to use the Gemini API.

2. **Module Not Found Errors**: Make sure you've installed all required dependencies by running `pip install -r requirements.txt` in your virtual environment.

3. **Streamlit Command Not Found**: If the `streamlit` command is not recognized, try reinstalling it with `pip install streamlit`.

4. **Connection Errors**: 
   - Check your internet connection.
   - Ensure that your firewall is not blocking the application's access to the Google API.
   - If you see a message about retrying, wait for the app to complete its retry attempts.
   - If the error persists after multiple retries, try again later as there might be temporary API issues.

5. **Unexpected Behavior**: If the agents are not responding as expected, try resetting their prompts to default using the "Restore Defaults" button in the sidebar.

6. **Version Conflicts**: If you experience issues related to library versions, make sure you're using the versions specified in the requirements.txt file. If conflicts persist, try creating a new virtual environment and reinstalling the dependencies.

7. **Error Messages**: If you see error messages in the chat interface, check the console for more detailed error logs. These can be helpful when reporting issues.

If problems persist after trying these steps, please check the project's issue tracker or submit a new issue with a detailed description of the problem you're experiencing, including any error messages from the console.

## Known Limitations

- The Gemini model may have limitations in handling certain types of queries or generating specific formats of output. If you encounter unexpected responses, try rephrasing your question or prompt.
- The application currently doesn't support file uploads or processing of external data sources.
- Very long conversations may encounter token limits. If this happens, try starting a new conversation.
- Despite the retry mechanism, there might be cases where the API is consistently unavailable. In such cases, you'll need to try again later.

Enjoy using the Chain-of-Thought Chat App!