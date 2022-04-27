# Rodando o projeto

## Docker
Inicialmente será necessário instalar o Docker e o docker-compose.

Em primeiro lugar iremos rodar o comando para buildar e subir nosso containers
```
docker-compose up -d --build
```
Após o comando acima ser executado, iremos verificar se os containers estão ativos
```
docker ps
```

caso apareça os dois containers parecido com a imagem abaixo, já podemos começar a consumir nossa API

![image](https://user-images.githubusercontent.com/44317074/165385358-f4896413-7249-42f0-ad23-19633ef7951e.png)


# Como testar a API
## Postman
Estarei disponibilizando as chamadas da API no [Postman](https://www.postman.com/lebaliro/workspace/docke/request/6500042-1ab95641-e682-4817-94f7-5a1f789d6352)


## Tests
A pasta de `test/` possui o coverage completo da API.

Para executa-lá basta escrever:
```
python manage.py test
```


# DER

![Untitled Diagram drawio](https://user-images.githubusercontent.com/44317074/165387662-8259211c-f238-4ed0-b4bf-3ed944d45cd7.png)
