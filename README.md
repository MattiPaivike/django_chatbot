# Django OpenAI-Powered Chatbot with HTMX Streaming

![Demo](images/demo.gif)

While searching the web for an example of a Django-based LLM chatbot featuring asynchronous streaming, I found no suitable examples that incorporated HTMX and async. This prompted me to put together this repository.

### Key Features
* Asynchronous Streaming: This project leverages the HTMX websockets extension and Django's AsyncWebsocketConsumer to achieve real-time, streaming interactions with the chatbot.
* OpenAI Integration: Utilizes AsyncOpenAI client for seamless communication with OpenAI's API.
* Conversation History: Enhances user experience by maintaining a history of interactions, allowing the chatbot to provide contextually relevant responses.

Can be adapted to work with open-source Large Language Models like Llama-3, provided that the HTTP client handling communications with the LLM supports asynchronous operations.

## Notes about deploying to production

Because websockets requires ASGI instead of WSGI server, you should use something like Uvicorn: https://www.uvicorn.org/ to serve your application. I provided an example how to set this up in the `docker-compose.yml` file. Check out the additional environment variables in there if you plan on deploying this. Inside the `django_chatbot_app/chatbot/settings.py` file we check `ENVIRONMENT` variable to determine if we are in production or development mode. In development mode we use `daphne` ASGI server that is not suitable for production. Also take a look at `scripts/gunicorn/gunicorn_config.py` this is where we configure the gunicorn server to use Uvicorn as the worker in production.

## Running the application locally:

- Create OpenAI api key at: https://platform.openai.com/ 
- Create `.env` file to the root directory. Example: `.env_example`

- Create your virtual environment and install dependencies:
```
pip install -r requirements.txt
```

Note that the `requirements_prod.txt` file should only be used in "production" setup (docker-compose.yaml). See the `Dockerfile` for more information.

- Run migrations and runserver
```
python manage.py migrate
python manage.py runserver
```

- Create a user for the application and start chatting.

## Running the application in docker-compose (production-like setup):

- Create OpenAI api key at: https://platform.openai.com/ 
- Create `.env` file to the root directory. Example: `.env_example`.

```
docker-compose build
docker-compose up
```

The application is available at `http://127.0.0.1:8000`
