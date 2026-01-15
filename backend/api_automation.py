# API Automation - Generate Retrofit interfaces from OpenAPI/Swagger

import json
import re
from typing import Dict, List

class APIAutomation:
    """Automatically generate Retrofit interfaces from API documentation"""
    
    def __init__(self):
        self.type_mapping = {
            'string': 'String',
            'integer': 'Int',
            'number': 'Double',
            'boolean': 'Boolean',
            'array': 'List',
            'object': 'Any'
        }
    
    def parse_openapi(self, openapi_json: Dict) -> Dict:
        """Parse OpenAPI/Swagger JSON"""
        endpoints = []
        models = []
        
        # Parse paths (endpoints)
        for path, methods in openapi_json.get('paths', {}).items():
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    endpoint = {
                        'path': path,
                        'method': method.upper(),
                        'operation_id': details.get('operationId', ''),
                        'summary': details.get('summary', ''),
                        'parameters': self._parse_parameters(details.get('parameters', [])),
                        'request_body': self._parse_request_body(details.get('requestBody', {})),
                        'responses': self._parse_responses(details.get('responses', {}))
                    }
                    endpoints.append(endpoint)
        
        # Parse schemas (models)
        schemas = openapi_json.get('components', {}).get('schemas', {})
        for name, schema in schemas.items():
            model = self._parse_schema(name, schema)
            models.append(model)
        
        return {
            'endpoints': endpoints,
            'models': models,
            'base_url': self._extract_base_url(openapi_json)
        }
    
    def generate_retrofit_interface(self, api_data: Dict, package_name: str) -> str:
        """Generate Kotlin Retrofit interface"""
        
        interface_name = "ApiService"
        endpoints = api_data['endpoints']
        
        code = f'''package {package_name}.data.api

import retrofit2.Response
import retrofit2.http.*

interface {interface_name} {{
'''
        
        for endpoint in endpoints:
            # Generate method
            method_name = endpoint['operation_id'] or self._generate_method_name(endpoint)
            http_method = endpoint['method']
            path = endpoint['path']
            
            # Parameters
            params = []
            for param in endpoint.get('parameters', []):
                param_type = self.type_mapping.get(param['type'], 'String')
                params.append(f"@{param['in'].capitalize()}(\"{param['name']}\") {param['name']}: {param_type}")
            
            # Request body
            if endpoint.get('request_body'):
                body_type = endpoint['request_body'].get('type', 'Any')
                params.append(f"@Body body: {body_type}")
            
            # Response type
            response_type = endpoint.get('responses', {}).get('200', {}).get('type', 'Any')
            
            # Generate method signature
            params_str = ",\\n        ".join(params) if params else ""
            
            code += f'''
    /**
     * {endpoint.get('summary', '')}
     */
    @{http_method}("{path}")
    suspend fun {method_name}(
        {params_str}
    ): Response<{response_type}>
    
'''
        
        code += "}\n"
        
        return code
    
    def generate_data_classes(self, models: List[Dict], package_name: str) -> Dict[str, str]:
        """Generate Kotlin data classes from models"""
        
        data_classes = {}
        
        for model in models:
            class_name = model['name']
            properties = model['properties']
            
            code = f'''package {package_name}.data.model

import com.google.gson.annotations.SerializedName

/**
 * {model.get('description', '')}
 */
data class {class_name}(
'''
            
            # Generate properties
            props = []
            for prop in properties:
                prop_name = prop['name']
                prop_type = self.type_mapping.get(prop['type'], 'String')
                
                # Handle nullable
                if not prop.get('required', False):
                    prop_type += "?"
                
                # Handle arrays
                if prop['type'] == 'array':
                    item_type = self.type_mapping.get(prop.get('items', {}).get('type', 'Any'), 'Any')
                    prop_type = f"List<{item_type}>"
                
                # Add SerializedName annotation
                props.append(f'    @SerializedName("{prop_name}")\\n    val {self._to_camel_case(prop_name)}: {prop_type}')
            
            code += ",\\n".join(props)
            code += "\\n)\\n"
            
            data_classes[class_name] = code
        
        return data_classes
    
    def generate_repository(self, api_data: Dict, package_name: str) -> str:
        """Generate Repository pattern implementation"""
        
        return f'''package {package_name}.data.repository

import {package_name}.data.api.ApiService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ApiRepository @Inject constructor(
    private val apiService: ApiService
) {{
    
    suspend fun <T> safeApiCall(
        apiCall: suspend () -> retrofit2.Response<T>
    ): Result<T> = withContext(Dispatchers.IO) {{
        try {{
            val response = apiCall()
            if (response.isSuccessful) {{
                response.body()?.let {{
                    Result.success(it)
                }} ?: Result.failure(Exception("Empty response body"))
            }} else {{
                Result.failure(Exception("API Error: ${{response.code()}}"))
            }}
        }} catch (e: Exception) {{
            Result.failure(e)
        }}
    }}
    
    // Example method
    suspend fun fetchData() = safeApiCall {{
        apiService.getData()
    }}
}}
'''
    
    def generate_retrofit_builder(self, base_url: str, package_name: str) -> str:
        """Generate Retrofit builder with interceptors"""
        
        return f'''package {package_name}.data.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitBuilder {{
    
    private const val BASE_URL = "{base_url}"
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {{
        level = HttpLoggingInterceptor.Level.BODY
    }}
    
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .addInterceptor {{ chain ->
            val request = chain.request().newBuilder()
                .addHeader("Content-Type", "application/json")
                .addHeader("Accept", "application/json")
                .build()
            chain.proceed(request)
        }}
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val apiService: ApiService = retrofit.create(ApiService::class.java)
}}
'''
    
    def _parse_parameters(self, parameters: List) -> List[Dict]:
        """Parse endpoint parameters"""
        parsed = []
        for param in parameters:
            parsed.append({
                'name': param.get('name', ''),
                'in': param.get('in', 'query'),
                'type': param.get('schema', {}).get('type', 'string'),
                'required': param.get('required', False),
                'description': param.get('description', '')
            })
        return parsed
    
    def _parse_request_body(self, request_body: Dict) -> Dict:
        """Parse request body"""
        if not request_body:
            return {}
        
        content = request_body.get('content', {})
        json_content = content.get('application/json', {})
        schema = json_content.get('schema', {})
        
        return {
            'type': schema.get('$ref', '').split('/')[-1] or 'Any',
            'required': request_body.get('required', False)
        }
    
    def _parse_responses(self, responses: Dict) -> Dict:
        """Parse responses"""
        parsed = {}
        for status_code, response in responses.items():
            content = response.get('content', {})
            json_content = content.get('application/json', {})
            schema = json_content.get('schema', {})
            
            parsed[status_code] = {
                'type': schema.get('$ref', '').split('/')[-1] or 'Any',
                'description': response.get('description', '')
            }
        return parsed
    
    def _parse_schema(self, name: str, schema: Dict) -> Dict:
        """Parse schema to model"""
        properties = []
        required_fields = schema.get('required', [])
        
        for prop_name, prop_schema in schema.get('properties', {}).items():
            properties.append({
                'name': prop_name,
                'type': prop_schema.get('type', 'string'),
                'items': prop_schema.get('items', {}),
                'required': prop_name in required_fields,
                'description': prop_schema.get('description', '')
            })
        
        return {
            'name': name,
            'description': schema.get('description', ''),
            'properties': properties
        }
    
    def _extract_base_url(self, openapi_json: Dict) -> str:
        """Extract base URL from OpenAPI spec"""
        servers = openapi_json.get('servers', [])
        if servers:
            return servers[0].get('url', 'https://api.example.com')
        return 'https://api.example.com'
    
    def _generate_method_name(self, endpoint: Dict) -> str:
        """Generate method name from endpoint"""
        method = endpoint['method'].lower()
        path = endpoint['path'].replace('/', '_').replace('{', '').replace('}', '')
        return f"{method}{self._to_camel_case(path)}"
    
    def _to_camel_case(self, snake_str: str) -> str:
        """Convert snake_case to camelCase"""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])


# Example usage
def generate_api_from_swagger(swagger_url: str, package_name: str, output_dir: str):
    """Complete API generation from Swagger URL"""
    import requests
    import os
    
    # Fetch Swagger JSON
    response = requests.get(swagger_url)
    openapi_json = response.json()
    
    # Initialize automation
    automation = APIAutomation()
    
    # Parse API
    api_data = automation.parse_openapi(openapi_json)
    
    # Generate files
    api_dir = os.path.join(output_dir, 'data', 'api')
    model_dir = os.path.join(output_dir, 'data', 'model')
    repo_dir = os.path.join(output_dir, 'data', 'repository')
    
    os.makedirs(api_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(repo_dir, exist_ok=True)
    
    # 1. Retrofit Interface
    interface_code = automation.generate_retrofit_interface(api_data, package_name)
    with open(os.path.join(api_dir, 'ApiService.kt'), 'w') as f:
        f.write(interface_code)
    
    # 2. Data Classes
    data_classes = automation.generate_data_classes(api_data['models'], package_name)
    for class_name, code in data_classes.items():
        with open(os.path.join(model_dir, f'{class_name}.kt'), 'w') as f:
            f.write(code)
    
    # 3. Repository
    repo_code = automation.generate_repository(api_data, package_name)
    with open(os.path.join(repo_dir, 'ApiRepository.kt'), 'w') as f:
        f.write(repo_code)
    
    # 4. Retrofit Builder
    builder_code = automation.generate_retrofit_builder(api_data['base_url'], package_name)
    with open(os.path.join(api_dir, 'RetrofitBuilder.kt'), 'w') as f:
        f.write(builder_code)
    
    return {
        'success': True,
        'files_generated': len(data_classes) + 3,
        'endpoints': len(api_data['endpoints']),
        'models': len(api_data['models'])
    }
