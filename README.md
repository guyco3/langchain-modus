# LangChain Modus Integration 🔗➗

LangChain integration for Modus logical constraint systems. Validate logical predicates and enforce business rules within your LLM applications. Could be useful in making LLM agents more accurate and with tagging objects more accurately (example tagging a refund request with either should approve or not with a reason also) using both deterministic rules + LLMs.
## Installation 💻
```bash
pip3 install -e .
```

## Quick Start 🚀

### Initialize Tools
```py
from langchain_modus.tools import create_modus_tools
```

Initialize with your Modus API key
```py
modus_tools = create_modus_tools(
api_key="your_modus_api_key",
base_url="https://api.modus.company/v1" # Optional for custom deployments
)
```

### Available Tools 🛠️

#### 1. Get Predicates Tool
Fetch available predicates for a project

```py
predicates = modus_tools.run({
"project_id": "your_project_id"
})
```

Example output:
```bash
[

{'alias': 'RecentOrder', 'content': 'Order was placed within last 30 days'},

{'alias': 'DamagedProduct', 'content': 'Product exhibits physical damage'}

]
```

#### 2. Validate Assignment Tool

Validate truth assignments against project constraints

```py
validation_result = modus_tools.run({
"project_id": "your_project_id",
"assignments": json.dumps({
"RecentOrder": True,
"DamagedProduct": False
})
})
```

Example valid output:
```bash
{"valid": true, "violations": []}
```

Example invalid output:
```bash
{"valid": false, "violations": ["RefundRequest requires RecentOrder AND NOT DamagedProduct"]}
```

## Key Components 🔐
### Schemas
- `GetPredicatesInput`: Requires `project_id` to fetch predicates
- `ValidateAssignmentInput`: Takes `project_id` and truth assignments dictionary

### Tools
- `GetPredicatesTool`: Retrieves available predicates and their definitions
- `ValidateAssignmentTool`: Validates truth assignments against Modus constraints
- Shared `ModusClient` handles API communication

## Error Handling ⚠️
Both tools return error dictionaries in this format when exceptions occur:
```py
{"error": "Descriptive error message"}
```

## Examples
Check out the examples dir

## Contributing 🤝
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📜
MIT License - See [LICENSE](LICENSE) for details