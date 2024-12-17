"""Test the compare module."""

import os

from . import uri_to_path
from . import tmp_uri_fixture  # NOQA


def create_test_files(uri):
    fpaths = dict()
    for word in ["he", "she", "cat"]:
        fpath = os.path.join(uri_to_path(uri), word + ".txt")
        with open(fpath, "w") as fh:
            fh.write(word)
        fpaths[word] = fpath
    return fpaths


def test_diff_identifiers(tmp_uri_fixture):  # NOQA

    from dtoolcore import (
        DataSet,
        generate_admin_metadata,
        generate_proto_dataset,
    )
    from dtoolcore.utils import generate_identifier
    from dtoolcore.compare import diff_identifiers

    fpaths = create_test_files(tmp_uri_fixture)

    proto_ds_a = generate_proto_dataset(
        admin_metadata=generate_admin_metadata("test_compare_1"),
        base_uri=tmp_uri_fixture
    )
    proto_ds_a.create()
    proto_ds_a.put_item(fpaths["cat"], "a.txt")
    proto_ds_a.freeze()

    proto_ds_b = generate_proto_dataset(
        admin_metadata=generate_admin_metadata("test_compare_2"),
        base_uri=tmp_uri_fixture
    )
    proto_ds_b.create()
    proto_ds_b.put_item(fpaths["cat"], "b.txt")
    proto_ds_b.freeze()

    ds_a = DataSet.from_uri(proto_ds_a.uri)
    ds_b = DataSet.from_uri(proto_ds_b.uri)

    assert diff_identifiers(ds_a, ds_a) == []

    expected = [
        (generate_identifier("a.txt"), True, False),
        (generate_identifier("b.txt"), False, True)
    ]
    assert diff_identifiers(ds_a, ds_b) == expected


def test_diff_sizes(tmp_uri_fixture):  # NOQA

    from dtoolcore import (
        DataSet,
        generate_admin_metadata,
        generate_proto_dataset,
    )
    from dtoolcore.utils import generate_identifier
    from dtoolcore.compare import diff_sizes

    fpaths = create_test_files(tmp_uri_fixture)

    proto_ds_a = generate_proto_dataset(
        admin_metadata=generate_admin_metadata("test_compare_1"),
        base_uri=tmp_uri_fixture
    )
    proto_ds_a.create()
    proto_ds_a.put_item(fpaths["he"], "file.txt")
    proto_ds_a.freeze()

    proto_ds_b = generate_proto_dataset(
        admin_metadata=generate_admin_metadata("test_compare_2"),
        base_uri=tmp_uri_fixture
    )
    proto_ds_b.create()
    proto_ds_b.put_item(fpaths["she"], "file.txt")
    proto_ds_b.freeze()

    ds_a = DataSet.from_uri(proto_ds_a.uri)
    ds_b = DataSet.from_uri(proto_ds_b.uri)

    assert diff_sizes(ds_a, ds_a) == []

    expected = [
        (generate_identifier("file.txt"), 2, 3),
    ]
    assert diff_sizes(ds_a, ds_b) == expected


def test_diff_content(tmp_uri_fixture):  # NOQA

    from dtoolcore import (
        DataSet,
        generate_admin_metadata,
        generate_proto_dataset,
    )
    from dtoolcore.utils import generate_identifier
    from dtoolcore.compare import diff_content
    from dtoolcore.storagebroker import DiskStorageBroker

    fpaths = create_test_files(tmp_uri_fixture)

    proto_ds_a = generate_proto_dataset(
        admin_metadata=generate_admin_metadata("test_compare_1"),
        base_uri=tmp_uri_fixture
    )
    proto_ds_a.create()
    proto_ds_a.put_item(fpaths["cat"], "file.txt")
    proto_ds_a.freeze()

    proto_ds_b = generate_proto_dataset(
        admin_metadata=generate_admin_metadata("test_compare_2"),
        base_uri=tmp_uri_fixture
    )
    proto_ds_b.create()
    proto_ds_b.put_item(fpaths["she"], "file.txt")
    proto_ds_b.freeze()

    ds_a = DataSet.from_uri(proto_ds_a.uri)
    ds_b = DataSet.from_uri(proto_ds_b.uri)

    assert diff_content(ds_a, ds_a) == []

    identifier = generate_identifier("file.txt")
    expected = [(
        generate_identifier("file.txt"),
        DiskStorageBroker.hasher(ds_a.item_content_abspath(identifier)),
        DiskStorageBroker.hasher(ds_b.item_content_abspath(identifier))
    )]
    assert diff_content(ds_a, ds_b) == expected
