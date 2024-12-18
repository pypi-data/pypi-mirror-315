import os
import argparse
from pathlib import Path
from .migration_service import MigrationService
from .migration_manager import MigrationManager


def resolve_path(env_var):
    if not env_var:
        raise ValueError(f"The environment variable {env_var} is not set and no default is provided.")
    return Path(env_var).resolve()


def create_migrator(sa_dir: str, sa_fname: str, gcp_id: str, migrations_dir: str) -> MigrationManager:
    service = MigrationService(
        resolve_path(sa_dir),
        sa_fname,
        gcp_id,
        resolve_path(migrations_dir)
    )
    return service.create()


def run_migrations(migrator):
    try:
        migrator.run()
        print("Migration process completed successfully.")
    except Exception as e:
        print(f"Error during migration: {e}")


def list_migrations(migrator):
    print(migrator.list_migrations())


def reset_migrations(migrator):
    try:
        migrator.reset()
        print("Reset process completed successfully.")
    except Exception as e:
        print(f"Error during reset: {e}")


def main():
    parser = argparse.ArgumentParser(description="Perform BigQuery migrations")
    parser.add_argument(
        'command', choices=['list', 'run', 'reset'],
        help="Choose the operation to perform: list, run, reset"
    )
    parser.add_argument(
        '--gcp-sa-json-dir',
        help="Name of the service account JSON file directory (optional)"
    )
    parser.add_argument(
        '--gcp-sa-json-fname',
        help="Name of the service account JSON file (optional)"
    )
    parser.add_argument(
        '--migrations-dir',
        help="Name of the migrations directory (optional)"
    )
    parser.add_argument(
        '--gcp-project-id',
        help="Specify the Google Cloud Project ID (optional)"
    )

    args = parser.parse_args()

    gcp_sa_json_dir = args.migrations_dir or os.getenv('GCP_SA_JSON_DIR', 'credentials')
    gcp_sa_json_fname = args.migrations_dir or os.getenv('GCP_SA_JSON_FILENAME', 'gcp-sa.json')
    migrations_dir = args.migrations_dir or os.getenv('MIGRATIONS_DIR', 'migrations')
    gcp_project_id = args.gcp_project_id or os.getenv('GCP_PROJECT_ID')

    migrator = create_migrator(gcp_sa_json_dir, gcp_sa_json_fname, gcp_project_id, migrations_dir)

    if args.command == 'list':
        list_migrations(migrator)
    elif args.command == 'run':
        run_migrations(migrator)
    elif args.command == 'reset':
        reset_migrations(migrator)


if __name__ == "__main__":
    main()
