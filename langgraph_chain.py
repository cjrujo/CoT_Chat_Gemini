from typing import Dict, List
from langchain.schema import AIMessage, HumanMessage

def create_sequential_chain(agents):
    def run_chain(input_text: str, chat_history: List[Dict[str, str]] = None):
        if chat_history is None:
            chat_history = []
        
        # Convert chat history to a format that agents can use
        formatted_history = []
        for message in chat_history:
            if message["role"] == "user":
                formatted_history.append(HumanMessage(content=message["content"]))
            elif message["role"] == "assistant":
                formatted_history.append(AIMessage(content=message["content"]))
        
        agent_outcomes = {}
        current_input = input_text

        for i, agent in enumerate(agents):
            agent_name = f"Agent {i+1}"
            try:
                # Pass both the current input and the chat history to the agent
                result = agent.run({"input": current_input, "chat_history": formatted_history})
                agent_outcomes[agent_name] = result
                
                if i < len(agents) - 1:
                    # For all agents except the last one, update the input for the next agent
                    current_input = f"Original question: {input_text}\n\nPrevious analysis: {result}\n\nBased on this information and the chat history, please provide your analysis or improvement."
            
            except Exception as e:
                agent_outcomes[agent_name] = f"Error: {str(e)}"
                # If an agent fails, we'll still try to continue with the next one
                current_input = f"Original question: {input_text}\n\nPrevious agent encountered an error. Please provide your best analysis or response based on the original question and chat history."

        # The final output will be the response from the last agent
        final_output = agent_outcomes[f"Agent {len(agents)}"]
        
        return {
            "output": final_output,
            "agent_outcomes": agent_outcomes
        }
    
    return run_chain