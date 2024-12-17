# atlaz

Welcome to the Atlaz library! We want to give you the best knowledge graphs and tools as possible to make your data extraction and RAG as simple as possible. It should be simple to build powerful AI applications.

## Installation

```bash
pip install atlaz
```

To use the visualize function you need a working local graphviz installation. This can be achieved by for example `brew install graphviz` depending on your machine.


```example_script.py
source_text = r"""<Your source data that you want to analyze>"""
customization = r"""<Your custom instruction to specify relationships you want to focus on and what objects to include. Can safely be ignored if you are unsure about this, I recommend generating the graph without first.>"""

# Initialize client
client = Atlaz(api_key=OPENAI_API_KEY)
# Build Knowledge Graph
response = client.build_graph(source_text=source_text, customization=customization)
# Render Graphviz Graph
visualize(response['graph'], 'test')
```

Go crazy! ;)