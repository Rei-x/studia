echo "Launching docker compose"
docker compose up -d
echo "Waiting for services to start"
sleep 10
echo "Scaling up notification-service to 3 instances"
docker compose scale notification-service=3
echo "Scaled up notification-service to 3 instances"
sleep 10
echo "Scaling down notification-service to 2 instances"
docker compose scale notification-service=2
sleep 10
echo "Scaled down notification-service to 2 instances"
docker compose down
