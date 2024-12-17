# python-bigquery-migrations

Python bigquery-migrations package is for creating and manipulating BigQuery databases easily.

Migrations are like version control for your database, allowing you to define and share the application's datasets and table schema definitions.

## Typical project folder structure

```
your-project
├── credentials
│   ├── gcp-sa.json
├── migrations
│   ├── 2024_12_01_120000_create_users_table.py
├── src
│   ├── my_project_file.py
└── README.md
```

## Authorize Google BigQuery Client

Put your service account JSON file in the credentials subdirectory in the root of your project.

```
your-project
├── credentials
│   ├── gcp-sa.json
...
```

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
from src.bigquery_migrations.migration import Migration

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
        class_name = self.__class__.__name__
        print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        )

    def down(self):
        # TODO: Set table_id to the ID of the table to fetch.
        table_id = "your_project.your_dataset.example_table"
        
        # If the table does not exist, delete_table raises
        # google.api_core.exceptions.NotFound unless not_found_ok is True.
        self.client.delete_table(table_id, not_found_ok=True)
        class_name = self.__class__.__name__
        print("Deleted table '{}'.".format(table_id))
```

## Running migrations

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