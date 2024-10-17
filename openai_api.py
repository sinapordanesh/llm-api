"""
Install the OpenAI Python SDK

$ pip install openai
"""

import os
from openai import OpenAI
import json
import time
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


# Access the API key from the environment variable



class OPENAI_API:
    def __init__(self, model="gpt-4o", temperature=0.6, max_tokens=512, system_prompt=None):
        self.client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY'], 
        )
        # Configuration for model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
        self.system_prompt = system_prompt or "You are a highly capable assistant. Provide clear, accurate, and concise responses to any task or question."
        
    def codeSnippetCleanup(self, input):
        # Remove any occurrences of backticks and "python" keyword
        language_delimiters = { "python": "```python", "javascript": "```javascript","html": "```html", "java": "```java", "bash": "```bash", "json": "```json", "css": "```css", "cpp": "```cpp", "c": "```c", "ruby": "```ruby", "go": "```go", "php": "```php", "sql": "```sql", "shell": "```shell", "xml": "```xml",
            }
        for language, delimiter in language_delimiters.items():
                if delimiter in input:
                    # Remove the language-specific code block delimiter
                    input = input.replace(delimiter, "")
            
        # Remove the common ending code block delimiter
        input = input.replace("```", "")
        return input.strip()
    
    def communication(self, prompt, timeout=360):
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ], 
                timeout=timeout, 
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Timeout or error occurred."