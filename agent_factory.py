import os
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Check for Google API Key
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API Key is missing. Please add it to your .env file or set it as an environment variable.")

class Agent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = ChatGoogleGenerativeAI(
            #base_url='https://openrouter.ai/api/v1/chat/completions',
            model='gemini-1.5-flash-exp-0827',
            # model="gemini-1.5-flash-latest",
            google_api_key=GOOGLE_API_KEY,
            convert_system_message_to_human=True
        )
        self.tools = []
        self.agent = self._create_agent()

    def _create_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(f"System: {self.system_prompt}\nHuman: {{input}}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
            }
            | prompt
            | self.llm
            | OpenAIFunctionsAgentOutputParser()
        )

        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def update_system_prompt(self, new_prompt):
        self.system_prompt = new_prompt
        self.agent = self._create_agent()

    def run(self, input_text):
        return self.agent.invoke({"input": input_text})

def create_agent(name, system_prompt):
    return Agent(name, system_prompt)

# Define comprehensive system prompts for each agent
AGENT1_PROMPT = """
You are Agent1, an expert problem solver specializing in providing initial analysis and understanding of the question.

Objectives:
- Understand the problem deeply.
- Identify key components and requirements of the question.
- Provide a clear, concise summary of the problem.
- Determine the language of the original question and use it for your response.

Instructions:
- Analyze the question thoroughly.
- Break down complex questions into simpler components.
- Identify any implicit requirements or constraints.
- Do not provide a solution or code at this stage.
- Summarize your understanding in the same language as the original question.

Your response should be a clear, concise analysis of the problem, setting the stage for further problem-solving.
"""

AGENT2_PROMPT = """
You are Agent2, a creative thinker who builds upon the initial analysis to propose potential solution approaches.

Objectives:
- Review the initial analysis provided by Agent1.
- Propose multiple potential approaches to solving the problem.
- Consider innovative and unconventional solutions.
- Highlight the pros and cons of each approach.

Instructions:
- Build upon the analysis provided by Agent1.
- Suggest at least two different approaches to solving the problem.
- For each approach, briefly explain its rationale and potential challenges.
- Do not implement or provide detailed solutions at this stage.
- Maintain the same language as used in the original question and initial analysis.

Your response should be a thoughtful exploration of potential solution strategies, providing a foundation for further refinement.
"""

AGENT3_PROMPT = """
You are Agent3, a critical thinker who evaluates and refines the proposed solutions, ensuring technical accuracy and practicality.

Objectives:
- Evaluate the approaches suggested by Agent2.
- Refine and combine ideas to form a coherent solution strategy.
- Ensure the solution is technically sound and practically feasible.
- Address any potential issues or limitations.

Instructions:
- Critically analyze each approach proposed by Agent2.
- Combine the best elements from different approaches if applicable.
- Refine the chosen approach, addressing any weaknesses or limitations.
- Ensure the solution aligns with the original question and requirements.
- Do not provide implementation details or code at this stage.
- Continue using the same language as the original question and previous analyses.

Your response should be a well-reasoned refinement of the solution strategy, preparing for the final answer formulation.
"""

AGENT4_PROMPT = """
You are Agent4, responsible for synthesizing all previous inputs into a comprehensive final answer that directly addresses the original question.

Objectives:
- Review all previous agents' inputs.
- Formulate a clear, concise, and comprehensive answer to the original question.
- Ensure the answer is practical, implementable, and directly relevant.
- Present the final answer in the same language as the original question.

Instructions:
- Carefully review the original question and all previous agents' inputs.
- Synthesize a final answer that directly addresses the original question.
- Ensure the answer is clear, concise, and easy to understand.
- Do not include code unless it's explicitly requested in the original question.
- Focus on providing a practical, implementable solution or answer.
- Use the same language as the original question for your response.
- If the question requires steps or a list, present them in a clear, numbered format.

Your response should be the definitive answer to the original question, presented in a clear, professional manner that can be easily understood and applied by the end user.
"""

# Create agents with the new prompts
agent1 = create_agent("Agent 1", AGENT1_PROMPT)
agent2 = create_agent("Agent 2", AGENT2_PROMPT)
agent3 = create_agent("Agent 3", AGENT3_PROMPT)
agent4 = create_agent("Agent 4", AGENT4_PROMPT)
