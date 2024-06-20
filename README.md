# Connect, Combat and Conquer: MatcHub, Your Matchup Forum

![Descrição alternativa](imagem-intro.jpeg)

## What is Mathub?

[PT-BR]

Matchub é um fórum para jogadores de [_League of Legends_](#note--league-of-legends-lol)$^1$, onde os usuários podem ler e descrever as vantagens e desvantagens de cada [_matchup_ $^2$](#-matchup) do jogo. Seu objetivo é ser uma ferramenta rápida e assertiva para pesquisa estratégica, que pode ser empolgante e, em alguns momentos, desesperadora. Afinal, quem nunca correu para pesquisar a _matchup_ durante a tela de carregamento? Além disso, o Matchub busca ser uma plataforma de interação, "aproveitando" o fato de a comunidade ser "excepcionalmente educada e prestativa", proporcionando um ambiente divertido que vai além de [_Summoner's Rift_ $^3$](#-summoners-rift). Que tal compartilhar um pouco do seu conhecimento de [_monochampion_ $^4$](#-monochampion) conosco? Sua habilidade como desenvolvedor também é bem-vinda, pois nem só de _LoL_ vive o [_lolzeiro_ $^5$](#-lolzeiro).

[EN]

Matchub is a forum for [_League of Legends_ $^1$](#-league-of-legends-lol) players, where users can read and describe the advantages and disadvantages of each game [_matchup_ $^2$](#-matchup). Its goal is to be a quick and assertive tool for strategic research, which can be exciting and, at times, desperate. After all, who hasn't rushed to research the _matchup_ during the loading screen? Moreover, Matchub seeks to be an interaction platform, "taking advantage" of the fact that the community is "exceptionally polite and helpful," providing a fun environment that goes beyond [_Summoner's Rift_ $^3$](#-summoners-rift). How about sharing some of your [_monochampion_ $^4$](#-monochampion) knowledge with us? Your skills as a developer are also welcome, as a [_lolzeiro_ $^5$](#-lolzeiro) life isn't just about _LoL_.

## How build?

### Clone

Esse repositório é diferenciado, pois as pastas na verdade [apontam para outros repositórios $^6$](#-subdirectory) (se quiser saber o motivo de isso ter sido feito, ver [About The Project and Submodules](#about-the-project-and-submodules)). Assim, para clonar, é necessário seguir este comando:

````bash
git clone --recurse-submodules https://github.com/tarcidio/matchub.git
````

### Enviroment Variables

O código da API, desenvolvido em Java com o framework Spring, juntamente com a base de dados que utiliza o SGBD Postgres, importa variáveis de ambiente. Algumas dessas variáveis não são sensíveis e foram diretamente incorporadas no Dockerfile, eliminando a necessidade de configuração adicional. No entanto, outras variáveis contêm senhas, chaves e outros dados sensíveis que requerem cuidados especiais. Para executar a aplicação, é essencial criar dois arquivos que importem essas variáveis sensíveis. A seguir, será explicado como proceder com essa configuração. Para os leitores ansiosos, aqui vai um resumo dos nomes dos arquivos, caminhos e conteúdos a serem criados.

* **File 1**: `./matchub-api/docker/api/secrets-env.env`

```.dotenv
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
AWS_REGION=your_aws_region_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
AWS_S3_BUCKET_HUBUSER_IMAGES=your_aws_s3_bucket_hubuser_images_here
AWS_SQS_EVALUATION_NOTIFICATION_URL=your_aws_sqs_evaluation_notification_url_here
GMAIL_API_FROM=your_gmail_api_from_here
JWT_SECRET_KEY=your_jwt_secret_key_here
RIOT_DEVELOPMENT_API_KEY=your_riot_development_api_key_here
SPRING_DATASOURCE_PASSWORD=*your_spring_datasource_password_here
SPRING_DATASOURCE_USERNAME=your_spring_datasource_username_here
SPRING_SECURITY_USER_NAME=your_spring_security_user_name_here
SPRING_SECURITY_USER_PASSWORD=your_spring_security_user_password_here
APPLICATION_SECURITY_JWT_EXPIRATION=your_application_security_jwt_expiration_here
APPLICATION_SECURITY_JWT_REFRESH_TOKEN_EXPIRATION=your_application_security_jwt_refresh_token_expiration_here
```
* **File 2**: `./matchub-api/docker/databse/secrets-env.env`

```.dotenv
POSTGRES_USER=your_postgres_user_here
POSTGRES_PASSWORD=*your_postgres_password_here
```

_Note_: `your_spring_datasource_password_here` and `your_postgres_password_here` must be the same.

Vale lembrar que a aplicação utiliza a API do Gmail, fornecida pelo Google, para enviar e-mails aos usuários em determinadas situações. Para que isso funcione corretamente, é essencial que a aplicação esteja adequadamente conectada à API do Google, o que envolve a configuração de credenciais específicas. Esse processo inclui a criação de um projeto no [Google Cloud Console](#). [Abaixo](#google-api), você encontrará uma explicação sucinta de como obter essas credenciais.

Além disso, a aplicação também faz uso de [serviços da AWS, como S3, SQS e Lambda](), que são essenciais para diversas funcionalidades, como automatização do envio de e-mails, gerenciamento de imagens dos usuários e suporte a outras funcionalidades futuras. Para que a aplicação possa acessar esses serviços, é necessário configurar chaves e outras permissões que permitam a comunicação com a AWS. Informações detalhadas sobre esse processo serão abordadas no [tópico abaixo](#aws).

#### Google API

Conforme mencionado anteriormente, a aplicação utiliza a API do Gmail, o que requer a criação e configuração de um projeto no Google Cloud Console. Abaixo, você encontrará um guia passo a passo simplificado para configurar tudo corretamente:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto.
3. Ative o projeto.
4. Navegue até "APIs e Serviços" > "Credenciais" > "Criar Credenciais" > "ID do cliente OAuth".
5. Faça o download do arquivo JSON contendo as credenciais.
6. Renomeie o arquivo para `credentials.json`.
7. Mova o arquivo para a pasta específica: `./matchub-api/matchub-api/src/main/resources/google/api/credentials/credentials.json`.

É crucial que o arquivo `credentials.json` seja renomeado e colocado exatamente na pasta indicada, conforme as configurações predefinidas da aplicação. Qualquer desvio dessas instruções pode resultar em erros de compilação. Se for necessário fazer alterações nessas configurações, você precisará modificar o `Dockerfile.api` localizado em `./matchub-api/matchub-api/docker/api/Dockerfile.api`.

Por fim, no arquivo 1 (`./matchub-api/docker/api/secrets-env.env`), configure a variável `GMAIL_API_FROM` para ser igual ao email dono do projeto configurado na credencial (exemplos: `GMAIL_API_FROM=nome.sobrenome@gmail.com`).

Para informações adicionais sobre o processo de credenciamento, consulte a [nota $^7$](#note--about-oauth-20-system-and-service-account).

#### AWS

Como já informado, a aplicação utiliza os [serviços da AWS](), exigindo algumas configurações no [AWS Management Console](). Abaixo, você encontrará um guia passo a passo simplificado para configurar tudo corretamente:

1. Conecte-se e selecione a região
    1. [Crie]() uma conta na AWS para acessar os serviços
    2. [**Acesse o AWS Management Console**]()
    2. No canto superior direito, [selecione a região que desejar](). Será nesta região que armazenaremos os serviços S3 e o SQS
    3. No Arquivo 1 `secrets-env.env`, salve o nome da região em `AWS_REGION`

2. Criar um Bucket no S3
    1. **Acesse o AWS Management Console** e vá até o serviço Amazon S3.
    2. Clique em **Criar bucket**.
    3. Dê um nome único ao seu bucket
    4. Configure as opções para permitir acesso público
    5. Clique em **Criar bucket**.
    6. No Arquivo 1 `secrets-env.env`, salve o nome do bucket em `AWS_S3_BUCKET_HUBUSER_IMAGES`

3. Criar um SQS
    1. **Acesse o AWS Management Console** e vá até o serviço Amazon SQS.
    2. Clique em **Criar fila**.
    3. Escolha entre uma fila padrão ou uma fila FIFO (First-In-First-Out).
    4. Configure os atributos da fila conforme necessário
    5. Clique em **Criar fila**.
    6. No Arquivo 1 `secrets-env.env`, salve a url do SQS em `AWS_SQS_EVALUATION_NOTIFICATION_URL`

4. Armazenar Credenciais Gmail API no AWS Secrets
    1. **Acesse o AWS Management Console** e vá até o serviço AWS Secrets Manager
    2. Clique em **Store a new secret**.
    3. Escolha o tipo de segredo. Para credenciais da API do Gmail, você pode escolher **Other type of secrets**.
    4. Insira as credenciais da `client_id` e `client_secret` da API do Gmail adquiridas no arquivo `credentials.json`. Você pode armazenar as credenciais em formato chave-valor. Por exemplo:
    ```json
    {
        "client_id": "seu_client_id",
        "client_secret": "seu_client_secret"
    }
    ```
    5. Clique em **Next**.
    6. Dê um nome e, opcionalmente, uma descrição ao seu segredo.
    7. Clique em **Next** e revise as configurações.
    8. Clique em **Store** para salvar o segredo.
    9. Guarde o [ARN]() deste segredo para a etapa 7.

5. Criar [Camada para o Lambda]()
    1. No painel de navegação à esquerda, clique em "Layers".
    2. Clique em "Create layer".
    3. Dê um nome e uma descrição para a camada
    4. Faça upload do [arquivo ZIP que se encontra `./lambda/google-layer.zip`]()
    5. Clique em "Create".

6. Criar Lambda
    1. **Acesse o AWS Management Console** e vá até o serviço Amazon Lambda.
    2. Clique em "Create function".
    3. Escolha "Author from scratch".
    4. Insira um nome para a função.
    5. Escolha o runtime Python 3.8
    6. Crie a função Lambda
    7. Em "Visão Geral" clique em "Add trigger" à esquerda
    8. Na lista de triggers disponíveis, selecione "SQS".
    9. Escolha a fila SQS que criou anteriormente
    10. Configure as [opções adicionais]() para o trigger
    11. Salve a configuração
    12. Vá na aba "Código" > "Origem do código" e cole o código anexado neste diretório `./lambda/evaluation-notification.py`
    13. Vá em "Camadas" > "Adicionar uma camada"
    14. Escolha a opção "Camada Personalizada"
    15. Escolha a camada criada anteriormente
    16. clique em "Adicionar"

7. Configurar um Usuário IAM e Políticas de Acesso
    1. **Acesse o AWS Management Console** e vá até o serviço Amazon IAM.
    2. Vá até **Usuários** e clique em **Adicionar usuário**.
    3. Escolha um nome de usuário e clique em **Próximo: Permissões**.
    5. Escolha [**Anexar políticas existentes diretamente**]()
    6. Procure por políticas relacionadas ao S3 (como `AmazonS3FullAccess` para acesso total) e ao SQS (como `AmazonSQSFullAccess` para acesso total) e anexe
    7. Complete a criação do usuário
    8. Salve o ID da chave de acesso e chave de acesso secreta (credenciais de acesso) em, respectivamente, 
    `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` no Arquivo 1 `secrets-env.env`
    9. Vá até **Funções** e clique em na função Lambda criada na última etapa
    10. Clique em "Adicionar permissões" > "Políticas em Linha"
    11. Selecione o serviço Secrets Manager
    12. Clique em JSON e anexe a política para acessar o segredo criado anteriormente referente as credenciais do Gmail API. Segue o JSON base, devendo alterar o ARN referente ao segredo.
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": "secretsmanager:GetSecretValue",
                "Resource": "arn_aws_gmail_secrets"
            }
        ]
    }
    ```

Observação: para testar se a função Lambda está funcionando corretamente, é possível ir até o serviço SQS,selecionar a SQS criada, criar uma mensagem, enviar e verificar se a função Lambda é acionada automaticamente e processa a mensagem conforme esperado. Envie a seguinte mensagem:

```json
{"email": "tarcidio.antonio@usp.br", "subject": "This is a test subject e-mail.", "text": "This is a test message e-mail."}
```

#### Riot Sign On (RSO)

A aplicação possui uma módulo para integração com a API Riot conhecida como Riot Sign On (RSO) para que o usuário conecte-se com sua conta Riot e possa associar sua conta com o nível de maestria com um determinado campeão. Nesse sentido, no arquivo 1 `secrets-env.env`, é necessário informar uma chave de desenvolvedor que se consegue pelo site da Riot. Porém, a integração ainda está em construção e a funcionalidade ainda não existe de forma que quem desejar rodar essa aplicação, no campo `RIOT_DEVELOPMENT_API_KEY`, basta deixar com algum texto aleatório e não haverá nenhuma complicação.

#### Spring Datasource and Postgres

Como mencionado anteriormente, a aplicação utiliza o Postgres como Sistema de Gerenciamento de Banco de Dados (SGBD) para armazenar os dados no servidor. Para configurar uma instância do Postgres, é necessário inicialmente definir as variáveis de usuário. Após isso, essas informações devem ser integradas ao código da API, que estabelecerá a conexão com o SGBD. Siga os passos abaixo para a configuração:

1. No Arquivo 1, localizado em `./matchub-api/docker/database/secrets-env.env`, insira o nome de usuário e a senha. Escolha esses dados com cuidado!

```.dotenv
POSTGRES_USER=your_postgres_user_here
POSTGRES_PASSWORD=*your_postgres_password_here
```

2. No Arquivo 2, encontrado em `./matchub-api/docker/api/secrets-env.env`, insira o nome de usuário e a senha, utilizando exatamente os mesmos valores definidos na etapa anterior. Este procedimento habilitará a API Spring a estabelecer uma conexão eficaz com o SGBD.

```.dotenv
SPRING_DATASOURCE_USERNAME=your_spring_datasource_username_here
SPRING_DATASOURCE_PASSWORD=your_spring_datasource_password_here
```

#### Spring Security and JWT Token

Para gerenciar a segurança da aplicação, o Spring Security utiliza propriedades específicas para a autenticação básica, que são especialmente úteis durante o desenvolvimento ou em cenários de teste. Essas propriedades, que definem um usuário e uma senha padrão, foram configuradas por meio de variáveis de ambiente. Essas credenciais básicas facilitam a configuração inicial da segurança sem comprometer a funcionalidade da aplicação durante as fases de desenvolvimento e teste. Insira as informações necessárias no Arquivo 1, localizado em `./matchub-api/docker/api/secrets-env.env`.

```.dotenv
SPRING_SECURITY_USER_NAME=your_spring_security_user_name_here
SPRING_SECURITY_USER_PASSWORD=your_spring_security_user_password_here
```


o que é oauth2.0, token, jwt token, refresh token
valores esperados para expliração

JWT_SECRET_KEY=your_jwt_secret_key_here
APPLICATION_SECURITY_JWT_EXPIRATION=your_application_security_jwt_expiration_here
APPLICATION_SECURITY_JWT_REFRESH_TOKEN_EXPIRATION=your_application_security_jwt_refresh_token_expiration_here

### Docker

o que é docker
eh necessário ter instalado
basta executar:

docker-compose up -d

## About the project and submodules

on building

## Notes

###### Note $^1$: _League of Legends (LoL)_ 

Jogo eletrônico do gênero Multiplayer Online Battle Arena (MOBA), desenvolvido e publicado pela Riot Games. Lançado em outubro de 2009, é um dos jogos mais populares e influentes do mundo dos esportes eletrônicos cujo o objetivo é destruir o _Nexus_ (estrutura especial do mapa) da equipe adversária, localizado na base inimiga. Neste jogo, jogadores controlam personagens únicos chamados "campeões", cada um com habilidades específicas e estilos de jogo distintos.

###### Note $^2$: _matchup_

No jogo League of Legends, se refere a confronto direto entre dois personagens do jogo. Esse termo é usado para descrever como as habilidades, forças e fraquezas de um campeão se comparam às do campeão adversário, influenciando a estratégia e o resultado da partida na fase inicial do jogo ou em combates específicos.

###### Note $^3$: _Summoner's Rift_

Mapa principal e mais icônico do jogo _League of Legends_. É o campo de batalha onde a maioria das partidas padrão do jogo ocorre, tanto para partidas amadoras quanto profissionais.

###### NOte $^4$: _monochampion_ 

Refere-se a um jogador que se especializa em jogar com um único campeão quase exclusivamente. Esses jogadores dedicam a maior parte de seu tempo de jogo a dominar todas as nuances e estratégias associadas a esse campeão específico.

###### Note $^5$: _lolzeiro_ 

Termo informal usado no Brasil para se referir a uma pessoa que joga _League of Legends_.

###### Note $^6$: Subdirectory

Refere-se a qualquer diretório que esteja dentro de outro diretório no repositório. Esse sistema é utilizado para organizar arquivos e pastas de maneira hierárquica e lógica. Para fins de curiosidade, os seguintes comandos foram utilizados para criar esses subdiretórios:

```bash
git submodule add https://github.com/tarcidio/matchub-api matchub-api

git submodule add https://github.com/tarcidio/matchub-web matchub-web
```

Suponha que o repositório `matchub-api` seja atualizado. Para sincronizar com as novas versões, basta executar:

```bash
cd matchub-api
git push origin nome-da-branch

cd ..
git add matchub-api
git commit -m "Atualizado submódulo matchub-api com as últimas alterações"
git push
```

###### Note $^7$: About Oauth 2.0 System and Service Account

Para fins de esclarecimento, é importante destacar que a API do Gmail do Google suporta tanto o uso de contas de serviço quanto o sistema OAuth 2.0, sendo este último utilizado nesta aplicação. Uma conta de serviço é um tipo especial de conta de usuário destinada a ser utilizada por aplicações, serviços e máquinas, ao invés de pessoas. Essas contas são empregadas para fornecer uma identidade a processos que realizam operações automatizadas, como o envio de e-mails automáticos.

Por outro lado, OAuth 2.0 é um protocolo de autorização amplamente adotado que permite que aplicações terceirizadas obtenham acesso limitado a um serviço HTTP, seja em nome de um usuário ou em nome da própria aplicação. Esse protocolo opera com base em tokens, que são strings codificadas contendo um conjunto de informações utilizadas para autenticar um usuário ou dispositivo e autorizar o acesso a recursos específicos. No contexto do OAuth 2.0, o usuário autorizado recebe dois tipos de tokens: um token de curta duração e um token longevo. Para realizar suas atividades, a aplicação utiliza o token de curta duração e, quando este expira, solicita uma renovação utilizando o token longevo. Isso garante uma maior segurança, pois, caso um agente mal-intencionado obtenha o token de curta duração, ele terá um tempo limitado de uso e precisará do token longevo, que geralmente é armazenado de forma mais segura, para obter um novo token de curta duração.

###### Note $^8$: AWS Service

* **Amazon Web Services (AWS)**: plataforma, oferecida pela Amazon, que fornece uma variedade de serviços básicos de infraestrutura como computação, armazenamento, segurança, etc. AWS também permite que execute aplicações na nuvem, reduzindo a necessidade de investimento em hardware físico e proporcionando escalabilidade e flexibilidade.
* **IAM (Identity and Access Management)**: serviço da AWS que permite gerenciar o acesso aos recursos da AWS através da criação de usuários, grupos da AWS e permissões, negando ou autorizando o acesso aos recursos da AWS conforme configurado.
* **Usuário IAM**: entidade do AWS IAM para representar a pessoa ou serviço que interage com a AWS. Um usuário pode ser um indivíduo, sistema ou aplicação que necessita de acesso à AWS. Cada usuário IAM pode ter credenciais associadas, como senhas ou chaves de acesso, que são usadas para autenticar suas solicitações à AWS.
* **Grupo de Políticas IAM**: conjunto de permissões que você pode atribuir a múltiplos usuários, grupos ou funções dentro da AWS. As políticas são essencialmente documentos JSON que especificam as ações permitidas ou negadas e os recursos aos quais essas ações se aplicam.
* **AWS Secrets Manager**: serviço que permite gerenciar e recuperar, de forma segura, segredos como chaves de API, senhas e tokens anteriormente armazeados.
* **S3 (Simple Storage Service)**: serviço de armazenamento de objetos que oferece escalabilidade, segurança de dados, alta disponibilidade e performance.
* **SQS (Simple Queue Service)**: serviço assincrono de mensagem que permite enviar, armazenar e receber mensagens entre componentes de software (partes de um programa desenvolvido de forma independente)
* **Lambda**: serviço que permite executar código sem provisionar ou gerenciar servidores em respostas a eventos, como recebimento ou mudança de dados em um outro serviço da AWS.

###### Nota: Políticas AWS

    Observações sobre políticas:
    * As políticas citadas acima são gerais, porém recomendamos fortemente que sejam criadas políticas personalizadas para a manipulação. Assim, o usuário conseguirá manipular apenas o bucket S3 e o SQS que lhe diz respeito e apenas poderá fazer ações que fazem sentido ,garantindo que usuários e serviços tenham apenas as permissões estritamente necessárias para realizar suas tarefas
    * É possível criar também grupos de políticas, facilitando consistência de permissões, gerenciamento, reutilização e auditoria
    * Nenhuma das observação acima é necessária ser implementada para execução da aplicação. Caso seja do seu interesse implementar, a interface AWS IAM tem diversas indicações para orientar. 

###### Trigger pode ter configurações de permissão adicionais, mas é configurado automaticamente


###### Relação região, custo e eficiência


###### Car~tao de credito para logar na AWS

. Eles requerem cartão de crédito apenas para o caso da aplicação exeder o uso gratuito dos recursos, o que é raro. Para o leitor desconfiado, utilize um cartão de longevidade curta

###### Spring e Spring Security

framework de segurança que faz parte do ecossistema Spring
fornece mecanismos de autenticação, Autorização, roteção contra ataques comuns, Integração com o Spring Framework


