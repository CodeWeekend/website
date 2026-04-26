FROM hugomods/hugo:exts-0.140.0 AS builder
WORKDIR /src
COPY . .
ENV HUGO_ENV=production
RUN hugo --minify --gc

FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=builder /src/public /usr/share/caddy
EXPOSE 80
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
