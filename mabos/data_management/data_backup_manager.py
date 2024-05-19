# mabos/data_management/data_backup_manager.py
from mabos.logging.logger import Logger
from mabos.configuration.configuration_manager import ConfigurationManager
from mabos.data_management.backup_storage import BackupStorage
from mabos.data_management.backup_scheduler import BackupScheduler
from mabos.data_management.backup_purger import BackupPurger
from mabos.data_management.backup_exceptions import BackupNotFoundError, BackupNetworkError, BackupInterruptedError, BackupRestoreError


class DataBackupManager:
    def __init__(self, backup_storage):
        self.backup_storage = backup_storage
        # Initialize other attributes and components
        self.backup_storage = backup_storage
        self.logger = Logger()
        self.config_manager = ConfigurationManager()
        self.backup_scheduler = BackupScheduler()
        self.backup_purger = BackupPurger(retention_period=self.config_manager.get_configuration('backup_retention_period'))

    def create_backup(self, data):
        # Create a backup of the given data
        backup_id = self.backup_storage.create_backup(data)
        self.logger.log(f"Backup created with ID: {backup_id}")
        return backup_id

    def restore_backup(self, backup_id):
        # Restore data from a specific backup
        try:
            data = self.backup_storage.restore_backup(backup_id)
            self.logger.log(f"Backup restored successfully. Backup ID: {backup_id}")
            return data
        except BackupNotFoundError as e:
            # Handle backup not found error
            self.logger.log(f"Error restoring backup: {str(e)}", level="error")
            raise
        except BackupNetworkError as e:
            # Handle network error during restore
            self.logger.log(f"Network error during backup restore: {str(e)}", level="error")
            raise
        except BackupInterruptedError as e:
            # Handle restore interruption
            self.logger.log(f"Backup restore interrupted: {str(e)}", level="error")
            raise
        except BackupRestoreError as e:
            # Handle restore error
            self.logger.log(f"Error during backup restore: {str(e)}", level="error")
            raise

    def schedule_backup(self, data, schedule):
        # Schedule a recurring backup of the data
        backup_job = self.backup_scheduler.schedule_backup(data, schedule)
        self.logger.log(f"Backup scheduled. Job ID: {backup_job.id}")

    def purge_old_backups(self, retention_period):
        purged_backups = self.backup_purger.purge_backups(retention_period)
        self.logger.log(f"Purged {len(purged_backups)} backups older than {retention_period} days")
        pass