#!/bin/bash

echo "Waiting for data_injestion container to complete its work..."
while ! curl -s http://data_injestion >/dev/null; do
    sleep 1
done
echo "data_injestion container is ready!"

exec "$@"