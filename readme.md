### README

# Segunda Via Cemig

## Requisitos

- Python

## Instalação

1. Clone este repositório para o seu ambiente local:
    ```bash
    git clone https://github.com/agoristony/cemig-segunda-via.git
    cd cemig-segunda-via
    ```

2. Instale as dependências do projeto:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

3. Faça uma cópia do arquivo `.env.example` e renomeie para `.env`:
    ```bash
    cp .env.example .env
    ```
    - Altere as variáveis de ambiente conforme necessário.


## Execução

### Linha de Comando

Para listar as instalações ativas do usuário, execute o seguinte comando:
```bash
python3 cemig2pdf.py
```

Para listar as faturas de uma instalação específica, utilize a opção `--site` ou `-s`, a opção `--all` ou `-a` para listar todas as faturas:
```bash
python3 cemig2pdf.py --site <instalacao>
```

Para ver os detalhes de uma fatura específica, utilize a opção `--identifier` ou `-i`:
```bash
python3 cemig2pdf.py --site <instalacao> --identifier <fatura>
```

Para exportar uma fatura específica para PDF, utilize a opção `--pdf` ou `-p`:
```bash
python3 cemig2pdf.py --site <instalacao> --identifier <fatura> --pdf
```

## Estrutura do Projeto

### Arquivos

- **captcha.py**: Módulo para resolver o captcha da página de login.
- **cemigweb.py**: Módulo para interagir com o site da Cemig.
- **cemig2pdf.py**: Script principal.
- **graphql.py**: Módulo para guardar as consultas e interagir com a API GraphQL da Cemig.
- **settings.py**: Módulo para guardar as configurações do projeto.


## Funcionalidades

- **Interface Web**:
  - Exibição das instalações ativas do usuário.
  - Exibição das faturas de uma instalação específica.
  - Exibição dos detalhes de uma fatura específica.
  - Exportação de uma fatura específica para PDF.
