from unittest.mock import patch, MagicMock
from scanner.fingerprint.banners import grab_banner


@patch("socket.socket")
def test_tcp_banner_grab(mock_socket):
    mock = MagicMock()
    mock.recv.return_value = b"SSH-2.0-Test"
    mock_socket.return_value.__enter__.return_value = mock

    banner = grab_banner("127.0.0.1", 22, "tcp")
    assert "SSH-2.0" in banner
