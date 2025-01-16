import typer

from scanner.scanner import Scanner
from scanner.db_manager import DatabaseManager
from cve_detector.cve_detector import scan_for_cves

app = typer.Typer()


@app.command()
def init(directory: str):
    """
    Scan a directory, initialize the database, create stamp of current state and store metadata.
    """
    print(f"Creating a snapshot of the current state for directory: {directory}")
    metadata_list = Scanner(directory).scan_directory()
    DatabaseManager().update_or_insert_metadata(metadata_list)
    print(f"Initialization complete. Metadata stored in database.")


@app.command()
def scan(directory: str):
    """
    Scan the target directory and compare results with the last scan stored in the database.
    """
    print(f"Scanning directory: {directory}")
    scanner = Scanner(directory)
    db_manager = DatabaseManager()

    # Current metadata from the scan
    current_metadata_list = scanner.scan_directory()
    current_files = {metadata.path for metadata in current_metadata_list}

    # Metadata stored in the database
    stored_metadata = db_manager.get_all_metadata()

    # Compare results
    for metadata in current_metadata_list:
        stored_entry = stored_metadata.get(metadata.path)
        if stored_entry:
            # Check if file has been modified
            if (stored_entry[1] != metadata.generated_hash or
                    stored_entry[2] != metadata.size or
                    stored_entry[3] != metadata.permissions or
                    stored_entry[4] != metadata.owner or
                    stored_entry[5] != metadata.modified_time):
                print(f"Modified: {metadata.path}")
        else:
            # New file
            print(f"New file: {metadata.path}")

    # Detect deleted files
    for stored_file in stored_metadata.keys():
        if stored_file not in current_files:
            print(f"Deleted file: {stored_file}")


@app.command()
def update(directory: str):
    """
    Update the database with the current file state (when authorized changes were made).
    """
    print(f"Updating database for directory: {directory}")
    scanner = Scanner(directory)
    db_manager = DatabaseManager()

    # Current metadata from the scan
    current_metadata_list = scanner.scan_directory()
    current_files = {metadata.path for metadata in current_metadata_list}

    # Update database with new and modified files
    db_manager.update_or_insert_metadata(current_metadata_list)

    # Remove deleted files from the database
    db_manager.delete_removed_files(current_files)

    print(f"Database updated for directory: {directory}")


@app.command()
def cve_scan():
    """Scan the system and search for known CVEs."""
    print("Scanning system for known CVEs...")
    scan_for_cves()


@app.command()
def report():
    """
    Generate a detailed report on detected changes.
    """
    print("Report generation is not implemented yet.")


if __name__ == "__main__":
    app()
