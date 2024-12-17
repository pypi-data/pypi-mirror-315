"""Tests for disk storage broker."""

import os
import pytz
import datetime
import time

import pytest

from . import tmp_dir_fixture  # NOQA
from . import tmp_uri_fixture  # NOQA
from . import TEST_SAMPLE_DATA


def test_initialise():

    from dtoolcore.storagebroker import DiskStorageBroker

    path = '/a/path'
    storagebroker = DiskStorageBroker(uri=path)  # NOQA


def test_create_structure(tmp_dir_fixture):  # NOQA

    from dtoolcore.storagebroker import DiskStorageBroker
    from dtoolcore.storagebroker import StorageBrokerOSError

    storagebroker = DiskStorageBroker(tmp_dir_fixture)

    with pytest.raises(StorageBrokerOSError):
        storagebroker.create_structure()

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')

    storagebroker = DiskStorageBroker(destination_path)

    assert not os.path.exists(destination_path)
    storagebroker.create_structure()
    assert os.path.isdir(destination_path)

    destination_path = os.path.join(tmp_dir_fixture, 'sub', 'my_proto_dataset')

    storagebroker = DiskStorageBroker(destination_path)

    with pytest.raises(OSError):
        storagebroker.create_structure()


def test_store_and_retrieve_readme(tmp_dir_fixture):  # NOQA

    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    storagebroker.put_readme('Hello world')
    assert storagebroker.get_readme_content() == 'Hello world'


def test_update_readme(tmp_dir_fixture):  # NOQA

    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    storagebroker.put_readme('Hello world')
    assert storagebroker.get_readme_content() == 'Hello world'

    assert len(storagebroker._list_historical_readme_keys()) == 0

    storagebroker.update_readme('Updated')
    assert storagebroker.get_readme_content() == 'Updated'

    assert len(storagebroker._list_historical_readme_keys()) == 1

    with open(storagebroker._list_historical_readme_keys()[0]) as fh:
        assert fh.read() == 'Hello world'

    time.sleep(0.1)

    storagebroker.update_readme('Updated again')
    assert storagebroker.get_readme_content() == 'Updated again'

    assert len(storagebroker._list_historical_readme_keys()) == 2


def test_store_and_retrieve_admin_metadata(tmp_dir_fixture):  # NOQA

    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    admin_metadata = {'hello': 'world'}
    storagebroker.put_admin_metadata(admin_metadata)

    storagebroker_2 = DiskStorageBroker(destination_path)
    retrieved_admin_metadata = storagebroker_2.get_admin_metadata()
    assert retrieved_admin_metadata == admin_metadata


def test_put_item(tmp_dir_fixture):  # NOQA

    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    input_file_path = os.path.join(TEST_SAMPLE_DATA, 'tiny.png')

    storagebroker.put_item(
        fpath=input_file_path,
        relpath='tiny.png'
    )

    handles = list(storagebroker.iter_item_handles())

    assert 'tiny.png' in handles


def test_store_and_retrieve_manifest(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    manifest = {'a': 'b', 'c': [1, 2, 3]}

    storagebroker.put_manifest(manifest)

    retrieved_manifest = storagebroker.get_manifest()

    assert retrieved_manifest == manifest

    # Test the formatting on disk.
#   expected = '{\n  "a": "b", \n  "c": [\n    1, \n    2, \n    3\n  ]\n}'
    expected_lines = [
        '{',
        '  "a": "b",',
        '  "c": [',
        '    1,',
        '    2,',
        '    3',
        '  ]',
        '}'
    ]

    with open(storagebroker.get_manifest_key()) as fh:
        for i, actual in enumerate(fh):
            actual = actual.rstrip()
            expected = expected_lines[i]
            assert actual == expected


def test_item_properties(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    input_file_path = os.path.join(TEST_SAMPLE_DATA, 'tiny.png')

    storagebroker.put_item(
        fpath=input_file_path,
        relpath='tiny.png'
    )

    handles = list(storagebroker.iter_item_handles())

    handle = handles[0]

    item_properties = storagebroker.item_properties(handle)

    # Check size_in_bytes property
    assert item_properties['size_in_bytes'] == 276

    # Check timestamp property
    assert 'utc_timestamp' in item_properties

    time_from_item = datetime.datetime.fromtimestamp(
        float(item_properties['utc_timestamp']),
        tz=pytz.UTC
    )

    time.sleep(0.1)   # Make tests more robust on Windows.
    time_delta = datetime.datetime.now(tz=pytz.UTC) - time_from_item

    assert time_delta.days == 0
    assert time_delta.seconds < 20

    # Check hash property
    from dtoolcore.filehasher import md5sum_hexdigest
    expected_hash = md5sum_hexdigest(input_file_path)

    assert item_properties['hash'] == expected_hash

    # Check relpath property
    assert item_properties['relpath'] == 'tiny.png'


def test_store_and_retrieve_item_metadata(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    handle = 'dummy'

    # Here we add two set of metadata with different keys
    storagebroker.add_item_metadata(
        handle=handle,
        key='foo',
        value='bar'
    )
    storagebroker.add_item_metadata(
        handle=handle,
        key='key',
        value={'subkey': 'subval',
               'morekey': 'moreval'}
    )

    # Test metadata retrieval (we get back both sets of metadata)
    metadata = storagebroker.get_item_metadata(handle)
    assert metadata == {
        'foo': 'bar',
        'key': {
            'subkey': 'subval',
            'morekey': 'moreval'
        }
    }


def test_store_and_retrieve_item_metadata(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    example_overlay = {
        'abcdef': 1,
        'ghijkl': 2
    }

    storagebroker.put_overlay(
        overlay_name="example",
        overlay=example_overlay
    )

    retrieved_overlay = storagebroker.get_overlay('example')

    assert example_overlay == retrieved_overlay


def test_post_freeze_hook(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    # The below should not raise an OSError because the .dtool/tmp_fragments
    # directory has not been created.
    storagebroker.post_freeze_hook()

    handle = 'dummy'
    storagebroker.add_item_metadata(handle, key='foo', value='bar')

    assert os.path.isdir(storagebroker._metadata_fragments_abspath)
    storagebroker.post_freeze_hook()
    assert not os.path.isdir(storagebroker._metadata_fragments_abspath)


def test_has_admin_metadata(tmp_dir_fixture):  # NOQA

    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    assert not storagebroker.has_admin_metadata()

    storagebroker.create_structure()
    assert not storagebroker.has_admin_metadata()

    admin_metadata = {'hello': 'world'}
    storagebroker.put_admin_metadata(admin_metadata)
    assert storagebroker.has_admin_metadata()


def test_list_dataset_uris(tmp_uri_fixture):  # NOQA

    import dtoolcore
    from dtoolcore.storagebroker import DiskStorageBroker

    assert [] == DiskStorageBroker.list_dataset_uris(
        base_uri=tmp_uri_fixture,
        config_path=None
    )

    # Create two datasets to be copied.
    expected_uris = []
    for name in ["test_ds_1", "test_ds_2"]:
        admin_metadata = dtoolcore.generate_admin_metadata(name)
        proto_dataset = dtoolcore.generate_proto_dataset(
            admin_metadata=admin_metadata,
            base_uri=tmp_uri_fixture,
            )
        proto_dataset.create()
        expected_uris.append(proto_dataset.uri)

    actual_uris = DiskStorageBroker.list_dataset_uris(
        base_uri=tmp_uri_fixture,
        config_path=None
    )

    assert set(expected_uris) == set(actual_uris)


def test_pre_freeze_hook(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    # Add a data file.
    data_fpath = os.path.join(storagebroker._data_abspath, "sample.txt")
    with open(data_fpath, "w") as fh:
        fh.write("some sample data")

    # The below should not raise an DiskStorageBrokerValidationError
    # because the structure is correct.
    storagebroker.pre_freeze_hook()

    # Now we add a rogue file.
    rogue_fpath = os.path.join(destination_path, "rogue.txt")
    with open(rogue_fpath, "w") as fh:
        fh.write("I should not be here")

    from dtoolcore.storagebroker import DiskStorageBrokerValidationWarning
    with pytest.raises(DiskStorageBrokerValidationWarning):
        storagebroker.pre_freeze_hook()


def test_unix_relpaths_from_iter_item_handles(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    # Add a data file.
    data_subdir = os.path.join(storagebroker._data_abspath, "level")
    os.mkdir(data_subdir)
    data_fpath = os.path.join(data_subdir, "sample.txt")
    with open(data_fpath, "w") as fh:
        fh.write("some sample data")

    handles = [h for h in storagebroker.iter_item_handles()]
    assert len(handles) == 1
    assert handles[0] == "level/sample.txt"


def test_put_get_annotation(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')
    storagebroker = DiskStorageBroker(destination_path)

    storagebroker.create_structure()

    # Test list annotation names.
    assert storagebroker.list_annotation_names() == []

    # Test various types of values.
    storagebroker.put_annotation("project", "value")
    assert storagebroker.get_annotation("project") == "value"

    storagebroker.put_annotation("project", 1)
    assert storagebroker.get_annotation("project") == 1
    assert type(storagebroker.get_annotation("project")) is int

    storagebroker.put_annotation("project", True)
    assert storagebroker.get_annotation("project") is True

    storagebroker.put_annotation("project", [1, 2, 3])
    assert storagebroker.get_annotation("project") == [1, 2, 3]

    storagebroker.put_annotation("project", {"a": 1})
    assert storagebroker.get_annotation("project") == {"a": 1}

    # Test list annotation names.
    assert storagebroker.list_annotation_names() == ["project"]


def test_put_text_creates_missing_subdirectories(tmp_dir_fixture):  # NOQA
    from dtoolcore.storagebroker import DiskStorageBroker

    destination_path = os.path.join(tmp_dir_fixture, 'my_proto_dataset')

    storagebroker = DiskStorageBroker(destination_path)

    assert not os.path.exists(destination_path)
    storagebroker.create_structure()
    assert os.path.isdir(destination_path)

    assert os.path.isdir(storagebroker._annotations_abspath)
    os.rmdir(storagebroker._annotations_abspath)
    assert not os.path.isdir(storagebroker._annotations_abspath)

    annotation_key = os.path.join(
        storagebroker._annotations_abspath,
        "a.json"
    )
    storagebroker.put_text(annotation_key, "{}")
    assert os.path.isdir(storagebroker._annotations_abspath)

    assert os.path.isfile(annotation_key)
    assert not os.path.isdir(annotation_key)
