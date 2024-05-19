# mabos/data_management/backup_exceptions.py

class BackupException(Exception):
    """Base class for backup-related exceptions."""
    pass

class BackupNotFoundError(BackupException):
    """Raised when a requested backup is not found."""
    pass

class BackupCorruptedError(BackupException):
    """Raised when a backup is found to be corrupted or invalid."""
    pass

class BackupStorageFullError(BackupException):
    """Raised when the backup storage is full and cannot accommodate new backups."""
    pass

class BackupPermissionDeniedError(BackupException):
    """Raised when the backup process does not have sufficient permissions to access the necessary resources."""
    pass

class BackupNetworkError(BackupException):
    """Raised when a network error occurs during the backup process."""
    pass

class BackupInterruptedError(BackupException):
    """Raised when the backup process is interrupted or terminated unexpectedly."""
    pass

class BackupRestoreError(BackupException):
    """Raised when an error occurs during the backup restoration process."""
    pass