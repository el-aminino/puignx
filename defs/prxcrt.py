#import required libraries
import jinja2
import subprocess

#template for proxy in nginx
nginx_template = """
server {
    listen {{ port }};
    server_name {{ server_name }};

    location / {
        proxy_pass http://{{ upstream }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    access_log /var/log/nginx/{{ server_name }}.access.log;
    error_log /var/log/nginx/{{ server_name }}.error.log;
}
"""

# Render the template with your specific configuration
config_data = {
    'port': 80,
    'server_name': 'example.com',
    'upstream': 'localhost:8000',  # Replace with your backend server address
}

template = jinja2.Template(nginx_template)
nginx_config = template.render(config_data)

# Save the generated configuration to a file
config_path = '/etc/nginx/sites-available/example'
with open(config_path, 'w') as f:
    f.write(nginx_config)

# Create a symbolic link to enable the site
subprocess.run(['ln', '-s', config_path, '/etc/nginx/sites-enabled/'])

# Reload Nginx to apply the changes
subprocess.run(['systemctl', 'reload', 'nginx'])
