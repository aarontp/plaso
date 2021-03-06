#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the Windows recycler parsers."""

import unittest

from plaso.formatters import recycler as _  # pylint: disable=unused-import
from plaso.lib import eventdata
from plaso.lib import timelib
from plaso.parsers import recycler

from tests.parsers import test_lib


class WinRecycleBinParserTest(test_lib.ParserTestCase):
  """Tests for the Windows Recycle Bin parser."""

  def testParseVista(self):
    """Tests the Parse function on a Windows Vista RecycleBin file."""
    parser_object = recycler.WinRecycleBinParser()
    storage_writer = self._ParseFile([u'$II3DF3L.zip'], parser_object)

    self.assertEqual(len(storage_writer.events), 1)

    event_object = storage_writer.events[0]

    expected_filename = (
        u'C:\\Users\\nfury\\Documents\\Alloy Research\\StarFury.zip')
    self.assertEqual(event_object.original_filename, expected_filename)

    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2012-03-12 20:49:58.633')
    self.assertEqual(event_object.timestamp, expected_timestamp)
    self.assertEqual(event_object.file_size, 724919)

    expected_message = u'{0:s} (from drive: UNKNOWN)'.format(expected_filename)
    expected_message_short = u'Deleted file: {0:s}'.format(expected_filename)
    self._TestGetMessageStrings(
        event_object, expected_message, expected_message_short)

  def testParseWindows10(self):
    """Tests the Parse function on a Windows 10 RecycleBin file."""
    parser_object = recycler.WinRecycleBinParser()
    storage_writer = self._ParseFile([u'$I103S5F.jpg'], parser_object)

    self.assertEqual(len(storage_writer.events), 1)

    event_object = storage_writer.events[0]

    expected_filename = (
        u'C:\\Users\\random\\Downloads\\bunnies.jpg')
    self.assertEqual(event_object.original_filename, expected_filename)

    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2016-06-29 21:37:45.618')
    self.assertEqual(event_object.timestamp, expected_timestamp)
    self.assertEqual(event_object.file_size, 222255)

    expected_message = u'{0:s} (from drive: UNKNOWN)'.format(expected_filename)
    expected_message_short = u'Deleted file: {0:s}'.format(expected_filename)
    self._TestGetMessageStrings(
        event_object, expected_message, expected_message_short)


class WinRecyclerInfo2ParserTest(test_lib.ParserTestCase):
  """Tests for the Windows Recycler INFO2 parser."""

  def testParse(self):
    """Reads an INFO2 file and run a few tests."""
    parser_object = recycler.WinRecyclerInfo2Parser()
    storage_writer = self._ParseFile([u'INFO2'], parser_object)

    self.assertEqual(len(storage_writer.events), 4)

    event_object = storage_writer.events[0]

    expected_timestamp = timelib.Timestamp.CopyFromString(
        u'2004-08-25 16:18:25.237')
    self.assertEqual(event_object.timestamp, expected_timestamp)
    self.assertEqual(
        event_object.timestamp_desc, eventdata.EventTimestamp.DELETED_TIME)

    self.assertEqual(event_object.record_index, 1)

    expected_filename = (
        u'C:\\Documents and Settings\\Mr. Evil\\Desktop\\lalsetup250.exe')
    self.assertEqual(event_object.original_filename, expected_filename)

    event_object = storage_writer.events[1]

    expected_message = (
        u'DC2 -> C:\\Documents and Settings\\Mr. Evil\\Desktop'
        u'\\netstumblerinstaller_0_4_0.exe (from drive: C)')
    expected_message_short = (
        u'Deleted file: C:\\Documents and Settings\\Mr. Evil\\Desktop'
        u'\\netstumblerinstaller...')

    self._TestGetMessageStrings(
        event_object, expected_message, expected_message_short)

    event_object = storage_writer.events[2]

    self._TestGetSourceStrings(event_object, u'Recycle Bin', u'RECBIN')


if __name__ == '__main__':
  unittest.main()
