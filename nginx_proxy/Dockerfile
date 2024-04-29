# Dockerfile for Nginx
FROM nginxinc/nginx-unprivileged:1-alpine

# Copy the Nginx configuration file
COPY ./default.conf.tpl /etc/nginx/conf.d/default.conf

USER root

RUN mkdir -p /vol/web && \
    chmod 755 /vol/web && \
    chown -R nginx:nginx /vol/web /etc/nginx/conf.d/default.conf
    
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nginx

CMD ["/entrypoint.sh"]
