install:
    npm install
    poetry install

fmt:
    autopep8 wf_airtable_api_client

test:
    PYTHONPATH=./ pytest -s
