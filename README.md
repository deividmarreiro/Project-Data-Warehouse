# Introduction

In this Udacity Project, we are helping a streaming startup, Sparkify to move their data to the cloud.
We builded a ETL process, to read the data from a Amazon S3 bucket and send to a Amazon Redshift database and create the analytics tables from the raw data.

# Datasets

The datasets used in this project was provided by the Udacity in the a public S3 bucket.

One of the buckets contains the songs and artist data and the second one has the user events on the app.
The datasets are in the format of json.

# Schema

We have the staging tables and the star schema.

*In the end of this section their a image of the schema*

## Staging Tables

- stage_events - table with the info about the user events
- stage_songs - table with the info about the data song and artists

## Dimesion Tables

- dim_user - the table who holds the user data
- dim_song - the table who holds the song data
- dim_artist - the table who holds the artist data
- dim_time - the table who holds the time data

## Fact Table

- fact_songplay - records of the events linked to the songs

![diagram](/images/udacity_diagram.png)


# Configuration and Setup

You have two ways to run the project

- 1. Using the Terraform to configurate all you need in the AWS
- 2. Configure manually on the AWS Console and set the local variables
- 3. Copy the local_dwh.cfg and save as dwh.cfg

But first of all you need to:
- Create the IAM User in the AWS Console.
- Give the needed access AdministratorAccess and attach policies.

## 1. Using Terraform

- 1. Create the venv and install the dependencies
  
```sh
    poetry shell && poetry install
```

- 2. Set the AWS SECRET_KEY and SECRET_ID

```sh
 export AWS_SECRET_ACCESS_KEY=...
 export AWS_ACCESS_KEY_ID=...
```

- 3. Run the command bellow, who will create the terraform plan and run the terraform apply and set the needed envvars

```sh
    make setup
```

- 4. Now just run the create_tables.py and the etl.py

```sh
    python3 create_tables.py && python3 etl.py
```

- 5. And in the end, run the command bellow to destroy the AWS services created.
  
```sh
    make destroy
```

## 2. Setting manually

- Use access key and secret key to create clients for IAM and Redshift.
- Create an IAM Role that makes Redshift able to access S3 bucket (ReadOnly)
- Create a RedShift Cluster and get the DWH_ENDPOINT(Host address) and DWH_ROLE_ARN and fill the config file with the same information in the local_dwh.cfg.

- Update the dwh.cfg with the needed information.

- Now just run the create_tables.py and the etl.py

```sh
    python3 create_tables.py && python3 etl.py
```