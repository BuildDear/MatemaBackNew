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

### Build docker image
```bash
docker build -t matema-back-new .
```

### Run docker container
```bash
docker run -d -p 8000:8000 matema-back-new
```
After this, the Calendario will be available at http://localhost:8000.


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


## Author
Matema backenders group


## Contacts
matema.group@gmail.com



