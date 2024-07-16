# curso-django-project1
> Este repositório tem como intuito desenvolver um website usando a framework django do Python.

## Preview Website
<img src="https://i.ibb.co/NWYtGdz/print-django-app-recipes.png" alt="preview-website">

## Instalação dos requisitos
Recomenda-se que seja instalado em um ambiente virtual. Para criar uma é simples:
```sh
python3 -m venv venv
```

Ative o ambiente virtual (Windows)
```sh
.\venv\Scripts\activate
```

Ative o ambiente virtual (Linux)
```sh
./venv/bin/activate
```

Instale as dependências:
```sh
pip install -r requirements.txt
```

## Aplique as migrations:
```sh
python manage.py migrate
```

## Rodando o servidor com o website:
```sh
py manage.py runserver --insecure
```

Agora basta abrir a url gerada no terminal em seu navegador.

No meu caso é:
```sh
127.0.0.1:8000
```

## Rodando com Docker
Na pasta do projeto, digite o seguinte comando para "buildar" a aplicação:
```sh
docker build -t django/recipes-app .
```

Em seguida, rode:
```sh
docker run -d -p 8000:8000 --name recipes-app django/recipes-app
```

E... **voilà!!!** Você tem a aplicação rodando em um contêiner com docker! :D 
