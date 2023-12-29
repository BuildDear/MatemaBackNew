# About Myself

## Greetings

Hello,
We are a team of backend developers who have developed the BACKEND for the MATEMA program. 
We have put a lot of effort into it and hope that 
people from all over the world will find mathematics a bit more interesting and discover 
new horizons in the field of mathematics.🥰🥰🥰

## Prerequisites

Before you begin, you will need the following tools:

- **Python 3.10**
- **Docker**
- **Something for testing(Postman or related)**

## Installation

Follow these steps to install and run the project:

### Clone the Repository

```bash
git clone https://github.com/BuildDear/MatemaBackNew.git
```

### Enter the Project Directory
```bash
cd MatemaBackNew
```

### Configure Environment Variables
```bash
cp .env.example .env
```

#### Transfer .env into Matema app

### Build docker image
```bash
docker build -t matema-back-new .
```

### Build docker-compose
```bash
docker-compose build
```

### Run docker-compose
```bash
docker-compose up
```

After this, the MatemaBack will be available at http://localhost:8000.
Redis will be available at redis://127.0.0.1:6379/0.


### Run celery worker
```bash
celery -A Matema worker -l info
```
After this, worker must be connected to (broker, transport) redis://127.0.0.1:6379/0 .


### Run celery beat (if need)
```bash
 celery -A Matema beat -l info
```
After this, worker must be connected to (broker) redis://127.0.0.1:6379/0.


### Run celery flower (if need)
```bash
 celery -A Matema beat -l info
```
After this, worker must be connected to (broker) redis://127.0.0.1:6379/0.


### Swagger documentation of all endpoints(if need)

 http://127.0.0.1:8000/swagger/


## Author
Matema backenders group


## Contacts
matema.group@gmail.com



