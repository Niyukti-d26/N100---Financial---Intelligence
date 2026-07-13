from src.peer_engine.engine import PeerEngine


def test_no_peer_group():

    engine = PeerEngine()

    result = engine.get_company_peer_data("ABB")

    assert result == "No peer group assigned"