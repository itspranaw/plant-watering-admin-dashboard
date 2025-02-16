TO run

1. Create and activate the virtual environment 
  ```
  cd backend 
  python -m venv env
  Source env/bin/activate # for linux 
  env/Scripts/activate # for windows
  ```
3. Install the dependencies
  ```
  pip install -r requirements.txt
  ```
5. Run the backend
  ```
  uvicorn main:app --reload
  ```
7. Run the frontend
  ```
   cd ../frontend
   npm install
   npm start
  ```
