
# PM 2.5 Data Analysis Application

## Running the Application

Clone the repo onto your local machine, open terminal and cd to breatheBattery

Ensure python3 is installed on your system

Open terminal and type 

```python3 --version```

If python is not installed then run

```brew install python3```

Run the following lines of code in the terminal:

```python3 -m venv venv```

```source venv/bin/activate```

```pip install -r requirements.txt```

```python3 main.py```

## Application Info

The application will create a local sqlite3 db, write all the data from the /device/<device_id>/history/ endpoint and then produce a csv report that will show when the PM 2.5 level is over 30, along with daily max, min and average

The application will run every ten seconds, to see if there's any new data from the api and write it to db (the report gets regenerated every ten seconds as well) 

It will also produce a .log file that gives insight into the how many records are getting added to the db etc

