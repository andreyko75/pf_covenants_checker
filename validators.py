"""
Pydantic модели для валидации результатов проверки ковенантов.
"""
from pydantic import BaseModel, Field
from typing import Dict, Literal


class CovenantResult(BaseModel):
    """Результат проверки ковенантов банка."""
    
    per_metric: Dict[str, Literal["OK", "FAIL"]] = Field(
        description="Статус по каждой метрике: ltv, llcr, dscr, balloon"
    )
    explanations: Dict[str, str] = Field(
        description="Краткие объяснения по каждой метрике"
    )
    verdict: Literal["APPROVE", "REJECT"] = Field(
        description="Общий вердикт по заявке"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "per_metric": {
                    "ltv": "OK",
                    "llcr": "OK", 
                    "dscr": "OK",
                    "balloon": "OK"
                },
                "explanations": {
                    "ltv": "LTV 0.65 < 0.7 - соответствует требованиям",
                    "llcr": "LLCR 1.1 >= 1.0 - соответствует требованиям",
                    "dscr": "DSCR 1.25 > 1.1 - соответствует требованиям", 
                    "balloon": "Balloon 40 <= 50 - соответствует требованиям"
                },
                "verdict": "APPROVE"
            }
        }


class CovenantInput(BaseModel):
    """Входные данные для проверки ковенантов."""
    
    ltv: float = Field(description="Loan-to-Value ratio", ge=0, le=1)
    llcr: float = Field(description="Loan Life Coverage Ratio", ge=0)
    dscr: float = Field(description="Debt Service Coverage Ratio", ge=0)
    balloon: float = Field(description="Balloon payment percentage", ge=0, le=100)
