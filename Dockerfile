# vllm base image
FROM vllm/vllm-openai:latest

# Update system and install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    libssl-dev \
    libpcre3-dev \
    zlib1g-dev \
    curl \
    gnupg \
    libxslt1-dev \
    libgd-dev \
    libgeoip-dev \
    lua5.1 \
    liblua5.1-dev \
    wget \
    unzip \
    nginx

# Install OpenResty
RUN wget -O - https://openresty.org/package/pubkey.gpg | apt-key add - && \
    echo "deb http://openresty.org/package/ubuntu focal main" > /etc/apt/sources.list.d/openresty.list && \
    apt-get update && \
    apt-get install -y openresty

# Install LuaRocks from source
RUN wget https://luarocks.org/releases/luarocks-3.9.2.tar.gz && \
    tar zxpf luarocks-3.9.2.tar.gz && \
    cd luarocks-3.9.2 && \
    ./configure --prefix=/usr \
                --with-lua-include=/usr/local/openresty/luajit/include/luajit-2.1 \
                --with-lua=/usr/local/openresty/luajit && \
    make && \
    make install && \
    cd .. && \
    rm -rf luarocks-3.9.2*

# Set up LuaRocks paths
ENV LUA_PATH="/usr/local/openresty/site/lualib/?.lua;/usr/local/openresty/site/lualib/?/init.lua;/usr/local/openresty/lualib/?.lua;;"
ENV LUA_CPATH="/usr/local/openresty/site/lualib/?.so;/usr/local/openresty/lualib/?.so;;"
ENV PATH="/usr/local/openresty/bin:/usr/local/openresty/nginx/sbin:$PATH"

# Install the required Lua modules
RUN luarocks install lua-resty-http

# Create directory for Nginx configuration
RUN mkdir -p /etc/nginx/conf.d

# Copy Nginx configuration
COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf

# Create required directories
RUN mkdir -p /var/log/nginx && \
    mkdir -p /var/cache/nginx && \
    mkdir -p /var/run

# Set proper permissions (using chmod instead of chown)
RUN chmod -R 755 /var/log/nginx && \
    chmod -R 755 /var/cache/nginx && \
    chmod -R 755 /var/run && \
    chmod -R 755 /etc/nginx/conf.d

# Expose ports
EXPOSE 80

workdir /usr/src
COPY entrypoint.sh /usr/src/
RUN chmod +x /usr/src/entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]
