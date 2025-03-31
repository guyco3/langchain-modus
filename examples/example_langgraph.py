from langgraph import Graph, Node
from langgraph.nodes import LLMNode, ToolNode
from langchain.llms import AI21
from langchain_modus.langchain_modus import ModusPredicates, ModusValidate

# Initialize tools
tool1 = ModusPredicates(modus_api_key='123')
tool2 = ModusValidate(modus_api_key='123')

# Define a prompt to generate truth assignments based on predicates
prompt = "Generate a truth assignment for the following predicates: {predicates}."

# Create nodes
llm_node = LLMNode(
    llm=AI21(),
    prompt=prompt,
    input_variables=["predicates"],
    output_key="truth_assignments",
)

tool_node1 = ToolNode(tools=[tool1])
tool_node2 = ToolNode(tools=[tool2])

# Define the graph
graph = Graph(
    nodes=[
        tool_node1,
        llm_node,
        tool_node2,
    ],
    edges=[
        (tool_node1, llm_node),
        (llm_node, tool_node2),
    ],
)

# Run the graph
document_id = 12
result = graph.run({"document_id": document_id})
print(result)
