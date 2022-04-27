install:
    npm install
    poetry install

fmt:
    black wf_airtable_api_client

test:
    PYTHONPATH=./ pytest -s
