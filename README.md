# topicos-back-end-trabalho-livros

## Participantes

| Nome    | RA |
| -------- | ------- |
| Bruno Vilardi Bueno  | 19.00331-5     |

## Overview
Trabalho realizado para a disciplina de Tópicos Avançados em Back End

Repositorio dividido em front end (/front), back end (/funcoes e /lambda_layer) e infraestrutura como código (/iac)

Endpoints funcionais para teste:

Front: https://d27g3rvb8o75cq.cloudfront.net/index.html

Back: https://r4gw3w34fg.execute-api.us-east-1.amazonaws.com/prod/feedback/

Documentação do Back: https://www.postman.com/speeding-sunset-812905/workspace/selfie-dev-maua/collection/16858667-bd1209c5-a221-47b6-9506-b5d5e2b11afc?action=share&creator=16858667

Info para fazer requisições do Back:
Rotas disponíveis: 
- GET ler-feedback (query_parameters: feedback_id: str)
- GET ler-todos-feedbacks
- POST enviar-feedback (body: json*)

Chave de API: 7YQaiuW0lq8d5HIvNzdBrafvB8q7J10l1t0NIOEF

*referência de json:
        
        {
            
            "produto":

                {

                    "id": "12345",

                    "nome": "Leite"  

                },

                "comentario": "gelado",

                "classificacao": 8

        }


## Diagrama de Arquitetura
![image](https://github.com/Brvilardi/topicos-back-end-trabalho-livros/blob/main/artefatos/t2-back.jpg?raw=true)


## Artefatos
- A coleção do postman pode ser encontrada via JSON na pasta /artefatos ou via link
- A coleção do API Gateway pode ser encontrada na pasta /artefatos

- As funções Lambda de cada rota podem ser encontradas na pasta /funcoes
- O código que é comum a todas as Lambdas pode ser encontrado na pasta /lambda_layer

- A infraestrutura foi 100% implementada usando infraestrutura como código com o AWS CDK e pode ser encontrada na pasta /iac

## Implementação

Para implementar o projeto basta seguir os seguintes passos:

Configurar o venv do CDK:
        cd iac

        python3 -m venv .venv

        source .venv/bin/activate

        pip install -r requirements.txt


Fazer o deploy da infra
        `dk bootstrap`

        `cdk deploy`

Buildar o front end
        cd front

        flutter pub get

        flutter build web

Implementar o front end
        cd build/web

        aws s3 cp . s3://<nome do bucket>  --recursive

Invalidar o cache
        Abrir console da AWS

        Acessar o serviço CloudFront

        Abrir a distribuição criada pelo IaC

        Clicar em "invalidações"

        Criar invalidação com "/*"

Acessar a aplicação
        
        Abrir via navegador a página pela URL do cloudfront + "/index.html"




