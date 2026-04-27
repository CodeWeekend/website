# =============================================================================
# CodeWeekend — Static site Dockerfile
# Multi-stage: Hugo build → Caddy serve
# Final image is ~25MB; serves static HTML with HTTP/2, gzip, brotli, auto-SSL.
# =============================================================================

# ---------- Build stage ----------
FROM hugomods/hugo:exts-0.140.0 AS builder

WORKDIR /src

# Copy everything (gitignore handles excludes)
COPY . .

# Build the site. --minify shrinks output, --gc cleans up cache.
# HUGO_ENV=production turns on all production optimizations.
ENV HUGO_ENV=production
RUN hugo --minify --gc

# ---------- Serve stage ----------
FROM caddy:2-alpine

# Caddy config (gzip, zstd, security headers)
COPY Caddyfile /etc/caddy/Caddyfile

# Static site output from the build stage
COPY --from=builder /src/public /usr/share/caddy

EXPOSE 80
EXPOSE 443

# Caddy will pick up the Caddyfile from /etc/caddy automatically
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
