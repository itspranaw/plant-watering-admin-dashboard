# To run

1. Create and activate the virtual environment 
  ```
  cd backend 
  python -m venv env
  Source env/bin/activate # for linux 
  env/Scripts/activate # for windows
  ```
2. Install the dependencies
  ```
  pip install -r requirements.txt
  ```
3. Run the backend
  ```
  uvicorn main:app --reload
  ```
4. Run the frontend
  ```
   cd ../frontend
   npm install
   npm start
  ```
## Also need to have MySQL server installed and running, create a .env folder with the following information in backend folder
```
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_HOST=
MYSQL_DB=plant_db
```
