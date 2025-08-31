# Krishi360 - Agricultural Platform

Krishi360 is a comprehensive agricultural platform that connects farmers, buyers, and agricultural consultants to create a sustainable and efficient agricultural ecosystem.

## 🌱 Features

### For Farmers
- **Crop Management**: List and manage your crops with detailed information
- **Direct Sales**: Connect directly with buyers without intermediaries
- **Expert Consultations**: Get advice from agricultural experts
- **Order Tracking**: Monitor orders and manage inventory

### For Buyers
- **Browse Crops**: Discover fresh produce from local farmers
- **Secure Payments**: Safe and secure payment processing
- **Order Tracking**: Real-time order status updates
- **Quality Assurance**: Access to organic and certified produce

### For Consultants
- **Expert Advice**: Provide consultations to farmers
- **Knowledge Sharing**: Share agricultural expertise
- **Consultation Management**: Manage consultation requests
- **Rating System**: Build reputation through farmer feedback

### For Administrators
- **User Management**: Manage all platform users
- **Analytics Dashboard**: Comprehensive platform statistics
- **Order Management**: Oversee all transactions
- **Content Moderation**: Ensure platform quality

## 🚀 Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login with role-based access control
- **Styling**: Custom CSS with light green agricultural theme

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd krishi-360
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env with your configuration
   # At minimum, set a strong SECRET_KEY
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 👥 Demo Accounts

The initialization script creates several demo accounts for testing:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Farmer | farmer1 | password123 |
| Buyer | buyer1 | password123 |
| Consultant | consultant1 | password123 |

## 🎨 Design Features

- **Light Green Theme**: Agricultural-inspired color scheme
- **Rice Field Backgrounds**: Beautiful SVG backgrounds representing rice fields
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern UI**: Clean, intuitive interface with Bootstrap 5
- **Accessibility**: WCAG compliant design elements

## 📁 Project Structure

```
krishi-360/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables example
├── routes/                # Route blueprints
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   ├── farmer.py         # Farmer-specific routes
│   ├── buyer.py          # Buyer-specific routes
│   ├── consultant.py     # Consultant routes
│   └── admin.py          # Admin routes
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── auth/             # Authentication templates
│   ├── farmer/           # Farmer templates
│   ├── buyer/            # Buyer templates
│   ├── consultant/       # Consultant templates
│   └── admin/            # Admin templates
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── main.js       # JavaScript functions
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///krishi360.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
```

### Database Configuration

- **Development**: SQLite database (default)
- **Production**: PostgreSQL or MySQL recommended

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

1. **Set up a production database**
2. **Configure environment variables**
3. **Use a production WSGI server** (e.g., Gunicorn)
4. **Set up reverse proxy** (e.g., Nginx)
5. **Enable HTTPS**

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@krishi360.com or create an issue in the repository.

## 🔮 Future Enhancements

- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time chat system
- [ ] Advanced analytics and reporting
- [ ] Weather integration
- [ ] IoT device integration
- [ ] Blockchain for supply chain tracking
- [ ] Machine learning for crop recommendations
- [ ] Multi-language support
- [ ] Advanced payment gateways
- [ ] SMS/Email notifications

## 🙏 Acknowledgments

- Bootstrap for the responsive framework
- Font Awesome for the beautiful icons
- Flask community for the excellent documentation
- Agricultural experts for domain knowledge

---

**Krishi360** - Growing Agriculture, Growing Communities 🌾
