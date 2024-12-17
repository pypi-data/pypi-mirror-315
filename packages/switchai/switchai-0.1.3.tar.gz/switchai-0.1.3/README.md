# SwitchAI  

SwitchAI is a lightweight and flexible library that provides a standardized interface for interacting with various AI APIs like OpenAI, Anthropic, Mistral, and more. With SwitchAI, you can easily switch between AI providers or use multiple APIs simultaneously, all with a simple and consistent interface.  

## Installation  

Install with pip:  
```bash  
pip install switchai  
```  

## Getting Started  

Here’s an example of how to use SwitchAI:  
```python  
from switchai import SwitchAI  

# Initialize the client with your chosen AI model or provider  
client = SwitchAI("gpt-4o")  

# Send a chat message to the AI  
response = client.chat(  
    messages=[  
        {"role": "user", "content": "Hello, how are you?"}  
    ]  
)
```  

## Documentation  

For full documentation, visit [SwitchAI Documentation](https://switchai.readthedocs.io/).  

## Contributing  

Contributions are always welcome! If you'd like to help enhance SwitchAI, feel free to make a contribution.
