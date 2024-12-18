# python-bigquery-migrations

Python bigquery-migrations package is for creating and manipulating BigQuery databases easily.

Migrations are like version control for your database, allowing you to define and share the application's datasets and table schema definitions.

## Getting Started

## Install
```
pip install bigquery-migrations
```

## Create the project folder structure

Create two subdirectory:
1. credentials
2. migrations

```
your-project-root-folder
├── credentials
├── migrations
└── ...
```

## Create the neccessary files in the folders

Put your Google Cloud Service Account JSON file in the credentials subdirectory. See more info in the [Authorize BigQuery Client section](#authorize-bigquery-client)

Create your own migrations and put them in the migrations directory. See the [Migration structure section](#migration-structure) and [Migration naming conventions section](#migration-naming-conventions) for more info.

```
your-project
├── credentials
│   ├── gcp-sa.json
├── migrations
│   ├── 2024_12_01_120000_create_users_table.py
└── ...
```

## Running migrations

> **IMPORTANT!**  
> You have to create your own Migrations first! [Jump to Creating Migrations section](#creating-migrations)

To run all of your outstanding migrations, execute the `run` command:

```bash
bigquery-migrations run
```

You can specify the Google Cloud Project id witth the `--gcp-project-id` argument:

```bash
bigquery-migrations run --gcp-project-id
```

## Rolling Back Migrations

To reverse all of your migrations, execute the `reset` command:

```bash
bigquery-migrations reset
```

### Authorize BigQuery Client

Put your service account JSON file in the credentials subdirectory in the root of your project.

```
your-project
├── credentials
│   ├── gcp-sa.json
...
```

#### Creating a Service Account for Google BigQuery

You can connect to BigQuery with a user account or a service account. A service account is a special kind of account designed to be used by applications or compute workloads, rather than a person.

Service accounts don’t have passwords and use a unique email address for identification. You can associate each service account with a service account key, which is a public or private RSA key pair. In this walkthrough, we use a service account key in AWS SCT to access your BigQuery project.

To create a BigQuery service account key

1. Sign in to the [Google Cloud management console](https://console.cloud.google.com/).
1. Make sure that you have API enabled on your [BigQuery API](https://console.cloud.google.com/apis/library/bigquery.googleapis.com) page. If you don’t see API Enabled, choose Enable.
1. On the Service accounts page, choose your BigQuery project, and then choose Create service account.
1. On the [Service account](https://console.cloud.google.com/iam-admin/serviceaccounts) details page, enter a descriptive value for Service account name. Choose Create and continue. The Grant this service account access to the project page opens.
1. For Select a role, choose BigQuery, and then choose BigQuery Admin. AWS SCT uses permissions to manage all resources within the project to load your BigQuery metadata in the migration project.
1. Choose Add another role. For Select a role, choose Cloud Storage, and then choose Storage Admin. AWS SCT uses full control of data objects and buckets to extract your data from BigQuery and then load it into Amazon Redshift.
1. Choose Continue, and then choose Done.
1. On the [Service account](https://console.cloud.google.com/iam-admin/serviceaccounts) page, choose the service account that you created.
1. Choose Keys, Add key, Create new key.
1. Choose JSON, and then choose Create. Choose the folder to save your private key or check the default folder for downloads in your browser.

## Creating migrations

Put your migrations files in the migrations subdirectory of the root of your project.

```
your-project
├── migrations
│   ├── 2024_12_01_120000_create_users_table.py
...
```

### Migration structure

The migration class must contain two methods: `up` and `down`.

The `up` method is used to add new dataset, tables, columns etc. to your BigQuery project, while the `down` method should reverse the operations performed by the up method.

```python
from google.cloud import bigquery
from bigquery_migrations import Migration

class CreateUsersTable(Migration):
    """
    See:
    https://github.com/googleapis/python-bigquery/tree/main/samples
    """

    def up(self):
        # TODO: Set table_id to the ID of the table to create.
        table_id = "your_project.your_dataset.example_table"
        
        # TODO: Define table schema
        schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="NULLABLE"),
        ]
        table = bigquery.Table(table_id, schema=schema)
        table = self.client.create_table(table)
        print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        )

    def down(self):
        # TODO: Set table_id to the ID of the table to fetch.
        table_id = "your_project.your_dataset.example_table"
        
        # If the table does not exist, delete_table raises
        # google.api_core.exceptions.NotFound unless not_found_ok is True.
        self.client.delete_table(table_id, not_found_ok=True)
        print("Deleted table '{}'.".format(table_id))
```

### Migration naming conventions

|Pattern              |yyyy_mm_dd_hhmmss_your_class_name.py    |
|---------------------|----------------------------------------|              
|Example filename     |2024_12_10_120000_create_users_table.py |
|Example class name   |CreateUsersTable                        |
