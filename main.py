''''Main file to run the API server'''

import uvicorn
from api.api import create_app


def main():
    '''Main function to run the API server'''
    app = create_app()
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
