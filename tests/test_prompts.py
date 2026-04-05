import os
import yaml
import pytest


class TestPromptValidation:
    @classmethod
    def setup_class(cls):
        prompt_file = os.path.join("prompts", "bug_to_user_story_v2.yml")

        with open(prompt_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        cls.prompt_data = data["bug_to_user_story_v2"]
        cls.system_prompt = cls.prompt_data.get("system_prompt", "")
        cls.user_prompt = cls.prompt_data.get("user_prompt", "")
        cls.full_text = f"{cls.system_prompt}\n{cls.user_prompt}"

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo existe e não está vazio."""
        assert "system_prompt" in self.prompt_data
        assert isinstance(self.system_prompt, str)
        assert self.system_prompt.strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona."""
        role_keywords = [
            "product manager",
            "gerente de produto",
            "especializado",
            "especialista",
            "você é um",
        ]
        lower_text = self.system_prompt.lower()
        assert any(keyword in lower_text for keyword in role_keywords), (
            "O system_prompt não parece definir claramente uma persona/role."
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato de User Story e critérios de aceitação."""
        lower_text = self.full_text.lower()

        expected_indicators = [
            "como um [tipo de usuário], eu quero [ação/resultado esperado], para que eu possa [benefício]",
            "critérios de aceitação:",
            "- dado que",
            "- quando",
            "- então",
        ]

        missing = [item for item in expected_indicators if item not in lower_text]
        assert not missing, f"Indicadores de formato ausentes: {missing}"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos few-shot suficientes."""
        lower_text = self.system_prompt.lower()

        few_shot_indicators = [
            "exemplo 1",
            "exemplo 2",
            "exemplo 3",
            "bug report:",
            "resposta:",
        ]

        matches = sum(1 for item in few_shot_indicators if item in lower_text)
        assert matches >= 4, "O prompt não parece conter exemplos few-shot suficientes."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum TODO no texto."""
        assert "[todo]" not in self.full_text.lower()
        assert "todo:" not in self.full_text.lower()

    def test_minimum_techniques(self):
        """Verifica se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt_data.get("techniques_used", [])
        assert isinstance(techniques, list), "techniques_used deve ser uma lista."
        assert len(techniques) >= 2, "É necessário listar pelo menos 2 técnicas no YAML."


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])