from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_modus.langchain_modus import ModusPredicates, ModusValidate

# Initialize Gemini Flash model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Initialize Modus tools with your API key
modus_tools = [
    ModusPredicates(modus_api_key='123'),
    ModusValidate(modus_api_key='123')
]

# Create agent prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to Modus validation tools."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Create the agent
agent = create_tool_calling_agent(llm, modus_tools, prompt)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=modus_tools,
    verbose=True
)

# Example usage
document_id = 12
data = {
    "5226fbe4-0aa3-4a58-938d-378c70f2d9f9": True,
    "5226fbe4-0aa3-4a58-938d-378c70f2d9f8": True
}

# Get predicates
predicates_result = agent_executor.invoke({
    "input": f"Get predicates for document {document_id}"
})
print(predicates_result['output'])

# Validate assignments
validation_result = agent_executor.invoke({
    "input": f"Validate document {document_id} with assignments {data}"
})
print(validation_result['output'])
