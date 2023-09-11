# Define a class to manage the Nginx installation and web server setup
class web_server {
  package { 'nginx':
    ensure => 'installed',
  }

  service { 'nginx':
    ensure  => 'running',
    enable  => true,
    require => Package['nginx'],
  }
}

# Create the necessary directories and set ownership
file { ['/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<!DOCTYPE html>
              <html>
              <head>
              <title>Deploying web static</title>
              </head>
              <body>
              <h1>Deploying to two servers.</h1>
              </body>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  notify => Service['nginx'],
}

# Define the Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => "server {
    listen 80 default_server;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}",
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  require => Class['web_server'],
}

# Test Nginx configs and restart Nginx
exec { 'test_nginx_configs':
  command     => 'nginx -t',
  refreshonly => true,
  subscribe   => File['/etc/nginx/sites-available/default'],
  notify      => Service['nginx'],
}

# Ensure that the Nginx service is running
Service['nginx'] ~> Exec['test_nginx_configs']

