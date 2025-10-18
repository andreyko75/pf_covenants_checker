"""
Промпты для трех техник проверки ковенантов банка.
"""
from langchain.prompts import PromptTemplate


# Zero-Shot промпт
ZERO_SHOT_PROMPT = PromptTemplate(
    input_variables=["ltv", "llcr", "dscr", "balloon"],
    template="""Вы - эксперт по банковским ковенантам. Проверьте заявку на соответствие минимальным требованиям банка.

Входные данные:
- LTV (Loan-to-Value): {ltv}
- LLCR (Loan Life Coverage Ratio): {llcr}  
- DSCR (Debt Service Coverage Ratio): {dscr}
- Balloon (Balloon payment %): {balloon}

Правила проверки:
- LTV < 0.7 → OK, иначе FAIL
- LLCR >= 1 → OK, иначе FAIL
- DSCR > 1.1 → OK, иначе FAIL  
- Balloon ≤ 50 → OK, иначе FAIL

Вердикт: APPROVE если все метрики OK, иначе REJECT.

Верните результат строго в JSON формате:
{{
  "per_metric": {{
    "ltv": "OK/FAIL",
    "llcr": "OK/FAIL", 
    "dscr": "OK/FAIL",
    "balloon": "OK/FAIL"
  }},
  "explanations": {{
    "ltv": "краткое объяснение",
    "llcr": "краткое объяснение",
    "dscr": "краткое объяснение", 
    "balloon": "краткое объяснение"
  }},
  "verdict": "APPROVE/REJECT"
}}"""
)


# Few-Shot промпт с примерами
FEW_SHOT_PROMPT = PromptTemplate(
    input_variables=["ltv", "llcr", "dscr", "balloon"],
    template="""Вы - эксперт по банковским ковенантам. Проверьте заявку на соответствие минимальным требованиям банка.

Правила проверки:
- LTV < 0.7 → OK, иначе FAIL
- LLCR >= 1 → OK, иначе FAIL
- DSCR > 1.1 → OK, иначе FAIL  
- Balloon ≤ 50 → OK, иначе FAIL

Примеры:

Пример 1:
Вход: LTV=0.65, LLCR=1.1, DSCR=1.25, Balloon=40
Результат:
{{
  "per_metric": {{"ltv": "OK", "llcr": "OK", "dscr": "OK", "balloon": "OK"}},
  "explanations": {{
    "ltv": "LTV 0.65 < 0.7 - соответствует требованиям",
    "llcr": "LLCR 1.1 >= 1.0 - соответствует требованиям", 
    "dscr": "DSCR 1.25 > 1.1 - соответствует требованиям",
    "balloon": "Balloon 40 <= 50 - соответствует требованиям"
  }},
  "verdict": "APPROVE"
}}

Пример 2:
Вход: LTV=0.8, LLCR=0.9, DSCR=1.0, Balloon=60
Результат:
{{
  "per_metric": {{"ltv": "FAIL", "llcr": "FAIL", "dscr": "FAIL", "balloon": "FAIL"}},
  "explanations": {{
    "ltv": "LTV 0.8 >= 0.7 - не соответствует требованиям",
    "llcr": "LLCR 0.9 < 1.0 - не соответствует требованиям",
    "dscr": "DSCR 1.0 <= 1.1 - не соответствует требованиям", 
    "balloon": "Balloon 60 > 50 - не соответствует требованиям"
  }},
  "verdict": "REJECT"
}}

Пример 3 (граничный случай):
Вход: LTV=0.7, LLCR=1.0, DSCR=1.1, Balloon=50
Результат:
{{
  "per_metric": {{"ltv": "FAIL", "llcr": "OK", "dscr": "OK", "balloon": "OK"}},
  "explanations": {{
    "ltv": "LTV 0.7 >= 0.7 - не соответствует требованиям",
    "llcr": "LLCR 1.0 >= 1.0 - соответствует требованиям",
    "dscr": "DSCR 1.1 > 1.1 - не соответствует требованиям",
    "balloon": "Balloon 50 <= 50 - соответствует требованиям"
  }},
  "verdict": "REJECT"
}}

Теперь проверьте заявку:
Вход: LTV={ltv}, LLCR={llcr}, DSCR={dscr}, Balloon={balloon}

Верните результат строго в JSON формате:"""
)


# Chain-of-Verification промпт
CHAIN_OF_VERIFICATION_PROMPT = PromptTemplate(
    input_variables=["ltv", "llcr", "dscr", "balloon"],
    template="""Вы - эксперт по банковским ковенантам. Проверьте заявку на соответствие минимальным требованиям банка.

Входные данные:
- LTV (Loan-to-Value): {ltv}
- LLCR (Loan Life Coverage Ratio): {llcr}  
- DSCR (Debt Service Coverage Ratio): {dscr}
- Balloon (Balloon payment %): {balloon}

Правила проверки:
- LTV < 0.7 → OK, иначе FAIL
- LLCR >= 1 → OK, иначе FAIL
- DSCR > 1.1 → OK, иначе FAIL  
- Balloon ≤ 50 → OK, иначе FAIL

Сначала выполните самопроверку:

1. Проверьте LTV: {ltv} < 0.7? Результат: [OK/FAIL]
2. Проверьте LLCR: {llcr} >= 1? Результат: [OK/FAIL]  
3. Проверьте DSCR: {dscr} > 1.1? Результат: [OK/FAIL]
4. Проверьте Balloon: {balloon} ≤ 50? Результат: [OK/FAIL]

Чек-лист самопроверки:
- Все поля присутствуют в результате?
- Сравнения применены к правильным входным числам?
- Граничные условия трактованы корректно?
- JSON будет валидным?

После самопроверки верните только финальный JSON результат:
{{
  "per_metric": {{
    "ltv": "OK/FAIL",
    "llcr": "OK/FAIL", 
    "dscr": "OK/FAIL",
    "balloon": "OK/FAIL"
  }},
  "explanations": {{
    "ltv": "краткое объяснение",
    "llcr": "краткое объяснение",
    "dscr": "краткое объяснение", 
    "balloon": "краткое объяснение"
  }},
  "verdict": "APPROVE/REJECT"
}}"""
)
