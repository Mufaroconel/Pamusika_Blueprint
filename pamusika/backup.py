import shutil

# Path to your original database
original_db_path = "instance/mumsikadatabase.db"
# Path for the backup
backup_db_path = "instance/mumsikadatabase_backup.db"

# Create a backup
shutil.copyfile(original_db_path, backup_db_path)

print("Backup created successfully.")
