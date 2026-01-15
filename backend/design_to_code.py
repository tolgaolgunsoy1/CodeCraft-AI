import base64
import os
from PIL import Image
import io
import requests
import json

class DesignToCode:
    """Convert UI designs/screenshots to Compose code"""
    
    def __init__(self, gemini_api_key):
        self.api_key = gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def analyze_design(self, image_path):
        """Analyze UI design and extract components"""
        image_base64 = self._encode_image(image_path)
        
        prompt = """Analyze this UI design and identify:
1. Layout structure (Column, Row, Box)
2. UI components (Button, TextField, Card, Image, Text)
3. Colors and styling
4. Spacing and padding

Return as JSON:
{
  "layout": "Column",
  "components": [
    {"type": "Text", "text": "Title", "style": "headline"},
    {"type": "Button", "text": "Click", "color": "#6200EE"}
  ]
}"""
        
        result = self._call_gemini_vision(image_base64, prompt)
        return self._parse_components(result)
    
    def generate_compose_code(self, components, package_name):
        """Generate Jetpack Compose code from components"""
        code = f"""package {package_name}.ui.generated

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun GeneratedScreen() {{
    {self._generate_layout(components)}
}}
"""
        return code
    
    def _generate_layout(self, components):
        layout = components.get('layout', 'Column')
        items = components.get('components', [])
        
        code = f"{layout}(\n        modifier = Modifier\n            .fillMaxSize()\n            .padding(16.dp)\n    ) {{\n"
        
        for item in items:
            comp_type = item.get('type')
            if comp_type == 'Text':
                code += f"        Text(\n            text = \"{item.get('text', '')}\",\n"
                code += f"            style = MaterialTheme.typography.{item.get('style', 'bodyLarge')}\n        )\n"
            elif comp_type == 'Button':
                code += f"        Button(onClick = {{ /* TODO */ }}) {{\n"
                code += f"            Text(\"{item.get('text', 'Button')}\")\n        }}\n"
            elif comp_type == 'TextField':
                code += f"        OutlinedTextField(\n            value = \"\",\n"
                code += f"            onValueChange = {{}},\n            label = {{ Text(\"{item.get('label', '')}\") }}\n        )\n"
            elif comp_type == 'Card':
                code += f"        Card(\n            modifier = Modifier.fillMaxWidth()\n        ) {{\n"
                code += f"            Text(\"{item.get('text', '')}\")\n        }}\n"
            
            code += "        Spacer(modifier = Modifier.height(8.dp))\n"
        
        code += "    }"
        return code
    
    def _encode_image(self, image_path):
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def _call_gemini_vision(self, image_base64, prompt):
        url = f"{self.base_url}/gemini-pro-vision:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        return "{}"
    
    def _parse_components(self, result):
        try:
            # Extract JSON from markdown code blocks if present
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                result = result.split("```")[1].split("```")[0]
            
            return json.loads(result.strip())
        except:
            return {"layout": "Column", "components": []}
