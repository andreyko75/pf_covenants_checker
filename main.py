"""
CLI для проверки ковенантов банка с тремя техниками промптинга.
"""
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import typer
from pydantic import ValidationError

from chain_factory import CovenantChainFactory
from validators import CovenantInput, CovenantResult


app = typer.Typer(help="Проверка ковенантов банка с использованием LangChain")


def load_input_from_file(file_path: str) -> Dict[str, float]:
    """Загружает входные данные из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Валидируем входные данные
        validated_data = CovenantInput(**data)
        return validated_data.model_dump()
        
    except FileNotFoundError:
        typer.echo(f"Файл {file_path} не найден", err=True)
        raise typer.Exit(1)
    except (json.JSONDecodeError, ValidationError) as e:
        typer.echo(f"Ошибка в файле {file_path}: {e}", err=True)
        raise typer.Exit(1)


def get_interactive_input() -> Dict[str, float]:
    """Получает входные данные интерактивно."""
    try:
        ltv = float(typer.prompt("Введите LTV (0-1)"))
        llcr = float(typer.prompt("Введите LLCR"))
        dscr = float(typer.prompt("Введите DSCR"))
        balloon = float(typer.prompt("Введите Balloon (%)"))
        
        # Валидируем данные
        validated_data = CovenantInput(ltv=ltv, llcr=llcr, dscr=dscr, balloon=balloon)
        return validated_data.model_dump()
        
    except (ValueError, ValidationError) as e:
        typer.echo(f"Ошибка ввода: {e}", err=True)
        raise typer.Exit(1)


def print_result(result: CovenantResult, explain: bool = False):
    """Выводит результат проверки."""
    if explain:
        typer.echo("\n=== РЕЗУЛЬТАТ ПРОВЕРКИ КОВЕНАНТОВ ===")
        typer.echo(f"LTV: {result.per_metric['ltv']} - {result.explanations['ltv']}")
        typer.echo(f"LLCR: {result.per_metric['llcr']} - {result.explanations['llcr']}")
        typer.echo(f"DSCR: {result.per_metric['dscr']} - {result.explanations['dscr']}")
        typer.echo(f"Balloon: {result.per_metric['balloon']} - {result.explanations['balloon']}")
        typer.echo(f"\nВердикт: {result.verdict}")
        typer.echo("=" * 40)
    else:
        # Выводим только JSON
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


@app.command("zero")
def zero_shot(
    input_file: Optional[str] = typer.Option(None, "--input", help="JSON файл с данными"),
    explain: bool = typer.Option(False, "--explain", help="Показать объяснения"),
    temperature: Optional[float] = typer.Option(None, "--temperature", help="Температура модели")
):
    """Zero-Shot проверка ковенантов."""
    try:
        # Получаем входные данные
        if input_file:
            input_data = load_input_from_file(input_file)
        else:
            input_data = get_interactive_input()
        
        # Создаем цепочку
        factory = CovenantChainFactory(temperature=temperature)
        chain = factory.create_zero_shot_chain()
        
        # Запускаем проверку
        result = factory.run_chain(chain, input_data)
        print_result(result, explain)
        
    except Exception as e:
        typer.echo(f"Ошибка: {e}", err=True)
        raise typer.Exit(1)


@app.command("few")
def few_shot(
    input_file: Optional[str] = typer.Option(None, "--input", help="JSON файл с данными"),
    explain: bool = typer.Option(False, "--explain", help="Показать объяснения"),
    temperature: Optional[float] = typer.Option(None, "--temperature", help="Температура модели")
):
    """Few-Shot проверка ковенантов."""
    try:
        # Получаем входные данные
        if input_file:
            input_data = load_input_from_file(input_file)
        else:
            input_data = get_interactive_input()
        
        # Создаем цепочку
        factory = CovenantChainFactory(temperature=temperature)
        chain = factory.create_few_shot_chain()
        
        # Запускаем проверку
        result = factory.run_chain(chain, input_data)
        print_result(result, explain)
        
    except Exception as e:
        typer.echo(f"Ошибка: {e}", err=True)
        raise typer.Exit(1)


@app.command("cov")
def chain_of_verification(
    input_file: Optional[str] = typer.Option(None, "--input", help="JSON файл с данными"),
    explain: bool = typer.Option(False, "--explain", help="Показать объяснения"),
    temperature: Optional[float] = typer.Option(None, "--temperature", help="Температура модели")
):
    """Chain-of-Verification проверка ковенантов."""
    try:
        # Получаем входные данные
        if input_file:
            input_data = load_input_from_file(input_file)
        else:
            input_data = get_interactive_input()
        
        # Создаем цепочку
        factory = CovenantChainFactory(temperature=temperature)
        chain = factory.create_chain_of_verification_chain()
        
        # Запускаем проверку
        result = factory.run_chain(chain, input_data)
        print_result(result, explain)
        
    except Exception as e:
        typer.echo(f"Ошибка: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()