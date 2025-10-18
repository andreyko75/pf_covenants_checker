#!/usr/bin/env python3
"""
Простой скрипт для проверки ковенантов банка.
"""
import json
import sys
import os
from pathlib import Path

from chain_factory import CovenantChainFactory
from validators import CovenantInput, CovenantResult


def load_input_from_file(file_path: str) -> dict:
    """Загружает входные данные из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Валидируем входные данные
        validated_data = CovenantInput(**data)
        return validated_data.model_dump()
        
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        sys.exit(1)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Ошибка в файле {file_path}: {e}")
        sys.exit(1)


def get_interactive_input() -> dict:
    """Получает входные данные интерактивно."""
    try:
        ltv = float(input("Введите LTV (0-1): "))
        llcr = float(input("Введите LLCR: "))
        dscr = float(input("Введите DSCR: "))
        balloon = float(input("Введите Balloon (%): "))
        
        # Валидируем данные
        validated_data = CovenantInput(ltv=ltv, llcr=llcr, dscr=dscr, balloon=balloon)
        return validated_data.model_dump()
        
    except (ValueError, Exception) as e:
        print(f"Ошибка ввода: {e}")
        sys.exit(1)


def print_result(result: CovenantResult, explain: bool = False):
    """Выводит результат проверки."""
    if explain:
        print("\n=== РЕЗУЛЬТАТ ПРОВЕРКИ КОВЕНАНТОВ ===")
        print(f"LTV: {result.per_metric['ltv']} - {result.explanations['ltv']}")
        print(f"LLCR: {result.per_metric['llcr']} - {result.explanations['llcr']}")
        print(f"DSCR: {result.per_metric['dscr']} - {result.explanations['dscr']}")
        print(f"Balloon: {result.per_metric['balloon']} - {result.explanations['balloon']}")
        print(f"\nВердикт: {result.verdict}")
        print("=" * 40)
    else:
        # Выводим только JSON
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("Использование: python run.py <technique> [options]")
        print("Техники: zero, few, cov")
        print("Опции: --input <file> --explain --temperature <value>")
        sys.exit(1)
    
    technique = sys.argv[1]
    
    # Парсим аргументы
    input_file = None
    explain = False
    temperature = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--input" and i + 1 < len(sys.argv):
            input_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--explain":
            explain = True
            i += 1
        elif sys.argv[i] == "--temperature" and i + 1 < len(sys.argv):
            temperature = float(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    try:
        # Получаем входные данные
        if input_file:
            input_data = load_input_from_file(input_file)
        else:
            input_data = get_interactive_input()
        
        # Создаем цепочку
        factory = CovenantChainFactory(temperature=temperature)
        
        if technique == "zero":
            chain = factory.create_zero_shot_chain()
        elif technique == "few":
            chain = factory.create_few_shot_chain()
        elif technique == "cov":
            chain = factory.create_chain_of_verification_chain()
        else:
            print(f"Неизвестная техника: {technique}")
            sys.exit(1)
        
        # Запускаем проверку
        result = factory.run_chain(chain, input_data)
        print_result(result, explain)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
