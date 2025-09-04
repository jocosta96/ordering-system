#!/bin/bash

# Script to set up AWS SSM Parameter Store parameters for the FastFood application
# Usage: ./setup-ssm-parameters.sh [--dry-run] [--region REGION]

set -e

# Default values
REGION="us-east-1"
DRY_RUN=false
PREFIX="/fastfood/database/"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}$message${NC}"
}

# Function to print usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Setup AWS SSM Parameter Store parameters for FastFood application"
    echo ""
    echo "Options:"
    echo "  --dry-run           Show what would be created without actually creating"
    echo "  --region REGION     AWS region (default: us-east-1)"
    echo "  --prefix PREFIX     SSM parameter prefix (default: /fastfood/database/)"
    echo "  --help             Show this help message"
    echo ""
    echo "Environment Variables (required):"
    echo "  DB_HOST            Database hostname"
    echo "  DB_PORT            Database port (default: 5432)"
    echo "  DB_NAME            Database name (default: fastfood)"
    echo "  DB_USERNAME        Database username (default: postgres)"
    echo "  DB_PASSWORD        Database password (required)"
    echo "  DB_DRIVER          Database driver (default: postgresql)"
    echo ""
    echo "Example:"
    echo "  export DB_HOST=mydb.region.rds.amazonaws.com"
    echo "  export DB_PASSWORD=secure-password"
    echo "  $0 --region us-west-2"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --prefix)
            PREFIX="$2"
            shift 2
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Check if AWS CLI is available
if ! command -v aws &> /dev/null; then
    print_status $RED "Error: AWS CLI is not installed or not in PATH"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    print_status $RED "Error: AWS credentials not configured or invalid"
    exit 1
fi

print_status $BLUE "FastFood SSM Parameter Setup"
print_status $BLUE "============================"
echo ""

# Get configuration values from environment or use defaults
DB_HOST=${DB_HOST:-""}
DB_PORT=${DB_PORT:-"5432"}
DB_NAME=${DB_NAME:-"fastfood"}
DB_USERNAME=${DB_USERNAME:-"postgres"}
DB_PASSWORD=${DB_PASSWORD:-""}
DB_DRIVER=${DB_DRIVER:-"postgresql"}

# Validate required parameters
if [[ -z "$DB_HOST" ]]; then
    print_status $RED "Error: DB_HOST environment variable is required"
    echo "Set it with: export DB_HOST=your-database-host"
    exit 1
fi

if [[ -z "$DB_PASSWORD" ]]; then
    print_status $RED "Error: DB_PASSWORD environment variable is required"
    echo "Set it with: export DB_PASSWORD=your-secure-password"
    exit 1
fi

print_status $GREEN "Configuration:"
echo "  Region: $REGION"
echo "  Prefix: $PREFIX"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo "  Database: $DB_NAME"
echo "  Username: $DB_USERNAME"
echo "  Password: [HIDDEN]"
echo "  Driver: $DB_DRIVER"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    print_status $YELLOW "DRY RUN MODE - No parameters will be created"
    echo ""
fi

# Array of parameters to create
declare -a PARAMETERS=(
    "${PREFIX}host|$DB_HOST|String|Database hostname"
    "${PREFIX}port|$DB_PORT|String|Database port"
    "${PREFIX}database|$DB_NAME|String|Database name"
    "${PREFIX}username|$DB_USERNAME|String|Database username"
    "${PREFIX}password|$DB_PASSWORD|SecureString|Database password"
    "${PREFIX}driver|$DB_DRIVER|String|Database driver"
)

print_status $GREEN "Creating SSM Parameters..."
echo ""

# Function to create or update parameter
create_parameter() {
    local param_name=$1
    local param_value=$2
    local param_type=$3
    local param_description=$4
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_status $BLUE "Would create: $param_name (Type: $param_type)"
        return
    fi
    
    # Check if parameter already exists
    if aws ssm describe-parameters --region "$REGION" --parameter-filters "Key=Name,Values=$param_name" --query 'Parameters[0].Name' --output text 2>/dev/null | grep -q "$param_name"; then
        print_status $YELLOW "Updating existing parameter: $param_name"
        aws ssm put-parameter \
            --region "$REGION" \
            --name "$param_name" \
            --value "$param_value" \
            --type "$param_type" \
            --description "$param_description" \
            --overwrite \
            --no-cli-pager
    else
        print_status $GREEN "Creating new parameter: $param_name"
        aws ssm put-parameter \
            --region "$REGION" \
            --name "$param_name" \
            --value "$param_value" \
            --type "$param_type" \
            --description "$param_description" \
            --no-cli-pager
    fi
}

# Create each parameter
for param in "${PARAMETERS[@]}"; do
    IFS='|' read -r name value type description <<< "$param"
    create_parameter "$name" "$value" "$type" "$description"
done

echo ""
if [[ "$DRY_RUN" == "true" ]]; then
    print_status $BLUE "Dry run completed. No parameters were created."
else
    print_status $GREEN "SSM parameters created successfully!"
fi

echo ""
print_status $BLUE "Next Steps:"
echo "1. Update the IAM role ARN in dev/k8s/sa_app.yaml"
echo "2. Deploy the updated Kubernetes manifests:"
echo "   kubectl apply -f dev/k8s/sa_app.yaml"
echo "   kubectl apply -f dev/k8s/cfm_database.yaml"
echo "   kubectl apply -f dev/k8s/dpm_app.yaml"
echo "3. Verify configuration:"
echo "   curl http://your-app/health/config"

echo ""
print_status $YELLOW "Security Note:"
echo "The database password is stored as a SecureString and encrypted with AWS KMS."
echo "Make sure your IAM role has the necessary permissions to decrypt it."

echo ""
print_status $GREEN "Setup completed!"
