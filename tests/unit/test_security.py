"""
Unit tests for security module.

Tests cover:
- HTTP authentication
- Credential validation
- User authentication
- Error handling
"""

import pytest
import os
from unittest.mock import Mock
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials

from src.security.http_auth import check_credentials, get_current_user, raise_not_authorized


class TestSecurityAuth:
    """Test cases for security authentication"""

    @pytest.fixture
    def mock_credentials(self):
        """Mock HTTPBasicCredentials"""
        credentials = Mock(spec=HTTPBasicCredentials)
        return credentials

    @pytest.fixture
    def setup_env_vars(self):
        """Setup environment variables for testing"""
        original_user = os.environ.get('API_USER')
        original_pwd = os.environ.get('API_PWD')
        
        # Set test environment variables
        os.environ['API_USER'] = 'testuser'
        os.environ['API_PWD'] = 'testpassword'
        
        yield
        
        # Restore original environment variables
        if original_user:
            os.environ['API_USER'] = original_user
        else:
            os.environ.pop('API_USER', None)
            
        if original_pwd:
            os.environ['API_PWD'] = original_pwd
        else:
            os.environ.pop('API_PWD', None)

    def test_raise_not_authorized(self):
        """Test that raise_not_authorized raises correct HTTPException"""
        with pytest.raises(HTTPException) as exc_info:
            raise_not_authorized()
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password"
        assert "WWW-Authenticate" in exc_info.value.headers
        assert exc_info.value.headers["WWW-Authenticate"] == "Basic"

    def test_check_credentials_success(self, mock_credentials, setup_env_vars):
        """Test successful credential validation"""
        mock_credentials.username = "testuser"
        mock_credentials.password = "testpassword"
        
        result = check_credentials(mock_credentials)
        
        assert result == "testuser"

    def test_check_credentials_wrong_username(self, mock_credentials, setup_env_vars):
        """Test credential validation with wrong username"""
        mock_credentials.username = "wronguser"
        mock_credentials.password = "testpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            check_credentials(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password"

    def test_check_credentials_wrong_password(self, mock_credentials, setup_env_vars):
        """Test credential validation with wrong password"""
        mock_credentials.username = "testuser"
        mock_credentials.password = "wrongpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            check_credentials(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password"

    def test_check_credentials_both_wrong(self, mock_credentials, setup_env_vars):
        """Test credential validation with both username and password wrong"""
        mock_credentials.username = "wronguser"
        mock_credentials.password = "wrongpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            check_credentials(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password"

    def test_check_credentials_empty_username(self, mock_credentials, setup_env_vars):
        """Test credential validation with empty username"""
        mock_credentials.username = ""
        mock_credentials.password = "testpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            check_credentials(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_check_credentials_empty_password(self, mock_credentials, setup_env_vars):
        """Test credential validation with empty password"""
        mock_credentials.username = "testuser"
        mock_credentials.password = ""
        
        with pytest.raises(HTTPException) as exc_info:
            check_credentials(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_success(self, mock_credentials, setup_env_vars):
        """Test successful user retrieval"""
        mock_credentials.username = "testuser"
        mock_credentials.password = "testpassword"
        
        result = get_current_user(mock_credentials)
        
        assert result == "testuser"

    def test_get_current_user_wrong_username(self, mock_credentials, setup_env_vars):
        """Test user retrieval with wrong username"""
        mock_credentials.username = "wronguser"
        mock_credentials.password = "testpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password"

    def test_get_current_user_wrong_password(self, mock_credentials, setup_env_vars):
        """Test user retrieval with wrong password"""
        mock_credentials.username = "testuser"
        mock_credentials.password = "wrongpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password"

    def test_get_current_user_both_wrong(self, mock_credentials, setup_env_vars):
        """Test user retrieval with both username and password wrong"""
        mock_credentials.username = "wronguser"
        mock_credentials.password = "wrongpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Incorrect username or password"

        def test_credentials_with_special_characters(self, mock_credentials, setup_env_vars):
            """Test credential validation with special characters"""
            # Set environment variables with special characters
            os.environ['API_USER'] = 'user@domain.com'
            os.environ['API_PWD'] = 'pass@word123!'

            mock_credentials.username = "user@domain.com"
            mock_credentials.password = "pass@word123!"

            result = check_credentials(mock_credentials)

            assert result == "user@domain.com"

        def test_credentials_with_unicode(self, mock_credentials, setup_env_vars):
            """Test credential validation with unicode characters"""
            # Set environment variables with unicode characters
            os.environ['API_USER'] = 'usér'
            os.environ['API_PWD'] = 'pässwörd'

            mock_credentials.username = "usér"
            mock_credentials.password = "pässwörd"

            result = check_credentials(mock_credentials)

            assert result == "usér"

    def test_credentials_case_sensitive(self, mock_credentials, setup_env_vars):
        """Test that credential validation is case sensitive"""
        mock_credentials.username = "TestUser"  # Different case
        mock_credentials.password = "testpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            check_credentials(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_credentials_with_whitespace(self, mock_credentials, setup_env_vars):
        """Test credential validation with whitespace"""
        mock_credentials.username = " testuser "  # With whitespace
        mock_credentials.password = "testpassword"
        
        with pytest.raises(HTTPException) as exc_info:
            check_credentials(mock_credentials)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_returns_username(self, mock_credentials, setup_env_vars):
        """Test that get_current_user returns the username"""
        mock_credentials.username = "testuser"
        mock_credentials.password = "testpassword"
        
        result = get_current_user(mock_credentials)
        
        assert result == "testuser"
        assert isinstance(result, str)

    def test_environment_variables_not_set(self, mock_credentials):
        """Test behavior when environment variables are not set"""
        # Remove environment variables
        os.environ.pop('API_USER', None)
        os.environ.pop('API_PWD', None)
        
        mock_credentials.username = "testuser"
        mock_credentials.password = "testpassword"
        
        with pytest.raises(KeyError):
            check_credentials(mock_credentials)

        def test_credentials_encoding_handling(self, mock_credentials, setup_env_vars):
            """Test that credential encoding is handled correctly"""
            # Test with credentials that might have encoding issues
            mock_credentials.username = "testuser"
            mock_credentials.password = "testpassword"

            # This should not raise any encoding errors
            result = check_credentials(mock_credentials)

            assert result == "testuser"

        def test_multiple_credential_checks(self, mock_credentials, setup_env_vars):
            """Test multiple credential checks in sequence"""
            mock_credentials.username = "testuser"
            mock_credentials.password = "testpassword"

            # First check
            result1 = check_credentials(mock_credentials)
            assert result1 == "testuser"
            
            # Second check
            result2 = check_credentials(mock_credentials)
            assert result2 is True
            
            # Third check
            result3 = get_current_user(mock_credentials)
            assert result3 == "testuser"

        def test_credentials_with_numbers(self, mock_credentials, setup_env_vars):
            """Test credential validation with numeric values"""
            # Set environment variables with numbers
            os.environ['API_USER'] = 'user123'
            os.environ['API_PWD'] = 'pass456'

            mock_credentials.username = "user123"
            mock_credentials.password = "pass456"

            result = check_credentials(mock_credentials)

            assert result == "user123"

        def test_credentials_with_mixed_content(self, mock_credentials, setup_env_vars):
            """Test credential validation with mixed content"""
            # Set environment variables with mixed content
            os.environ['API_USER'] = 'user@123'
            os.environ['API_PWD'] = 'Pass@word!456'

            mock_credentials.username = "user@123"
            mock_credentials.password = "Pass@word!456"

            result = check_credentials(mock_credentials)

            assert result == "user@123" 