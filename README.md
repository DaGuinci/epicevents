# Epic Events
Openclassrooms study project - P12

## Table of contents <!-- omit in toc -->

- [1. Brief](#1-brief)
  - [1.1. Class diagram](#11-class-diagram)
  - [1.2. DB model](#12-db-model)
  - [1.3. Permissions](#13-permissions)
- [2. Upgrade suggestions](#2-upgrade-suggestions)
- [3. Documentation](#3-documentation)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Execution](#execution)

### 1. Brief

* Départements:
  * commercial
    * Cree/update profil client
  * support
    * Responsable org evenement
  * gestion
    * Cree contrat/associe contrat-client

#### 1.1. Class diagram

<!--

```plantuml
@startuml
skinparam backgroundColor #123749
skinparam roundcorner 20
skinparam classfontcolor lemon chiffon
skinparam titlefontcolor linen
skinparam arrowfontcolor linen
skinparam attributefontcolor linen

skinparam class {
BackgroundColor #123749
ArrowColor #EEB258
BorderColor #EEB258
AttributeFontColor linen
}
title Class diagram

  class User {
    - id: uuid
    - name: str
    - email: str
    - password: hashed_str
    - role: str
    - permissions: Permissions
    + getContracts(): list
    + getEvents(): list
    + getUsers(): list
  }

  class Commercial extends User {
    + createClient()
    + updateClient(Client)
    + createEvent()
    + updateContract(Contract)
  }

  class Manager extends User {
    + createUser()
    + updateUser(User)
    + deleteUser(User)
    + createContract()
    + updateContract(Contract)
    + assignSupportToEvent(Event, Support)
  }

  class Support extends User {
    + updateEvent(event)
  }

together {
  class Event {
    - id: int
    - contract_id: int
    - client_info: dict
    - date_start: str
    - date_end: str
    - epic_contact: Support
    - location: str
    - attendees: str
    - notes: str
    + method1(): ReturnType
  }

  class Contract {
    - id: int
    - client: Client
    - epic_contact: Commercial
    - total_amount: float
    - due_amount: float
    - date_created: str
    - signed_status: bool
    + get_client_infos(self.Client): dict
  }

  class Client {
    - id: int
    - name: str
    - email: str
    - phone: str
    - company: str
    - date_created: str
    - date_updated: str
    - epic_contact: Commercial
  }
}

Commercial "1" -down- "0..*" Client
Support "1" -- "0..*" Event
Commercial "1" -down- "0..*" Contract
Client "1" -right- "0..*" Contract
Contract "1" -right- "1" Event

@enduml
```
-->
![Alt text](README.svg)
<!--
' MyClass "1" -- "*" MyAssociatedObject -->
#### 1.2. DB model

![Alt text](ERD.svg)

#### 1.3. Permissions
  
* Tous
  * Acces lecture a toutes ressources

* Gestion
  * CRUD user
  * CRU contract
  * Acces events par filtre
  * Update event (associer un user support)
  * read all users
  * read all contracts
  * read all clients
  * read all events

* Commercial
  * creer clients
  * modifier clients propres
  * modifier contrats clients propres
  * acces contrat par filtre
  * créer evenement pour client contrat signé
  * read all users
  * read all contracts
  * read all clients
  * read all events
  
* Support
  * acces events par filtre
  * update events propres
  * read all users
  * read all contracts
  * read all clients
  * read all events

### 2. Upgrade suggestions

  - Add a companies table to retrieve clients from same company

### 3. Documentation

#### Installation

* Clone project
  
  ```bash
  git clone https://github.com/DaGuinci/epicevents.git
  ```
  
* Install dependencies
  ```bash
  pipenv install
  ```

* Activate environment
  ```bash
  pipenv shell
  ```

#### Configuration

* Create a database and fill the config.json with correct informations:   
*To use pytest, create a second database, but this is optionnal to run the application*
  
  ```json
  {
    "db_config":{
      "db_name":"your_database",
      "db_user":"your_user",
      "db_pass":"your_pass"
    },
    "test_db_config":{
      "db_name":"your_test_database",
      "db_user":"your_user",
      "db_pass":"your_pass"
    },
  }
  ```

* After this, to prevent git to commit your local informations:
  
  ```bash
  git update-index --skip-worktree config.json
  ```


#### Execution

* Launch the application
  
    ```bash
    python main.py
    ```