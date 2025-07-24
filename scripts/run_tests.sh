#!/bin/bash

# Test runner script for the ordering system
# This script runs all tests with proper configuration and reporting

set -e

echo "🧪 Running Ordering System Tests"
echo "================================="

# Set test environment variables
export LOG_LEVEL=DEBUG
export ANONYMOUS_EMAIL=anonymous@test.local
export API_PREFIX=/test/api
export ALLOWED_ORIGINS=*

# Install test dependencies if not already installed
if [ ! -f "requirements-test.txt" ]; then
    echo "❌ Test requirements file not found"
    exit 1
fi

echo "📦 Installing test dependencies..."
pip install -r requirements-test.txt

# Run linting and code quality checks
echo "🔍 Running code quality checks..."
echo "Running black..."
black --check src/ tests/
echo "Running flake8..."
flake8 src/ tests/
echo "Running isort..."
isort --check-only src/ tests/
echo "Running mypy..."
mypy src/

# Run unit tests
echo "🧪 Running unit tests..."
pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov/unit

# Run integration tests
echo "🔗 Running integration tests..."
pytest tests/integration/ -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov/integration

# Run all tests with coverage report
echo "📊 Generating comprehensive coverage report..."
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml

# Show coverage summary
echo "📈 Coverage Summary:"
coverage report --show-missing

echo "✅ All tests completed successfully!"
echo "📁 Coverage reports available in:"
echo "   - HTML: htmlcov/index.html"
echo "   - XML: coverage.xml" 