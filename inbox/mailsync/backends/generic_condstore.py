"""
----------------------------------
GENERIC SYNC ENGINE WITH CONDSTORE
----------------------------------

IMAP backend with CONDSTORE support.

For providers that not provide server-side threading, so we have to thread
messages ourselves. Currently we make each message its own thread.
"""
from inbox.mailsync.backends.imap.condstore import CondstoreFolderSyncEngine
from inbox.mailsync.backends.imap.monitor import ImapSyncMonitor

__all__ = ['ImapCondstoreSyncMonitor']

PROVIDER = 'generic_condstore'
SYNC_MONITOR_CLS = 'ImapCondstoreSyncMonitor'


class ImapCondstoreSyncMonitor(ImapSyncMonitor):
    @property
    def sync_engine_class(self):
        return CondstoreFolderSyncEngine
