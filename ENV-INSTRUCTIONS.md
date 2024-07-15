# Enviroment Variables

![Env-Art](/demo/Env-Art.jpeg)

## Introduction

The MatcHub API code imports environment variables to configure both Spring and Postgres. Some of these variables are not sensitive and have been directly incorporated into the Dockerfile, eliminating the need for additional configuration. However, other variables contain passwords, keys, and other sensitive data that require special care. To run the application, it is essential to create two files that import these sensitive variables. Next, it will be explained how to proceed with this configuration. For eager readers, here is a summary of the file names, paths and content to be created.

* **File 1**: `.docker/secrets/secrets-env-api.env`

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
* **File 2**: `.docker/secrets/secrets-env-db.env`

```.dotenv
POSTGRES_USER=your_postgres_user_here
POSTGRES_PASSWORD=your_postgres_password_here
```

_Note_: 
* `your_spring_datasource_username_here` and `your_postgres_user_here` must be the same.
* `your_spring_datasource_password_here` and `your_postgres_password_here` must be the same.

## Table of Content

* [Google API](#google-api)
* [Amazon Web Services](#amazon-web-services)
    * [Connection and Region Selection](#connection-and-region-selection)
    * [Setting Up an S3 Bucket](#setting-up-an-s3-bucket)
    * [Setting Up an SQS Queue](#setting-up-an-sqs-queue)
    * [Storing Gmail API Credentials in AWS Secrets Manager](#storing-gmail-api-credentials-in-aws-secrets-manager)
    * [Creating a Layer for Lambda](#creating-a-layer-for-lambda)
    * [Setting Up a Lambda Function](#setting-up-a-lambda-function)
    * [IAM User Configuration and Access Policies](#iam-user-configuration-and-access-policies)
* [Riot Sign On (RSO)](#riot-sign-on-rso)
* [Configuration of Spring Datasource and Postgres](#configuration-of-spring-datasource-and-postgres)
* [Spring Security](#spring-security)
* [OAuth2.0](#oauth20)
    * [JWT Token Key](#jwt-token-key)
    * [Expiration Time](#expiration-time)
* [Notes](#notes)

## Google API

The application relies on the Gmail API, which requires the creation and configuration of a project in the [Google Cloud Console](#1-google-cloud-console)$^1$. Below is a simplified step-by-step guide to ensure everything is set up correctly:

1. Access the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Activate the created project.
4. Navigate to "APIs & Services" > "Credentials" > "Create Credentials" > "OAuth client ID".
5. Download the JSON file containing the credentials.
6. Rename the downloaded file to `credentials.json`.
7. Transfer the file to the specific folder: `./matchub-api/matchub-api/src/main/resources/google/api/credentials/credentials.json`.

It is essential that the `credentials.json` file is renamed and placed precisely in the specified folder, according to the pre-established settings of the application. Any deviation from these instructions may lead to compilation errors. If it is necessary to adjust these settings, you will need to modify the `Dockerfile.api` located at `./docker/dockerfiles/Dockerfile.api`.

Additionally, in the file `.docker/secrets/secrets-env-api.env`, configure the `GMAIL_API_FROM` variable to match the email associated with the project set up in the credential (for example: `GMAIL_API_FROM=nome.sobrenome@gmail.com`).

For more details on the credential acquisition process, consult the [note about Service Account and Auth2.0](#2-service-account)$^2$.

## Amazon Web Services

The application relies on [Amazon Web Services (AWS)](#4-amazon-web-service)$^4$, which requires specific configurations in the [AWS Management Console](https://aws.amazon.com/pt/console/). Below, I present a simplified step-by-step guide to ensure everything is set up correctly:

### Connection and Region Selection

1. [Create](#5-credit-card-and-registration-on-aws)$^5$ an AWS account to access the services.
2. [Access the AWS Management Console](https://aws.amazon.com/pt/console/).
3. In the top right corner, [select the desired region](#6-region-choice)$^6$. This will be the region where the S3 and SQS services will be stored.
4. In the file `secrets-env-api.env`, record the name of the region in `AWS_REGION`.

### Setting Up an S3 Bucket

1. [Access the AWS Management Console](https://aws.amazon.com/pt/console/) and navigate to the Amazon S3 service.
2. Click on **Create bucket**.
3. Assign a unique name to your bucket.
4. Adjust the settings to allow public access, if necessary.
5. Confirm the creation by clicking on **Create bucket**.
6. In the file `secrets-env-api.env`, note the name of the bucket in `AWS_S3_BUCKET_HUBUSER_IMAGES`.

### Setting Up an SQS Queue

1. [Access the AWS Management Console](https://aws.amazon.com/pt/console/) and locate the Amazon SQS service.
2. Click on **Create queue**.
3. Choose between a standard queue or a FIFO (First-In-First-Out) queue, as needed.
4. Set the attributes of the queue according to the desired specifications.
5. Finalize by clicking on **Create queue**.
6. In the file `secrets-env-api.env`, record the SQS URL in `AWS_SQS_EVALUATION_NOTIFICATION_URL`.


### Storing Gmail API Credentials in AWS Secrets Manager

1. [Access the AWS Management Console](https://aws.amazon.com/pt/console/) and navigate to the AWS Secrets Manager service.
2. Click on **Store a new secret**.
3. Choose the type of secret. For Gmail API credentials, select **Other type of secrets**.
4. Enter the `client_id` and `client_secret` credentials obtained from the `credentials.json` file. Store the credentials in a key-value format, as shown below:

```json
{
    "client_id": "seu_client_id",
    "client_secret": "seu_client_secret"
}
```

5. Click on **Next**.
6. Name your secret and, optionally, add a description.
7. Click on **Next** again to review the settings.
8. Click on **Store** to save the secret.
9. Note down the [ARN](#7-arn)$^7$ of this secret for later use.

### Creating a Layer for Lambda

1. [Access the AWS Management Console](https://aws.amazon.com/pt/console/) and go to the Amazon Lambda service.
2. In the left navigation panel, click on ["Layers"](#8-layers)$^8$.
3. Select "Create layer".
4. Name and describe your layer.
5. Upload the ZIP file located at `./lambda/google-layer.zip`.
6. Click on "Create".

### Setting Up a Lambda Function

1. [Access the AWS Management Console](https://aws.amazon.com/pt/console/) and go to the Amazon Lambda service.
2. Click on "Create function".
3. Choose "Author from scratch".
4. Enter a name for the function.
5. Select the Python 3.8 runtime.
6. Create the Lambda function.
7. In the "Overview" section, click on "Add trigger" on the left.
8. From the available triggers list, select "SQS".
9. Choose the previously created SQS queue.
10. Basic settings are applied automatically, but you can configure additional options for the trigger.
11. Save the settings.
12. In the "Code" > "Code source" tab, paste the code from the file `./lambda/evaluation-notification.py`.
13. Go to "Layers" > "Add a layer".
14. Select "Custom layer".
15. Choose the layer you previously created.
16. Click on "Add".

### IAM User Configuration and Access Policies

1. [Access the AWS Management Console](https://aws.amazon.com/pt/console/) and navigate to the **Amazon IAM** service.
2. Select the **Users** option and click on **Add user**.
3. Enter a username and select **Next: Permissions**.
4. Choose the option **Attach existing policies directly**.
5. Search for and select the [necessary policies](#9-custom-iam-policies-and-policy-group)$^9$ for S3 (`AmazonS3FullAccess` for full access) and for SQS (`AmazonSQSFullAccess` for full access), and attach them to the user.
6. Complete the user creation.
7. Store the access key ID and the secret access key in the variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in the file `secrets-env-api.env`.
8. Navigate to **Roles** and select the previously created Lambda function.
9. Click on **Add permissions** and then on **Inline Policies**.
10. Choose the **Secrets Manager** service.
11. In the JSON tab, insert the policy to access the previously created secret related to the Gmail API credentials. Modify the ARN as needed in the following JSON:
    
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

**Testing the Lambda Function:**
To check if the Lambda function is operating correctly, go to the SQS service, select the created queue, send the following message, and verify if the function is automatically activated and processes the message properly:

```json
{"email": "tarcidio.antonio@usp.br", "subject": "This is a test subject e-mail.", "text": "This is a test message e-mail."}
```

## Riot Sign On (RSO)

The application includes a module for integration with the Riot API, known as Riot Sign On (RSO). This feature allows users to connect with their Riot account and link their mastery level with a specific champion. To configure this functionality, it is necessary to enter a developer key in the `secrets-env-api.env` file, which can be obtained from the Riot website. Currently, the integration with RSO is under development, and the full functionality is not yet available. Therefore, for testing purposes, you can enter any random text in the `RIOT_DEVELOPMENT_API_KEY` field without causing any issues in running the application.

## Configuration of Spring Datasource and Postgres

As previously mentioned, the application uses Postgres as the Database Management System (DBMS) to store information on the server. To set up a Postgres instance, follow the detailed steps below:

1. In File 1, located at `.docker/secrets/secrets-env-db.env`, enter the username and password for Postgres. Choose these credentials carefully to ensure security.

```.dotenv
POSTGRES_USER=your_postgres_user_here
POSTGRES_PASSWORD=your_postgres_password_here
```

2. In File 2, found at `.docker/secrets/secrets-env-api.env`, repeat the username and password set previously. This repetition is crucial for the Spring API to establish an effective connection with the DBMS.

```.dotenv
SPRING_DATASOURCE_USERNAME=your_spring_datasource_username_here
SPRING_DATASOURCE_PASSWORD=your_spring_datasource_password_here
```

## Spring Security

To effectively manage the security of the application, we use [Spring Security](#10-spring-and-spring-security)$^{10}$, which supports specific properties for basic authentication. These properties are particularly useful during the development and testing phases, allowing for simplified security configuration without compromising the overall functionality of the application. The default user and password credentials are configured through environment variables, facilitating the initial implementation of security. Enter the necessary information in File 1, located at `.docker/secrets/secrets-env-api.env`.

```.dotenv
SPRING_SECURITY_USER_NAME=your_spring_security_user_name_here
SPRING_SECURITY_USER_PASSWORD=your_spring_security_user_password_here
```

## OAuth2.0

The authorization protocol selected to allow the user to have restricted access to the application is OAuth 2.0. To implement this protocol using Spring Security, it is essential to define three key parameters. These parameters have been configured as environment variables, as shown below.

### JWT Token Key

The first setting involves the secret key used to encrypt the signature of the tokens, specifically JWT tokens. It is crucial to choose a secure key and store it in File 1, located at `.docker/secrets/secrets-env-api.env`. You can generate a secure key using a site like [Random Key Gen](https://randomkeygen.com/), which provides robust options for key generation.

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

### 1. Google Cloud Console

The Google Cloud Console is a web-based administrative interface provided by Google for managing services and resources on the Google Cloud Platform (GCP). This platform is a comprehensive suite of cloud computing services offered by Google, used for a variety of applications, including, among others, the management of email sending automation and access to Google Drive. The console facilitates the administration of these services, allowing users to configure, monitor, and manage their applications and data efficiently and centrally.

[Return to text](#google-api)

### 2. Service Account

For clarification purposes, it is important to highlight that Google's Gmail API supports both the use of service accounts and the [OAuth 2.0](#3-oauth20)$^3$ system, with the latter being used in this application. A service account is a special type of user account intended to be used by applications, services, and machines, rather than people. These accounts are employed to provide an identity to processes that perform automated operations, such as sending automatic emails.

[Return to text](#google-api)

### 3. OAuth2.0

OAuth 2.0 is a widely adopted authorization protocol that allows third-party applications to obtain limited access to an HTTP service, usually on behalf of a user. It operates by issuing access tokens to authorized clients, who then use these tokens to access protected resources on a resource server. OAuth 2.0 is flexible and supports different authorization flows (grant types) to accommodate various application scenarios, such as web applications, mobile apps, and backend services. This flexibility facilitates secure integration between different systems, ensuring that only authorized users can access sensitive resources.

A "token" in the context of OAuth 2.0 is an encoded string that contains essential information for user authorization and client validation. There are mainly two types of tokens used: the access token and the refresh token (refresh token). The access token is used to make authenticated requests to the resource server, generally having a short validity period for security reasons. The refresh token has a longer lifespan and is used to obtain new access tokens without the user needing to authenticate again, improving the user experience by reducing the frequency of login requests. This ensures greater security, as if a malicious agent obtains the short-duration token, they will have limited time to use it and will need the long-lived token, which is usually stored more securely, to obtain a new short-duration token.

The JWT (JSON Web Token) is a specific type of access token that contains a set of claims (assertions) encoded in JSON format. These claims can include information about the user's identity, the token's validity, and other relevant data. The JWT is digitally signed, which ensures its integrity and authenticity, and can be encrypted to protect sensitive information against unauthorized interceptions. The use of JWTs in OAuth 2.0 is particularly useful in scenarios where performance is critical, as it allows for independent token validation, without the need to constantly consult an authentication server.

[Return to text](#google-api)

### 4. Amazon Web Service

* **Amazon Web Services (AWS)**: a platform offered by Amazon that provides a variety of basic infrastructure services such as computing, storage, security, etc. AWS also allows you to run applications in the cloud, reducing the need for investment in physical hardware and providing scalability and flexibility.
* **Identity and Access Management (IAM)**: an AWS service that allows you to manage access to AWS resources by creating AWS users, groups, and permissions, denying or authorizing access to AWS resources as configured.
* **IAM User**: an entity of AWS IAM to represent the person or service interacting with AWS. A user can be an individual, system, or application that needs access to AWS. Each IAM user can have associated credentials, such as passwords or access keys, which are used to authenticate their requests to AWS.
* **IAM Policy Group**: a set of permissions that you can assign to multiple users, groups, or roles within AWS. Policies are essentially JSON documents that specify the allowed or denied actions and the resources to which these actions apply.
* **AWS Secrets Manager**: a service that allows you to securely manage and retrieve secrets such as API keys, passwords, and previously stored tokens.
* **S3 (Simple Storage Service)**: an object storage service that offers scalability, data security, high availability, and performance.
* **SQS (Simple Queue Service)**: an asynchronous messaging service that allows you to send, store, and receive messages between software components (parts of a program developed independently)
* **Lambda**: a service that allows you to run code without provisioning or managing servers in response to events, such as receiving or changing data in another AWS service.

[Return to text](#amazon-web-services)

### 5. Credit Card and Registration on AWS

To create an account on AWS, it is necessary to register a credit card. This card will only be used if the consumption of resources exceeds the free offer limit, which is generally unlikely. For those concerned about security, it is recommended to use a credit card with a short validity.

[Return to text](#connection-and-region-selection)

### 6. Region Choice

When choosing a region to host services on AWS, consider both cost and efficiency to achieve an appropriate balance. The proximity of the selected region to the end users can reduce latency and enhance performance. Additionally, differences in service prices between regions can have a significant impact on operational costs. It is also essential to verify the availability of specific services in the chosen region, as not all AWS services are available in all regions. However, for this test application, it is unlikely that operational costs will exceed the free quota offered by AWS regardless of the region chosen.

[Return to text](#connection-and-region-selection)

### 7. ARN

The Amazon Resource Name (ARN) is a unique identifier used to distinctly identify resources within the Amazon Web Services (AWS) ecosystem. It ensures that resources are specified unambiguously across the platform, allowing AWS services to recognize and interact with resources from other services. An ARN is composed of several components that provide specific details about the resource. Its general structure is as follows:

```
arn:partition:service:region:account-id:resource-type/resource-id
```

Each component of the ARN serves a specific purpose:

* **arn**: Indicates that the string is an ARN.
* **partition**: A partition that denotes a specific subset of AWS resources. Commonly, this is "aws" for global resources or "aws-cn" for resources in China.
* **service**: The AWS service managing the resource (e.g., `s3` for Amazon S3, `ec2` for Amazon EC2).
* **region**: The AWS region where the resource is located (e.g., `us-east-1`). For resources not specific to any region, this field may be empty.
* **account-id**: The AWS account ID that owns the resource.
* **resource-type**: The type of the resource (e.g., `instance` for an EC2 instance).
* **resource-id**: A unique identifier for the resource within the service.

[Return to text](#storing-gmail-api-credentials-in-aws-secrets-manager)

### 8. Layers

A Layer is a way to import libraries, custom dependencies, or even common code that multiple Lambda functions may require. In this project, it was necessary to import the libraries `google.oauth2.credentials` and `google.auth.transport.requests` so that the Lambda function could access the Google API, as these libraries are not natively available on AWS.

[Return to text](#creating-a-layer-for-lambda)

### 9. Custom IAM Policies and Policy Group

The user policies mentioned in the topic [Configure an IAM User and Access Policies](#iam-user-configuration-and-access-policies) are comprehensive, and it is highly recommended to develop custom policies specific to the S3 and SQS services. By doing this, you ensure that the user has access only to the relevant S3 bucket and SQS, and only to the pertinent actions, ensuring that users and services have only the permissions strictly necessary for their activities. It is also important to highlight the possibility of creating policy groups, which facilitates the consistency of permissions, management, reuse, and auditing. Although custom policies and policy groups are not essential for running the application, if you are interested in implementing them, the AWS IAM interface offers several guidelines to assist in this process.

[Return to text](#iam-user-configuration-and-access-policies)

### 10. Spring and Spring Security

Spring is a widely used Java development framework designed to simplify the creation of complex applications. It provides a comprehensive infrastructure that supports the construction of high-performance and easy-to-maintain Java applications. One of the main features of Spring is the inversion of control (IoC), which helps in managing dependencies between components, allowing for looser coupling and greater modularity. Additionally, Spring supports integration with other Java technologies, such as JDBC, Hibernate, JPA, and many others, thus facilitating integration and scalability of systems.

Spring Security, on the other hand, is a powerful subproject of the Spring Framework that offers robust security features for Java applications. It focuses primarily on authentication and authorization, providing a comprehensive security model that can be customized and extended as needed. Spring Security facilitates the protection of applications against common threats, such as session fixation, clickjacking, cross-site request forgery attacks, among others. With flexible configuration and support for multiple authentication sources, including LDAP, database, and file-based authentication, Spring Security is a reliable choice for developers who need to implement robust security controls in their applications.

[Return to text](#spring-security)