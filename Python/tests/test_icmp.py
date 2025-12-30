from unittest.mock import patch, MagicMock

from scanner.protocols.icmp import icmp_ping


@patch("scanner.protocols.icmp.IP")
@patch("scanner.protocols.icmp.ICMP")
@patch("scanner.protocols.icmp.sr1")
def test_icmp_success(mock_sr1, mock_icmp, mock_ip):
    mock_sr1.return_value = object()

    assert icmp_ping("8.8.8.8") is True

def test_icmp_without_scapy_returns_false():
    # No patching → simulates missing scapy
    assert icmp_ping("8.8.8.8") is False