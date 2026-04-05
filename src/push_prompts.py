import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, print_section_header

load_dotenv()


def get_missing_env_vars(required_vars: list[str]) -> list[str]:
    """Retorna a lista de variáveis de ambiente ausentes ou vazias."""
    missing = []
    for var in required_vars:
        value = os.getenv(var, "").strip()
        if not value:
            missing.append(var)
    return missing


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).
    """
    try:
        username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
        if not username:
            print("ERRO: USERNAME_LANGSMITH_HUB não preenchido no .env")
            return False

        full_prompt_name = f"{username}/{prompt_name}"

        system_prompt = prompt_data.get("system_prompt", "").strip()
        user_prompt = prompt_data.get("user_prompt", "").strip()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", user_prompt),
            ]
        )

        print(f"Fazendo push do prompt: {full_prompt_name}")
        hub.push(full_prompt_name, prompt, new_repo_is_public=True)
        print(f"Push concluído com sucesso: {full_prompt_name}")

        return True

    except Exception as e:
        print(f"Erro ao fazer push do prompt {prompt_name}: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.
    """
    errors = []

    required_fields = ["description", "system_prompt", "user_prompt", "version", "tags"]
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório ausente: {field}")

    if "system_prompt" in prompt_data and not str(prompt_data["system_prompt"]).strip():
        errors.append("system_prompt está vazio")

    if "user_prompt" in prompt_data and "{bug_report}" not in str(prompt_data["user_prompt"]):
        errors.append("user_prompt deveria conter a variável {bug_report}")

    techniques = prompt_data.get("techniques_used", [])
    if not isinstance(techniques, list) or len(techniques) < 2:
        errors.append("techniques_used deve conter pelo menos 2 técnicas")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS PARA O LANGSMITH")

    required_env_vars = [
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT",
        "USERNAME_LANGSMITH_HUB",
    ]

    missing = get_missing_env_vars(required_env_vars)
    if missing:
        print("Variáveis de ambiente ausentes:")
        for var in missing:
            print(f" - {var}")
        return 1

    prompt_file = os.path.join("prompts", "bug_to_user_story_v2.yml")
    if not os.path.exists(prompt_file):
        print(f"Arquivo não encontrado: {prompt_file}")
        return 1

    print(f"Lendo prompt otimizado de: {prompt_file}")
    data = load_yaml(prompt_file)

    if not data:
        print("Erro ao carregar YAML.")
        return 1

    total = 0
    success = 0

    for prompt_name, prompt_data in data.items():
        total += 1

        print_section_header(f"Validando prompt: {prompt_name}")

        is_valid, errors = validate_prompt(prompt_data)
        if not is_valid:
            print("Prompt inválido:")
            for err in errors:
                print(f" - {err}")
            continue

        print("Validação OK")

        if push_prompt_to_langsmith(prompt_name, prompt_data):
            success += 1

    print_section_header("RESUMO")
    print(f"Prompts processados: {total}")
    print(f"Push com sucesso: {success}")
    print(f"Falhas: {total - success}")

    return 0 if success == total and total > 0 else 1


if __name__ == "__main__":
    sys.exit(main())