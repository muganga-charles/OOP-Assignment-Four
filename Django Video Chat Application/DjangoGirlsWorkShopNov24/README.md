
# 💬 Django Real-Time Chat Application

A real-time chat application built with Django and WebSockets, enabling instant messaging between multiple users in different chat rooms.

## ✨ Features

- Real-time messaging using WebSockets
- Multiple chat rooms
- Clean and responsive UI
- User authentication
- Message history
- Room-based conversations

## 🛠️ Technologies Used

- Django 5.x
- Channels (WebSockets)
- HTML/CSS
- JavaScript
- SQLite3

## 📋 Prerequisites

- Python 3.10+
- Virtual Environment

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/django-chat-app.git
cd django-chat-app
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Apply migrations**
```bash
python manage.py migrate
```

5. **Run the development server**
```bash
python manage.py runserver
```

## 📁 Project Structure
```
django-chat-app/
├── chat/                   # Main application directory
├── config/                 # Project configuration
├── static/                 # Static files (CSS, JS)
├── templates/             # HTML templates
└── manage.py              # Django management script
```

## 💻 Usage

1. Navigate to `http://localhost:8000`
2. Provide a username and a new chat room or join an existing one
3. Start chatting in real-time!


## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

For more detailed information, please refer to the [Django Girls Workshop Guide](https://djangogirls.tz/workshop/django-workshop.pdf)

## 👥 Authors

- [Fuad Habib](https://github.com/AvicennaJr)

---
⭐️ Star this repository if you find it helpful!
