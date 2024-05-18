from unittest.mock import patch


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello Robot'}


@patch('app.config.settings.current_position', '(4, 3), "EAST"')
def test__get_current_position__initial_position(test_client):
    response = test_client.get('/current-position')
    assert response.status_code == 200
    assert response.json() == {'position': '(4, 3), EAST'}


@patch('app.config.settings.current_position', '(4, 2), "EAST"')
def test__get_current_position__after_executing_command(test_client):
    response = test_client.get('/execute-command/LFFLBLF')
    response = test_client.get('/current-position')
    assert response.status_code == 200
    assert response.json() == {'position': '(5, 3), SOUTH'}


@patch('app.config.settings.current_position', '(4, 2), "EAST"')
def test__execute_command(test_client):
    response = test_client.get('/execute-command/FLFFFRFLB')
    assert response.status_code == 200
    assert response.json() == {'position': '(6, 4), NORTH'}


def test__execute_command__bad_request(test_client):
    response = test_client.get('/execute-command/123')
    assert response.status_code == 400
    assert response.json() == {'detail': 'Bad request'}


@patch('app.config.settings.current_position', '(4, 2), "EAST"')
def test__execute_command__stopped(test_client):
    response = test_client.get('/execute-command/BLFFF')
    assert response.status_code == 200
    assert response.json() == {'position': '(3, 4), NORTH STOPPED'}
