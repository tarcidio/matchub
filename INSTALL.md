# Enviroment Variables

The API code imports environment variables to configure both Spring and Postgres. Some of these variables are not sensitive and have been directly incorporated into the Dockerfile, eliminating the need for additional configuration. However, other variables contain passwords, keys, and other sensitive data that require special care. To run the application, it is essential to create two files that import these sensitive variables. Next, it will be explained how to proceed with this configuration. For eager readers, here is a summary of the file names, paths and content to be created.

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
SPRING_DATASOURCE_USERNAME=your_spring_datasource_username_here
SPRING_DATASOURCE_PASSWORD=your_spring_datasource_password_here
SPRING_SECURITY_USER_NAME=your_spring_security_user_name_here
SPRING_SECURITY_USER_PASSWORD=your_spring_security_user_password_here
APPLICATION_SECURITY_JWT_EXPIRATION=your_application_security_jwt_expiration_here
APPLICATION_SECURITY_JWT_REFRESH_TOKEN_EXPIRATION=your_application_security_jwt_refresh_token_expiration_here
```
* **File 2**: `./matchub-api/docker/databse/secrets-env.env`

```.dotenv
POSTGRES_USER=your_postgres_user_here
POSTGRES_PASSWORD=your_postgres_password_here
```

_Note_: 
* `your_spring_datasource_username_here` and `your_postgres_user_here` must be the same.
* `your_spring_datasource_password_here` and `your_postgres_password_here` must be the same.

## Google API

The application relies on the Gmail API, which requires the creation and configuration of a project in the [Google Cloud Console](). Below, I present a simplified step-by-step guide to ensure everything is set up properly:

1. Access the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Activate the created project.
4. Navigate to "APIs & Services" > "Credentials" > "Create Credentials" > "OAuth client ID".
5. Download the JSON file containing the credentials.
6. Rename the downloaded file to `credentials.json`.
7. Transfer the file to the specific folder: `./matchub-api/matchub-api/src/main/resources/google/api/credentials/credentials.json`.

It is essential that the `credentials.json` file is renamed and placed precisely in the specified folder, according to the pre-established settings of the application. Any deviation from these instructions may lead to compilation errors. If it is necessary to adjust these settings, you will need to modify the `Dockerfile.api` located at `./matchub-api/matchub-api/docker/api/Dockerfile.api`.

Additionally, in the file `./matchub-api/docker/api/secrets-env.env`, configure the `GMAIL_API_FROM` variable to match the email associated with the project set up in the credential (for example: `GMAIL_API_FROM=nome.sobrenome@gmail.com`).

For more details on the credential acquisition process, consult the [note $^7$](#note--about-oauth-20-system-and-service-account).

## Amazon Web Services

The application relies on [Amazon Web Services (AWS)](), which requires specific configurations in the [AWS Management Console](). Below, I present a simplified step-by-step guide to ensure everything is set up correctly:

### Connection and Region Selection

1. [Create]() an AWS account to access the services.
2. [**Access the AWS Management Console**]().
3. In the top right corner, [select the desired region](). This will be the region where the S3 and SQS services will be stored.
4. In the file `secrets-env.env`, record the name of the region in `AWS_REGION`.

### Setting Up an S3 Bucket

1. **Access the AWS Management Console** and navigate to the Amazon S3 service.
2. Click on **Create bucket**.
3. Assign a unique name to your bucket.
4. Adjust the settings to allow public access, if necessary.
5. Confirm the creation by clicking on **Create bucket**.
6. In the file `secrets-env.env`, note the name of the bucket in `AWS_S3_BUCKET_HUBUSER_IMAGES`.

### Setting Up an SQS Queue

1. **Access the AWS Management Console** and locate the Amazon SQS service.
2. Click on **Create queue**.
3. Choose between a standard queue or a FIFO (First-In-First-Out) queue, as needed.
4. Set the attributes of the queue according to the desired specifications.
5. Finalize by clicking on **Create queue**.
6. In the file `secrets-env.env`, record the SQS URL in `AWS_SQS_EVALUATION_NOTIFICATION_URL`.

### Armazenar Credenciais Gmail API no AWS Secrets

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

### Criar [Camada para o Lambda]()

1. No painel de navegação à esquerda, clique em "Layers".
2. Clique em "Create layer".
3. Dê um nome e uma descrição para a camada
4. Faça upload do [arquivo ZIP que se encontra `./lambda/google-layer.zip`]()
5. Clique em "Create".

### Criar Lambda

1. **Acesse o AWS Management Console** e vá até o serviço Amazon Lambda.
2. Clique em "Create function".
3. Escolha "Author from scratch".
4. Insira um nome para a função.
5. Escolha o runtime Python 3.8
6. Crie a função Lambda
7. Em "Visão Geral" clique em "Add trigger" à esquerda
8. Na lista de triggers disponíveis, selecione "SQS".
9. Escolha a fila SQS que criou anteriormente
10. Configuraçãoes básicas são feitas automáticamente, mas pode configurar opções adicionais para o trigger
11. Salve a configuração
12. Vá na aba "Código" > "Origem do código" e cole o código anexado neste diretório `./lambda/evaluation-notification.py`
13. Vá em "Camadas" > "Adicionar uma camada"
14. Escolha a opção "Camada Personalizada"
15. Escolha a camada criada anteriormente
16. clique em "Adicionar"

### Configurar um Usuário IAM e Políticas de Acesso

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

## Riot Sign On (RSO)

A aplicação possui uma módulo para integração com a API Riot conhecida como Riot Sign On (RSO) para que o usuário conecte-se com sua conta Riot e possa associar sua conta com o nível de maestria com um determinado campeão. Nesse sentido, no arquivo 1 `secrets-env.env`, é necessário informar uma chave de desenvolvedor que se consegue pelo site da Riot. Porém, a integração ainda está em construção e a funcionalidade ainda não existe de forma que quem desejar rodar essa aplicação, no campo `RIOT_DEVELOPMENT_API_KEY`, basta deixar com algum texto aleatório e não haverá nenhuma complicação.

## Spring Datasource and Postgres

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

## Spring Security

Para gerenciar a segurança da aplicação, o Spring Security utiliza propriedades específicas para a autenticação básica, que são especialmente úteis durante o desenvolvimento ou em cenários de teste. Essas propriedades, que definem um usuário e uma senha padrão, foram configuradas por meio de variáveis de ambiente. Essas credenciais básicas facilitam a configuração inicial da segurança sem comprometer a funcionalidade da aplicação durante as fases de desenvolvimento e teste. Insira as informações necessárias no Arquivo 1, localizado em `./matchub-api/docker/api/secrets-env.env`.

```.dotenv
SPRING_SECURITY_USER_NAME=your_spring_security_user_name_here
SPRING_SECURITY_USER_PASSWORD=your_spring_security_user_password_here
```

## OAuth2.0

The authorization protocol selected to allow the user to have restricted access to the application is OAuth 2.0. To implement this protocol using Spring Security, it is essential to define three key parameters. These parameters have been configured as environment variables, as shown below.

### JWT Token Key

The first setting involves the secret key used to encrypt the signature of the tokens, specifically JWT tokens. It is crucial to choose a secure key and store it in File 1, located at `./matchub-api/docker/api/secrets-env.env`. You can generate a secure key using a site like [Random Key Gen](https://randomkeygen.com/), which provides robust options for key generation.

```.dotenv
JWT_SECRET_KEY=your_jwt_secret_key_here
```

Example: A key was generated using the [Random Key Gen](https://randomkeygen.com/) website:

```.dotenv
JWT_SECRET_KEY=3DB4BB34F8222535B67F875499413B41931C6BF1896262B682B8B8576D
```

## Expiration Time

The next two settings pertain to the expiration times of the access token and the refresh token, respectively, measured in seconds. While there are no strict limits on these values, it is advisable to set the refresh token's expiration time significantly longer than that of the access token to enhance security.

```.dotenv
APPLICATION_SECURITY_JWT_EXPIRATION=your_application_security_jwt_expiration_here
APPLICATION_SECURITY_JWT_REFRESH_TOKEN_EXPIRATION=your_application_security_jwt_refresh_token_expiration_here
```
For example, you might set the `JWT_EXPIRATION` to 15 minutes and the `JWT_REFRESH_TOKEN_EXPIRATION` to one day:

```.dotenv
APPLICATION_SECURITY_JWT_EXPIRATION=900000
APPLICATION_SECURITY_JWT_REFRESH_TOKEN_EXPIRATION=86400000
```

## Notes

### 1. Service Account

For clarification purposes, it is important to highlight that Google's Gmail API supports both the use of service accounts and the [OAuth 2.0]() system, with the latter being used in this application. A service account is a special type of user account intended to be used by applications, services, and machines, rather than people. These accounts are employed to provide an identity to processes that perform automated operations, such as sending automatic emails.

### 2.0 OAuth2.0

OAuth 2.0 is a widely adopted authorization protocol that allows third-party applications to obtain limited access to an HTTP service, usually on behalf of a user. It operates by issuing access tokens to authorized clients, who then use these tokens to access protected resources on a resource server. OAuth 2.0 is flexible and supports different authorization flows (grant types) to accommodate various application scenarios, such as web applications, mobile apps, and backend services. This flexibility facilitates secure integration between different systems, ensuring that only authorized users can access sensitive resources.

A "token" in the context of OAuth 2.0 is an encoded string that contains essential information for user authorization and client validation. There are mainly two types of tokens used: the access token and the refresh token (refresh token). The access token is used to make authenticated requests to the resource server, generally having a short validity period for security reasons. The refresh token has a longer lifespan and is used to obtain new access tokens without the user needing to authenticate again, improving the user experience by reducing the frequency of login requests. This ensures greater security, as if a malicious agent obtains the short-duration token, they will have limited time to use it and will need the long-lived token, which is usually stored more securely, to obtain a new short-duration token.

The JWT (JSON Web Token) is a specific type of access token that contains a set of claims (assertions) encoded in JSON format. These claims can include information about the user's identity, the token's validity, and other relevant data. The JWT is digitally signed, which ensures its integrity and authenticity, and can be encrypted to protect sensitive information against unauthorized interceptions. The use of JWTs in OAuth 2.0 is particularly useful in scenarios where performance is critical, as it allows for independent token validation, without the need to constantly consult an authentication server.

### 3. Amazon Web Service

* **Amazon Web Services (AWS)**: a platform offered by Amazon that provides a variety of basic infrastructure services such as computing, storage, security, etc. AWS also allows you to run applications in the cloud, reducing the need for investment in physical hardware and providing scalability and flexibility.
* **Identity and Access Management (IAM)**: an AWS service that allows you to manage access to AWS resources by creating AWS users, groups, and permissions, denying or authorizing access to AWS resources as configured.
* **IAM User**: an entity of AWS IAM to represent the person or service interacting with AWS. A user can be an individual, system, or application that needs access to AWS. Each IAM user can have associated credentials, such as passwords or access keys, which are used to authenticate their requests to AWS.
* **IAM Policy Group**: a set of permissions that you can assign to multiple users, groups, or roles within AWS. Policies are essentially JSON documents that specify the allowed or denied actions and the resources to which these actions apply.
* **AWS Secrets Manager**: a service that allows you to securely manage and retrieve secrets such as API keys, passwords, and previously stored tokens.
* **S3 (Simple Storage Service)**: an object storage service that offers scalability, data security, high availability, and performance.
* **SQS (Simple Queue Service)**: an asynchronous messaging service that allows you to send, store, and receive messages between software components (parts of a program developed independently)
* **Lambda**: a service that allows you to run code without provisioning or managing servers in response to events, such as receiving or changing data in another AWS service.

### 4. Custom IAM Policies and Policy Group

The user policies mentioned in the topic [Configure an IAM User and Access Policies]() are comprehensive, and it is highly recommended to develop custom policies specific to the S3 and SQS services. By doing this, you ensure that the user has access only to the relevant S3 bucket and SQS, and only to the pertinent actions, ensuring that users and services have only the permissions strictly necessary for their activities. It is also important to highlight the possibility of creating policy groups, which facilitates the consistency of permissions, management, reuse, and auditing. Although custom policies and policy groups are not essential for running the application, if you are interested in implementing them, the AWS IAM interface offers several guidelines to assist in this process.

### 5. Region Choice

When choosing a region to host services on AWS, consider both cost and efficiency to achieve an appropriate balance. The proximity of the selected region to the end users can reduce latency and enhance performance. Additionally, differences in service prices between regions can have a significant impact on operational costs. It is also essential to verify the availability of specific services in the chosen region, as not all AWS services are available in all regions. However, for this test application, it is unlikely that operational costs will exceed the free quota offered by AWS regardless of the region chosen.

### 6. Credit Card and Registration on AWS

To create an account on AWS, it is necessary to register a credit card. This card will only be used if the consumption of resources exceeds the free offer limit, which is generally unlikely. For those concerned about security, it is recommended to use a credit card with a short validity.

### 7. Spring and Spring Security

Spring is a widely used Java development framework designed to simplify the creation of complex applications. It provides a comprehensive infrastructure that supports the construction of high-performance and easy-to-maintain Java applications. One of the main features of Spring is the inversion of control (IoC), which helps in managing dependencies between components, allowing for looser coupling and greater modularity. Additionally, Spring supports integration with other Java technologies, such as JDBC, Hibernate, JPA, and many others, thus facilitating integration and scalability of systems.

Spring Security, on the other hand, is a powerful subproject of the Spring Framework that offers robust security features for Java applications. It focuses primarily on authentication and authorization, providing a comprehensive security model that can be customized and extended as needed. Spring Security facilitates the protection of applications against common threats, such as session fixation, clickjacking, cross-site request forgery attacks, among others. With flexible configuration and support for multiple authentication sources, including LDAP, database, and file-based authentication, Spring Security is a reliable choice for developers who need to implement robust security controls in their applications.