from unittest.mock import patch
from scanner.protocols.udp import udp_scan


@patch("socket.socket")
def test_udp_no_response(mock_socket):
    sock = mock_socket.return_value.__enter__.return_value
    sock.recvfrom.side_effect = TimeoutError

    assert udp_scan("127.0.0.1", 9999) == "open|filtered"
