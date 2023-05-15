#! /bin/bash

envsubst '${your_domain}' < /app/nginx.conf > /etc/nginx/sites-available/default