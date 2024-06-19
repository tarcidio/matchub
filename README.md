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
iam
grupo de politicas
usuario
s3
lambda
sqs

1. Criar um Bucket no S3
    1. **Acesse o AWS Management Console** e vá até o serviço Amazon S3.
    2. Clique em **Criar bucket**.
    3. Dê um nome único ao seu bucket e selecione a região.
    4. Configure as opções conforme necessário (por exemplo, desativar o acesso público, habilitar versionamento, etc.).
    5. Clique em **Criar bucket**.

### 2. Configurar um Usuário IAM e Políticas de Acesso

1. **Acesse o serviço IAM** no AWS Management Console.
2. Vá até **Usuários** e clique em **Adicionar usuário**.
3. Escolha um nome de usuário e marque a opção **Acesso programático**. Isso permitirá que a aplicação se autentique via API.
4. Clique em **Próximo: Permissões**.
5. Escolha **Anexar políticas existentes diretamente** e procure por políticas relacionadas ao S3 (como `AmazonS3FullAccess` para acesso total ou crie uma política personalizada para um acesso mais restrito).
6. **(Opcional) Crie uma política personalizada**:
   - Vá até **Políticas** e clique em **Criar política**.
   - Use o designer de políticas para adicionar permissões. Por exemplo, você pode especificar ações como `s3:PutObject`, `s3:GetObject`, e `s3:DeleteObject` e definir o recurso como o ARN do seu bucket.
   - Revise e nomeie sua política.
   - Anexe esta política ao usuário criado.


#### Riot

#### Spring Datasource and Postgres

#### Spring Security and JWT Token

#### Summary

### Docker



docker-compose up -d

## About the project and submodules



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






