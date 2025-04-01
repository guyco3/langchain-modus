from langchain_modus import create_modus_tools
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DOCUMENT_ID = '67eafde0841aff119f4fd586'
MODUS_API_KEY = os.getenv("MODUS_API_KEY")
predicates_tool, validate_tool = create_modus_tools(api_key=MODUS_API_KEY)
tools = [predicates_tool, validate_tool]

# Set up Gemini Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

policy = """
Eligibility Requirements\n
To qualify for a refund:\n
✅ Order Recency: Your order must have been placed within the last 30 days.\n
✅ Product Condition: The item must show no signs of physical damage.\n
Refund Process\n
Submit your refund request through our Support Portal\n
Return the product in its original packaging\n
Refunds processed within 5 business days of receipt\n

Payment Recovery\n
Approved refunds will be credited to your original payment method.
"""

# Fixed prompt structure using MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""\
You are a helpful customer support assistant. You help users answer questions regarding a refund policy with project id {DOCUMENT_ID}.

When a user has a question relating to the policy:
1. Ask relevant questions to understand their problem
2. Call `modus_get_predicates` to get policy predicates
3. Assign truth values based on conversation
4. Validate assignments with `modus_validate_assignment`, try to set the predicate relating to their request as true firt

Refund Policy Context:
{policy}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent without legacy memory
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Configure modern memory handling
message_history = InMemoryChatMessageHistory()
conversational_agent = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

if __name__ == "__main__":
    print("Refund Policy Assistant (type 'exit' to quit)")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() == "exit":
                break
                
            response = conversational_agent.invoke(
                {"input": user_input, "policy_context": policy},
                config={"configurable": {"session_id": "user123"}}
            )
            print(f"\nAssistant: {response['output']}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            break
