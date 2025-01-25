# Route API Project

Este projeto consiste em uma API que calcula a menor rota entre vários lugares usando o OpenStreetMap e FastAPI.

## **Tutorial: Como Rodar o Projeto da API de Menor Rota**

Este tutorial descreve como configurar e rodar o projeto da API de menor rota entre locais usando FastAPI e outras bibliotecas em Python.

### **1. Clonar o Repositório**

Primeiro, clone o repositório do projeto (caso ainda não tenha feito isso):

```bash
git clone https://github.com/usuario/route-api.git
cd route-api
```

Substitua `usuario` pelo nome de usuário correto no GitHub, caso seja necessário.

### **2. Configurar o Ambiente Virtual**

Recomendamos criar um ambiente virtual para instalar as dependências do projeto e garantir que elas não interfiram em outros projetos:

```bash
# Criar um ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows
venv\Scripts\activate
# No Linux/macOS
source venv/bin/activate
```

### **3. Instalar as Dependências**

Com o ambiente virtual ativado, instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Esse comando irá instalar as bibliotecas necessárias, como `fastapi`, `uvicorn`, `osmnx`, `networkx`, e `geopy`.

### **4. Rodar o Servidor**

Para rodar o servidor da API, use o `uvicorn`. Execute o comando abaixo para iniciar o servidor localmente:

```bash
uvicorn app.main:app --reload
```

A flag `--reload` garante que o servidor seja recarregado automaticamente sempre que você modificar o código.

### **5. Acessar a Documentação da API**

Após rodar o servidor, você pode acessar a documentação interativa da API no seguinte endereço:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Essa página foi gerada automaticamente pelo FastAPI e permite testar as rotas diretamente do navegador.

### **6. Testar a API**

#### Endpoint: `POST /shortest-route`

Este endpoint recebe uma lista de locais e retorna a menor rota entre eles.

**Exemplo de corpo da requisição:**
```json
{
  "locations": ["São Paulo, SP", "Rio de Janeiro, RJ", "Belo Horizonte, MG"]
}
```

A resposta será algo como:

```json
{
  "route": [
    [-23.55052, -46.633308],
    [-22.908333, -43.196388]
  ],
  "distance": 440.5
}
```

A lista de coordenadas `route` contém a rota otimizada entre os locais fornecidos e a distância total da rota em quilômetros.

## **7. Parar o Servidor**

Para parar o servidor, basta pressionar `Ctrl+C` no terminal onde o servidor está rodando.

## **8. Dúvidas ou Problemas?**

Caso você tenha alguma dúvida ou problema, consulte a documentação do FastAPI ou abra uma issue no repositório para que possamos ajudar.

---

### **Estrutura do Projeto**
Se você quiser explorar a estrutura do projeto, ela será organizada da seguinte forma:

```
my_route_api/
├── app/
│   ├── __init__.py
│   ├── main.py           # Arquivo principal para rodar o servidor FastAPI
│   ├── models.py         # Definições dos modelos de dados (ex. Request)
│   ├── routes.py         # Definição das rotas da API
│   └── utils.py          # Funções auxiliares, se necessário (ex. funções de geocodificação)
├── requirements.txt      # Dependências do projeto
├── README.md             # Documentação do projeto
└── .gitignore            # Arquivo para ignorar arquivos desnecessários no git
```

Com isso, você está pronto para testar e usar a API para calcular a menor rota entre diferentes locais.

--- 

Essa é a documentação completa para rodar o projeto da API. Se precisar de mais alguma coisa, é só me chamar!

