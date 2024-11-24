# Currency Exchange Rate Application

This project is a simple currency exchange rate application built using **Flask**. The application allows users to register, log in, and convert currency using real-time exchange rate data from a public API. The application is deployed on two servers with a load balancer to ensure high availability and balanced traffic.

## Features
- **User Registration and Login:** Secure authentication using hashed passwords.
- **Currency Conversion:** Users can convert amounts between different currencies using real-time exchange rates.
- **Real-Time API Integration:** Fetch live exchange rates from an external API.
- **Load Balanced Deployment:** Deployed across two web servers behind a load balancer to distribute traffic.

## Requirements

- **Python 3.x**
- **Flask**: `pip install flask`
- **Flask-Login**: `pip install flask-login`
- **Flask-WTF**: `pip install flask-wtf`
- **requests**: `pip install requests`
- **python-dotenv**: `pip install python-dotenv`
- **NGINX (for load balancing)**
- **HAProxy (for SSL termination)**

## Environment Setup

### 1. **Install Dependencies**
Make sure to install the required dependencies for the Flask application:

```bash
pip install -r requirements.txt

Ensure you have the .env file containing the necessary environment variables:

API_KEY – API key for the external currency API.
SECRET_KEY – Secret key for Flask session management.

Example .env:
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

2. Clone the Repository
Clone this repository to your local machine or directly to the web servers.
git clone https://github.com/yourusername/currency-exchange-app.git (#This not the real git repository )
cd currency-exchange-app

3. Run the Flask Application Locally
You can run the Flask application locally for testing purposes. This is primarily for development:
python3 app.py
The app should now be running on http://127.0.0.1:5000 or http://<your_server_ip>:5000.

4. Deploy to Web Servers (web-01 & web-02)
On Each Server (web-01 and web-02):
Clone the repository and install dependencies.
Ensure that the Flask app is set to run on all available network interfaces by setting host="0.0.0.0" in app.py.
For example, in app.py, the line app.run(debug=True, host="0.0.0.0", port=5000) should be configured.

5. Configure Load Balancer
The load balancer distributes incoming traffic between web-01 and web-02. We are using HAProxy for SSL termination and load balancing.

HAProxy Configuration:
Install HAProxy on a separate machine (or use a dedicated instance for load balancing).
Configure HAProxy to listen on port 443 for SSL traffic and forward requests to the web servers (web-01 and web-02) on port 5000.
Example haproxy.cfg:
global
    log /dev/log    local0
    maxconn 200

defaults
    log     global
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

frontend https_front
    bind *:443 ssl crt /etc/ssl/private/your_ssl_cert.pem
    default_backend servers

backend servers
    balance roundrobin
    server web01 172.20.22.201:5000 check (replace with your real server ip address)
    server web02 172.20.22.202:5000 check (#replace with your real server ip address)
Ensure the SSL certificate is valid and properly set up.

6. Firewall Configuration
Ensure the following ports are open on the servers:

Port 443 for SSL traffic (on the load balancer).
Port 5000 for internal communication between HAProxy and the web servers.
7. Run the Load Balancer
Start HAProxy on the load balancer machine:
sudo systemctl restart haproxy
Ensure that HAProxy is running properly:
sudo systemctl status haproxy

8. Testing the Load Balancer
After setting up HAProxy, test the application by accessing the domain (e.g., https://yourdomain.com).

Verify Load Balancing:
You should be able to access the app from multiple browsers or devices, and the load balancer should distribute traffic between the two web servers.
You can check the logs on both web servers to ensure that requests are being handled by both.
9. Monitor and Scale
If needed, you can scale your application by adding more web servers behind the load balancer. Simply update the HAProxy configuration to include additional servers and restart HAProxy.

Troubleshooting
Application Not Loading:

Check if HAProxy is running.
Verify the firewall settings and ensure ports are open.
Check web server logs for errors (/var/log/syslog or application-specific logs).
API Key Issues:

Make sure the API_KEY environment variable is correctly set in the .env file.
Verify that the API key has access to the external currency API and isn't blocked or expired.
SSL Issues:

Ensure the SSL certificate path is correctly configured in HAProxy.
Check the certificate's validity and expiration.
#CONCLUSION
This setup provides a high-availability application with load balancing between multiple web servers and SSL termination through HAProxy. The application is secured with user authentication and allows for real-time currency conversion based on the latest exchange rates.

License
This project is licensed under the MIT License – see the LICENSE file for details.

### Key Sections in the README:

1. **Environment Setup:** Steps for setting up dependencies, environment variables, and configurations.
2. **Deployment to Web Servers:** Instructions for deploying the Flask app on multiple web servers (`web-01`, `web-02`).
3. **Load Balancer Configuration:** Detailed HAProxy configuration for load balancing and SSL termination.
4. **Testing:** How to test the setup to ensure the application is load-balanced and accessible through the load balancer.
5. **Troubleshooting:** Common issues and solutions.

This should cover everything you’ve done, from development to deployment and load balancing. Let me know if you need further adjustments!
