from beachbot_config import config, logger
from beachbot_config.config import setup_logger


def test_beachbot_config():
    assert config.BEACHBOT_HOME is not None
    assert config.BEACHBOT_CACHE is not None
    assert config.BEACHBOT_CONFIG is not None
    assert config.BEACHBOT_LOGS is not None
    assert config.BEACHBOT_MODELS is not None
    assert config.BEACHBOT_DATASETS is not None
    assert logger is not None


def test_missing_BEACHBOT_LOGS():
    # Temporarily move BEACHBOT_LOGS to a non-existent directory
    backup_BEACHBOT_LOGS = config.BEACHBOT_LOGS
    config.BEACHBOT_LOGS = config.BEACHBOT_LOGS / "tmptest"
    try:
        new_logger = setup_logger(config)
        assert new_logger is not None
    finally:
        # Remove temp log file
        (config.BEACHBOT_LOGS / "beachbot.log").unlink()
        config.BEACHBOT_LOGS.rmdir()
        # Restore BEACHBOT_LOGS
        config.BEACHBOT_LOGS = backup_BEACHBOT_LOGS
