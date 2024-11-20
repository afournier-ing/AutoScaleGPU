#!/bin/bash

# Check if the .secret file exists
if [ -f ".secret" ]; then
    # Export the AWS environment variables
    export $(grep -v '^#' .secret | xargs)
else
    echo "Error: .secret file not found. Exiting."
    exit 1
fi

# Execute the given command
exec "$@"

