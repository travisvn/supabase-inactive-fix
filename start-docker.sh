#!/bin/sh

if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install Docker to run this script."
    exit
fi

# Build the Docker image
docker build -t supabase-inactive-fix .

# Run the container
docker run -d --name supabase-inactive-fix supabase-inactive-fix

# Print instructions
echo "Docker container 'supabase-inactive-fix' is now running!"
echo "The Python script will run every day at midnight (00:00)"
echo ""
echo "To view logs: docker logs supabase-inactive-fix"
echo "To stop the container: docker stop supabase-inactive-fix"
echo "To restart the container: docker start supabase-inactive-fix"
