def pytest_configure(config):
    config.addinivalue_line("markers", "current: As current ones")
    config.addinivalue_line("markers", "learning: As learning exercises")
    config.addinivalue_line("markers", "api: As using the Notion API")
    config.addinivalue_line("markers", "slow: As slow ones")
    config.addinivalue_line("markers", "minimum: 最低限やっておきたいテスト")
