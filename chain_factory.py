"""
Фабрика LangChain цепочек для проверки ковенантов.
"""
import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import ValidationError

from prompts import ZERO_SHOT_PROMPT, FEW_SHOT_PROMPT, CHAIN_OF_VERIFICATION_PROMPT
from validators import CovenantResult


# Загружаем переменные окружения
load_dotenv()


class CovenantChainFactory:
    """Фабрика для создания цепочек проверки ковенантов."""
    
    def __init__(self, temperature: Optional[float] = None):
        """Инициализация фабрики с настройками модели."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "sk-your-api-key-here":
            raise ValueError("OPENAI_API_KEY не установлен в .env файле")
        
        self.base_url = os.getenv("OPENAI_BASE_URL") or None
        self.model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.temperature = temperature or float(os.getenv("TEMPERATURE", "0.2"))
        
        # Создаем LLM
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url
        )
    
    def create_zero_shot_chain(self) -> LLMChain:
        """Создает Zero-Shot цепочку."""
        return LLMChain(
            llm=self.llm,
            prompt=ZERO_SHOT_PROMPT,
            output_key="result"
        )
    
    def create_few_shot_chain(self) -> LLMChain:
        """Создает Few-Shot цепочку."""
        return LLMChain(
            llm=self.llm,
            prompt=FEW_SHOT_PROMPT,
            output_key="result"
        )
    
    def create_chain_of_verification_chain(self) -> LLMChain:
        """Создает Chain-of-Verification цепочку."""
        return LLMChain(
            llm=self.llm,
            prompt=CHAIN_OF_VERIFICATION_PROMPT,
            output_key="result"
        )
    
    def run_chain(self, chain: LLMChain, input_data: Dict[str, Any]) -> CovenantResult:
        """Запускает цепочку и возвращает валидированный результат."""
        try:
            # Запускаем цепочку
            result = chain.run(**input_data)
            
            # Пытаемся извлечь JSON из ответа
            json_str = self._extract_json_from_response(result)
            
            # Парсим JSON
            json_data = json.loads(json_str)
            
            # Валидируем через Pydantic
            return CovenantResult(**json_data)
            
        except (json.JSONDecodeError, ValidationError) as e:
            # При ошибке валидации пытаемся еще раз с подсказкой
            try:
                retry_prompt = f"""Предыдущий ответ был невалидным: {str(e)}
                
Верните валидный JSON по схеме:
{{
  "per_metric": {{"ltv": "OK/FAIL", "llcr": "OK/FAIL", "dscr": "OK/FAIL", "balloon": "OK/FAIL"}},
  "explanations": {{"ltv": "объяснение", "llcr": "объяснение", "dscr": "объяснение", "balloon": "объяснение"}},
  "verdict": "APPROVE/REJECT"
}}"""
                
                retry_result = self.llm.invoke(retry_prompt)
                json_str = self._extract_json_from_response(retry_result.content)
                json_data = json.loads(json_str)
                return CovenantResult(**json_data)
                
            except Exception as retry_error:
                raise ValueError(f"Не удалось получить валидный результат после повторной попытки: {retry_error}")
    
    def _extract_json_from_response(self, response: str) -> str:
        """Извлекает JSON из ответа модели."""
        # Ищем JSON в ответе
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("JSON не найден в ответе")
        
        return response[start_idx:end_idx]
