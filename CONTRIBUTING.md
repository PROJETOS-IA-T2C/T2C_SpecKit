# Guia de Contribuição

Obrigado por considerar contribuir com o RPA Spec-Kit!

## Como Contribuir

### Reportar Bugs

Se você encontrou um bug, por favor abra uma issue descrevendo:
- O que aconteceu
- O que você esperava que acontecesse
- Passos para reproduzir
- Ambiente (OS, Python version, etc.)

### Sugerir Melhorias

Sugestões são bem-vindas! Abra uma issue com:
- Descrição clara da melhoria
- Casos de uso
- Exemplos se aplicável

### Pull Requests

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

### Padrões de Código

- Siga PEP 8 para Python
- Use type hints quando possível
- Adicione docstrings para funções e classes
- Mantenha testes atualizados

## Desenvolvimento

### Setup

```bash
git clone https://github.com/org/rpa-spec-kit.git
cd rpa-spec-kit
pip install -e ".[dev]"
```

### Testes

```bash
pytest
```

### Linting

```bash
black .
flake8 .
```

## Perguntas?

Sinta-se à vontade para abrir uma issue para qualquer dúvida!

