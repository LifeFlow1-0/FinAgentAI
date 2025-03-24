"""
Tests for the configuration module.
"""
import os
import unittest
from pathlib import Path

from app.config import Settings, Environment


class TestConfigSettings(unittest.TestCase):
    """Test the application configuration settings."""
    
    def setUp(self):
        # Save original environment variables
        self.original_env = os.environ.copy()
        
        # Clear any environment variables that might affect tests
        if "ENV_FILE" in os.environ:
            del os.environ["ENV_FILE"]
        if "ENVIRONMENT" in os.environ:
            del os.environ["ENVIRONMENT"]
        if "DATABASE_PATH" in os.environ:
            del os.environ["DATABASE_PATH"]

    def tearDown(self):
        # Restore original environment variables
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_default_settings(self):
        """Test that default settings are loaded correctly."""
        settings = Settings()
        self.assertEqual(settings.APP_NAME, "LifeFlow")
        self.assertTrue(settings.DEBUG)
        self.assertEqual(settings.API_V1_PREFIX, "/api/v1")
        
        # Check that the SQLite database path is set correctly for development
        self.assertTrue(settings.DATABASE_PATH.endswith("lifeflow.db"))
        self.assertTrue(Path(settings.DATABASE_PATH).parent.absolute() == 
                       Path(__file__).parent.parent.absolute())
    
    def test_environment_specific_settings(self):
        """Test that environment-specific settings work."""
        # Test gamma environment
        os.environ["ENVIRONMENT"] = "gamma"
        settings = Settings()
        self.assertEqual(settings.ENVIRONMENT, Environment.GAMMA)
        
        # Only check that the gamma database path includes the correct environment name
        # and is set to use the data directory
        self.assertTrue("gamma" in settings.DATABASE_PATH.lower())
        self.assertTrue("/app/data" in settings.DATABASE_PATH)
    
    def test_database_path_override(self):
        """Test that DATABASE_PATH can be overridden."""
        test_db_path = "/tmp/test_db.sqlite"
        os.environ["DATABASE_PATH"] = test_db_path
        settings = Settings()
        self.assertEqual(settings.DATABASE_PATH, test_db_path)
        
        # Reset environment
        os.environ.pop("DATABASE_PATH")
    
    def test_env_file_override(self):
        """Test that ENV_FILE environment variable is respected."""
        os.environ["ENV_FILE"] = "custom.env"
        settings = Settings()
        # We just want to verify that the file is recognized, not that it loads
        # since the file might not exist in the test environment
        self.assertEqual(settings.model_config["env_file"], "custom.env")


if __name__ == "__main__":
    unittest.main() 