# Connect, Combat and Conquer: MatcHub, Your Matchup Forum

![Intro-Art](/demo/Intro-Art.jpeg)

## What is Mathub?

[PT-BR]

MatcHub é um fórum para jogadores de [_League of Legends_](#1-league-of-legends-lol)$^1$, onde os usuários podem ler e descrever as vantagens e desvantagens de cada [_matchup_](#2-matchup)$^2$ do jogo. Seu objetivo é ser uma ferramenta rápida e assertiva para pesquisa estratégica, que pode ser empolgante e, em alguns momentos, desesperadora. Afinal, quem nunca correu para pesquisar a _matchup_ durante a tela de carregamento? Além disso, o MatcHub busca ser uma plataforma de interação, "aproveitando" o fato de a comunidade ser "excepcionalmente educada e prestativa", proporcionando um ambiente divertido que vai além de [_Summoner's Rift_](#3-summoners-rift)$^3$. Que tal compartilhar um pouco do seu conhecimento de [_monochampion_](#4-monochampion)$^4$ conosco? Sua habilidade como desenvolvedor também é bem-vinda, pois nem só de _LoL_ vive o [_lolzeiro_](#5-lolzeiro)$^5$.

[EN]

MatcHub is a forum for [_League of Legends_](#1-league-of-legends-lol)$^1$ players, where users can read and describe the advantages and disadvantages of each game [_matchup_](#2-matchup)$^2$. Its goal is to be a quick and assertive tool for strategic research, which can be exciting and, at times, desperate. After all, who hasn't rushed to research the _matchup_ during the loading screen? Moreover, MatcHub seeks to be an interaction platform, "taking advantage" of the fact that the community is "exceptionally polite and helpful," providing a fun environment that goes beyond [_Summoner's Rift_](#3-summoners-rift)$^3$. How about sharing some of your [_monochampion_](#4-monochampion)$^4$ knowledge with us? Your skills as a developer are also welcome, as a [_lolzeiro_](#5-lolzeiro)$^5$ life isn't just about _LoL_.

## Table of Content

* [How to Build?](#how-to-build)
    * [Cloning](#cloning)
    * [Environment Configuration](#environment-configuration)
    * [Docker](#docker)
* [About the project and submodules](#about-the-project-and-submodules)
* [Notes](#notes)

## How to Build?

Below, you will find a quick guide on how to clone, configure, and run the application.

### Cloning

This repository is unique because the folders are actually [links to other repositories](#6-subdirectory)$^6$ (to understand the reason behind this structure, see [About The Project and Submodules](#about-the-project-and-submodules)). Therefore, to clone the project with all submodules, use the following command:

```bash
git clone --recurse-submodules https://github.com/tarcidio/MatcHub.git
```

### Environment Configuration

For the application to function correctly, it is necessary to set up some environment variables in two files that need to be created:

* **File 1**: `.docker/secrets/secrets-env-api.env`
* **File 2**: `.docker/secrets/secrets-env-db.env`

These variables are crucial for connecting the application to the database, Gmail API, Riot, AWS services, and for activating the authentication and authorization systems of Spring Security. All instructions on how to obtain the necessary keys and fill out the files are detailed in the [ENV-INSTRUCTIONS.md file attached to this repository](https://github.com/tarcidio/MatcHub/blob/main/ENV-INSTRUCTIONS.md). Just like in this README.md, important concepts are explained to assist less experienced users, but these explanations are placed in notes to avoid overwhelming more advanced readers.

### Docker

The application has been configured to run in Docker containers. To run it, [Docker must be installed](#7-docker-and-how-install)$^7$. Execute the following command in the terminal, in the project directory:

```bash
docker-compose up -d --build
```

Since Maven needs to import all dependencies to create the `.jar` file, the first execution may take a few minutes.

To finish, do:

```bash
docker-compose down --rmi all
```

## About the Architecture

The application is structured around the standard components of a web application: frontend, backend, and infrastructure services. In the frontend, the highlight is the Angular framework, which uses HTML, CSS, and TypeScript. Angular is notable for its high responsiveness and dynamism, enhancing the user experience and promoting effective code development organization. However, these advantages come with a steeper learning curve, especially when compared to other libraries or frameworks such as React and Vue.

In the backend, the RESTful API that interacts with Angular is developed using the Spring framework, based on Java. Spring is highly valued for its excellent dependency management, facilitating the decoupling between code modules, and simplifying the configuration process. It integrates efficiently with subframeworks like Spring Security for managing authentication ([see about in the API repository](https://github.com/tarcidio/matchub-api)), authorization, and role control. The extensive community supporting Spring also broadens its use. Despite its numerous advantages, both Spring and Java have a significant learning curve, particularly when compared to technologies like JavaScript with Node.js for backend management.

For data management, PostgreSQL was chosen as the Relational Database Management System (RDBMS). It is the fourth most used RDBMS globally, standing out for its adherence to SQL standards and its extensibility, which allows integration with a variety of tools and supports the management of large volumes of data. Additionally, PostgreSQL offers a robust set of security features. To better understand the entities that generated the database, see [the API repository.](https://github.com/tarcidio/matchub-api)

Infrastructure services are predominantly provided by Amazon Web Services (AWS) and Google, playing crucial roles in specific operations within the application flow. For storing user images, we use AWS S3, known for its robustness and scalability. Moreover, for the asynchronous processing of events, such as sending email notifications, we employ AWS Lambda. This service allows for the efficient and scalable execution of event-based functions, optimizing the application's performance and resource management.

Below is a visual representation of the architecture:

![Architecture](/demo/Architecture-Diagram.png)

Some workflows that deserve emphasis:

1. **User Interaction with the Frontend**: The user accesses the site through a browser and performs actions such as uploading images, which are sent to AWS S3 via the API.
2. **Communication with the Backend**: The Frontend communicates with the Backend via API to perform CRUD operations (Create, Read, Update, Delete) on entities such as HubUser, Comment, and Evaluation.
3. **Asynchronous Processing**: Specific events trigger the sending of messages to AWS SQS, which in turn activates Lambda functions to process these events, such as sending email notifications.
4. **Sending Emails**: Emails are sent through integration with the Gmail API to notify users about relevant events or to confirm actions such as registration and password recovery.

It is important to note that the use of SQS and Lambda for sending emails is optional and was implemented to explore AWS functionalities, not being the main focus on high performance.

## About the project and submodules

This project was developed by [Tarcídio Antônio Júnior](https://www.linkedin.com/in/tarcidio/), under the guidance of the internship program at [Opus Software](https://www.opus-software.com.br/). In 2024, while pursuing a degree in Computer Science at the [University of São Paulo (USP)](https://www5.usp.br/), São Carlos campus, specifically at the [Institute of Mathematical and Computer Sciences (ICMC)](https://www.icmc.usp.br/), Tarcídio took on this challenge with the aim of applying the knowledge gained both in his undergraduate studies and during his internship. Throughout this period, the project proved to be an excellent opportunity to delve deeper into concepts such as RESTful APIs, Java, Spring, TypeScript, and Angular, all of which were thoroughly covered in the Opus internship program.

The development of the project followed a chronological sequence aligned with the internship's study plan. Initially, Tarcídio focused on modeling and implementing the database. He then moved on to developing the backend and concluded with the implementation of the frontend. The strategy of dividing the project into distinct parts, aimed at facilitating learning during the internship, led to the creation of separate repositories, interconnected by a main repository with submodules, proving to be an effective approach.

This project symbolizes not only the learning acquired but also Tarcídio's gratitude for the education received at USP and the professional growth opportunity provided by Opus Software.

Sou muito grato a todos vocês por esta querida jornada!

## Notes

### 1. _League of Legends (LoL)_

_League of Legends_ is an electronic game in the Multiplayer Online Battle Arena (MOBA) genre, developed and published by Riot Games. Since its release in October 2009, it has become one of the most popular and influential games in the world of electronic sports. The main objective is to destroy the opposing team's _Nexus_, a crucial structure located at the enemy's base. Players control characters known as "champions," each with unique abilities and distinct play styles.

[Return to text](#what-is-mathub)

### 2. _Matchup_

In the context of _League of Legends_, a "matchup" refers to the direct confrontation between two champions. This term is used to analyze how the abilities, strengths, and weaknesses of one champion compare to those of their opponent, directly influencing the strategy and outcome of matches, especially during the early game phase or in specific combats.

[Return to text](#what-is-mathub)

### 3. _Summoner's Rift_

_Summoner's Rift_ is the main and most iconic map of _League of Legends_. It serves as the battlefield for the majority of standard matches, both at amateur and professional levels.

[Return to text](#what-is-mathub)

### 4. _Monochampion_

The term "monochampion" describes a player who specializes almost exclusively in playing a single champion. These players dedicate most of their gameplay time to mastering all the nuances and strategies related to that specific champion, aiming for a high level of proficiency.

[Return to text](#what-is-mathub)

### 5. _Lolzeiro_

"Lolzeiro" is an informal term used in Brazil to describe someone who plays _League of Legends_. It is widely used within the gaming community.

[Return to text](#what-is-mathub)

### 6. Subdirectory

A subdirectory is any directory located within another directory in a repository. This system is used to organize files and folders in a hierarchical and logical manner. For example, the following commands were used to add subdirectories to the project:

```bash
git submodule add https://github.com/tarcidio/MatcHub-api MatcHub-api

git submodule add https://github.com/tarcidio/MatcHub-web MatcHub-web
```

To synchronize the `MatcHub-api` repository with the latest updates, execute:

```bash
cd MatcHub-api
git pull origin main

cd ..
git add MatcHub-api
git commit -m "Updated MatcHub-api submodule with latest changes"
git push
```

[Return to text](#cloning)

### 7. Docker and How Install

Docker is an open-source platform that enables developers to build, ship, and run applications within containers. Containers are lightweight and portable environments that package an application and all its dependencies into a single entity, ensuring that the application operates consistently across any computing environment. This facilitates collaboration among developers and the deployment of systems across various production, testing, or development environments, reducing the "it works on my machine" issues. To install Docker, [visit the official website](https://docs.docker.com/engine/install/) and follow the instructions.

[Return to text](#docker)




