# 🏦 Проверка ковенантов банка с LangChain

**Современная система автоматической проверки соответствия заявок минимальным ковенантам банка с использованием трех техник промптинга**

Минимальный каркас для автоматизации процесса проверки ковенантов в проектном финансировании.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-2C2C2C?logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-CLI-378BA3)
![python-dotenv](https://img.shields.io/badge/python--dotenv-3776AB?logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?logo=json&logoColor=white)

---

## 🚀 Возможности

* **Три техники промптинга** — Zero-Shot, Few-Shot, Chain-of-Verification
* **Автоматическая валидация** — через Pydantic модели
* **JSON-выход** — для интеграции с CRM и дашбордами
* **Объяснимость** — детальные объяснения по каждой метрике
* **Обработка ошибок** — с автоматическими повторными попытками
* **Масштабируемость** — обработка множества заявок 24/7

---

## 📁 Структура проекта

```
pf_covenants_checker/
├─ .env # Переменные окружения
├─ requirements.txt # Зависимости Python
├─ run.py # Простой скрипт для запуска
├─ main.py # CLI интерфейс
├─ prompts.py # Промпты для трех техник
├─ chain_factory.py # Фабрика LangChain цепочек
├─ validators.py # Pydantic модели
├─ examples/ # ok.json, fail.json
└─ README.md
```

---

## ⚙️ Установка

```bash
git clone https://github.com/andreyko75/pf_covenants_checker.git
cd pf_covenants_checker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создайте `.env`:

```env
OPENAI_API_KEY=sk-ваш-ключ-здесь
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.2
```

---

## 🎯 Использование

```bash
# Zero-Shot
python run.py zero --input examples/ok.json

# Few-Shot
python run.py few --input examples/fail.json

# Chain-of-Verification
python run.py cov --input examples/ok.json

# С объяснениями
python run.py zero --input examples/ok.json --explain
```

---

## 📊 Правила проверки ковенантов

- **LTV (Loan-to-Value)**: < 0.7
- **LLCR (Loan Life Coverage Ratio)**: ≥ 1.0
- **DSCR (Debt Service Coverage Ratio)**: > 1.1
- **Balloon (Balloon payment %)**: ≤ 50

---

## 🛠 Технологии

* Python 3.11+, LangChain, OpenAI API, Pydantic, Typer, python-dotenv

---

**Репозиторий:** [https://github.com/andreyko75/pf_covenants_checker](https://github.com/andreyko75/pf_covenants_checker)

_Создано с ❤️ для изучения техник промптинга в LangChain_
