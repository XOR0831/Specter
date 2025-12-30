from unittest.mock import patch
from scanner.protocols.tcp import tcp_connect_scan


@patch("socket.socket")
def test_tcp_open(mock_socket):
    sock = mock_socket.return_value.__enter__.return_value
    sock.connect_ex.return_value = 0

    assert tcp_connect_scan("127.0.0.1", 22) == "open"
