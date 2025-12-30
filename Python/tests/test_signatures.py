from scanner.fingerprint.signatures import match_service


def test_ssh():
    svc = match_service("SSH-2.0-OpenSSH_8.9p1 Ubuntu")
    assert svc.name == "ssh"
    assert svc.version == "8.9p1"


def test_nginx():
    svc = match_service("Server: nginx/1.24.0")
    assert svc.name == "nginx"
    assert svc.version == "1.24.0"


def test_unknown():
    assert match_service("blah blah") is None
