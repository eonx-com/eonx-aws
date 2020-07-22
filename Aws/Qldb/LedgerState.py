from enum import Enum


class LedgerState(Enum):
    CREATING = 'CREATING'
    ACTIVE = 'ACTIVE'
    DELETING = 'DELETING'
    DELETED = 'DELETED'
