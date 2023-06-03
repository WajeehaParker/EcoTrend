#!/bin/bash

# Wait for the data_injestion container to be ready
echo "Waiting for data_injestion container to complete its work..."
while ! curl -s http://data_injestion >/dev/null; do
    sleep 1
done
echo "data_injestion container is ready!"

# Start the main process
exec "$@"