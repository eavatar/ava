# -*- coding: utf-8 -*-
"""
Data engine implementation based on lighting memory database
(http://symas.com/mdb/).
The Lmdb is initialized, the access needs to use its binding API, though.
Extension packages may provide higher-level APIs based on this.
"""
from __future__ import absolute_import, division, unicode_literals

import os
import logging
import msgpack
import lmdb
import six
from ava.runtime import environ
from ava.util import time_uuid
from ava.spi.errors import DataNotFoundError, DataExistError

_DATA_FILE_DIR = b'data'

logger = logging.getLogger(__name__)


class DocStore(object):
    def __init__(self, name, _db, _engine):
        self.name = name
        self._db = _db
        self._engine = _engine

    def __len__(self):
        with self._engine.database.begin() as txn:
            stat = txn.stat(self._db)
            return stat['entries']

    def __getitem__(self, _id):
        with self._engine.cursor(self.name) as cur:
            return cur.get(_id)

    def __setitem__(self, _id, doc):
        with self._engine.cursor(self.name, readonly=False) as cur:
            doc['_id'] = _id
            cur.put(doc)

    def __delitem__(self, _id):
        with self._engine.cursor(self.name, readonly=False) as cur:
            cur.remove(_id)

    def __iter__(self):
        return self._engine.cursor(self.name)._cursor.iternext(
            keys=True, values=False)

    def save(self, doc):
        with self._engine.cursor(self.name, readonly=False) as cur:
            return cur.put(doc)

    def get(self, id):
        with self._engine.cursor(self.name, readonly=True) as cur:
            return cur.get(id)

    def cursor(self, readonly=True):
        return self._engine.cursor(self.name, readonly=readonly)


class DocCursor(object):
    def __init__(self, _txn, _db, _readonly=True):

        self._txn = _txn
        self._db = _db
        self._readonly = _readonly
        self._cursor = lmdb.Cursor(_db, _txn)

    def __enter__(self, *args, **kwargs):
        self._txn.__enter__(*args, **kwargs)
        self._cursor.__enter__(*args, **kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.__exit__(exc_type, exc_val, exc_tb)
        self._txn.__exit__(exc_type, exc_val, exc_tb)

    def first(self):
        return self._cursor.first()

    def next(self):
        return self._cursor.next()

    def prev(self):
        return self._cursor.prev()

    def last(self):
        return self._cursor.last()

    def current_doc(self):
        return msgpack.unpackb(self._cursor.value())

    def current_id(self):
        return self._cursor.key()

    def close(self):
        self._cursor.close()

    def value(self):
        """
        Gets raw value of the record.
        :return: record's value.
        """
        return self._cursor.value()

    def key(self):
        return self._cursor.key()

    def get(self, _id):
        key = _id
        if not self._cursor.set_key(key):
            return None

        return msgpack.unpackb(self._cursor.value())

    def load(self, _id):
        """
        Same as get method, except raising exception if entry not found.
        :param _id: the document's ID.
        :return: the document object.
        """
        key = _id
        ret = self.get(key)
        if ret is None:
            raise DataNotFoundError()
        return ret

    def delete(self):
        """
        Actually deletes document and its revisions if required.
        :return:
        """
        return self._cursor.delete(True)

    def remove(self, _id):
        """
        Delete the current element and move to the next, returning True on
        success or False if the store was empty
        :return:
        """
        if isinstance(_id, unicode):
            _id = _id.encode('utf-8')

        key = _id
        if not self._cursor.set_key(key):
            return None

        return self._cursor.delete(True)

    def seek(self, _id):
        """
        Finds the document with the provided ID and moves position to its first revision.

        :param docid:
        :return: True if found; False, otherwise.
        """
        key = _id
        if self._cursor.set_key(key):
            return True
        else:
            return False

    def seek_range(self, doc_id):
        """
        Finds the document whose ID is greater than or equal to the provided
        ID and moves position to its first revision.

        :param doc_id:
        :return:
        """

        return self._cursor.set_range(doc_id)

    def count(self):
        """
        Return the number of values (“duplicates”) for the current key.
        Only meaningful for databases opened with dupsort=True.
        :return:
        """
        return self._cursor.count()

    def pop(self):
        """
        Fetch the first document then delete it. Returns None if no value
        existed.
        :return:
        """
        if self._cursor.first():
            doc = self.current_doc()
            self._cursor.delete(True)
            return doc
        return None

    def put(self, doc):
        _id = doc.get('_id')

        if _id is None:
            _id = time_uuid.utcnow().hex
            key = _id
            doc['_id'] = _id
            self._cursor.put(key, msgpack.packb(doc))
            return _id

        if isinstance(_id, unicode):
            _id = _id.encode('utf-8')
            doc['_id'] = _id
        key = _id
        if self._cursor.set_key(key):
            # document exists.
            raise DataExistError()

        self._cursor.put(key, msgpack.packb(doc))
        return _id

    def post(self, doc):
        """
        Creates a new document revision.
        :param doc:
        :return: _id
        """
        _id = doc.get('_id')

        if _id is None:
            _id = time_uuid.utcnow().hex
            doc['_id'] = _id
            self._cursor.put(_id, msgpack.packb(doc))
            return _id

        _id = _id.encode('utf-8')
        self._cursor.put(_id, msgpack.packb(doc))
        return _id

    def exists(self, _id):
        if isinstance(_id, six.string_types):
            _id = _id.encode('utf-8')

        if self._cursor.set_key(_id):
            return True
        return False


class DataEngine(object):
    def __init__(self):
        logger.debug("Initializing data engine...")
        self.datapath = None
        self.database = None
        self.stores = {}

    def start(self, ctx=None):
        logger.debug("Starting data engine...")

        self.datapath = os.path.join(environ.pod_dir(), _DATA_FILE_DIR)
        logger.debug("Data path: %s", self.datapath)

        try:
            self.database = lmdb.Environment(self.datapath, max_dbs=1024)
            with self.database.begin(write=False) as txn:
                cur = txn.cursor()
                for k, v in iter(cur):
                    logger.debug("Found existing store: %s", k)
                    _db = self.database.open_db(k, create=False)
                    self.stores[k] = DocStore(k, _db, self)
        except lmdb.Error:
            logger.exception("Failed to open database.", exc_info=True)
            raise

        logger.debug("Data engine started.")

    def stop(self, ctx=None):
        logger.debug("Stopping data engine...")
        if self.database:
            self.database.close()

        logger.debug("Data engine stopped.")

    def store_names(self):
        return self.stores.keys()

    def create_store(self, name, revisions=True):
        try:
            _db = self.database.open_db(name, dupsort=revisions, create=True)
            store = DocStore(name, _db, self)
            self.stores[name] = store
            return store
        except lmdb.Error, e:
            logger.exception(e)
            raise

    def get_store(self, name):
        return self.stores.get(name)

    def remove_store(self, name):
        try:
            store = self.stores.get(name)
            if store is not None:
                with self.database.begin(write=True) as txn:
                    txn.drop(store._db)
                del self.stores[name]
        except lmdb.Error, e:
            logger.exception("Failed to remove store.", e)
            raise

    def remove_all_stores(self):
        for name in self.stores.keys():
            self.remove_store(name)

    def store_exists(self, name):
        return name in self.stores

    def cursor(self, store_name, readonly=True):
        _write = True
        if readonly:
            _write = False

        _db = self.database.open_db(store_name, create=False, dupsort=True)
        _txn = self.database.begin(write=_write, buffers=False)
        return DocCursor(_txn, _db, _readonly=readonly)

    def stat(self):
        ret = self.database.stat()
        return ret

    def __iter__(self):
        return self.stores.iterkeys()

    def __getitem__(self, store_name):
        return self.get_store(store_name)

    def __delitem__(self, store_name):
        return self.remove_store(store_name)
