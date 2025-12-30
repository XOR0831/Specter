from pathlib import Path
import tempfile

from scanner.utils.targets import expand_targets


def test_single_ip():
    assert expand_targets("127.0.0.1") == ["127.0.0.1"]


def test_cidr():
    assert expand_targets("192.168.1.0/30") == [
        "192.168.1.1",
        "192.168.1.2",
    ]


def test_file_targets():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("127.0.0.1\n")
        path = Path(f.name)

    assert expand_targets(str(path)) == ["127.0.0.1"]
