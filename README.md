# Telegram Group Manager

### Project Background

This project was born from my need as a D&D Dungeon Master to simultaneously send pre-prepared messages to my players, and it has also been my first experiment in developing an entire software generated with AI Claude 4. I went through trial and error but I'm satisfied with the work done so far, even though it still has ample room for improvement.

The software is completely AI-generated and represents an example of how artificial intelligence can transform a specific idea into a complete and functional web application.
An advanced web application for managing user groups and sending personalized messages via Telegram bot with template support and detailed history tracking.

## Main Features

### Core Features
- **Group Management**: Create and manage user groups with intuitive interface
- **Personalized Messages**: Send different messages to each group user
- **Message Templates**: Prepare and save message lists for future use
- **Advanced History**: View sent messages with filters and statistics
- **User Import**: Automatically import users who have interacted with the bot
- **Multilingual Interface**: Support for 5 languages (Italian, English, French, German, Spanish)
- **MySQL Database**: Reliable persistence with backup and optimized performance

### New Features v2.0

#### 🎯 **Message Templates**
- **Template Creation**: Prepare personalized message lists with name and description
- **Automatic Save**: Templates are saved in database for future reuse
- **Quick Loading**: Load existing templates into the message sending form
- **Direct Send**: Send all template messages with a single click
- **Template Management**: View, edit and delete saved templates

#### 📊 **Advanced Message History**
- **Smart Filters**: Filter by status (sent/failed) and specific user
- **Real-time Statistics**: View success rates and performance metrics
- **Pagination**: Efficient handling of large message datasets
- **Error Details**: View specific errors to diagnose problems
- **Full View**: Expand long messages for complete visualization

#### 🌍 **Multilingual Support**
- **5 Supported Languages**: Italian (default), English, French, German, Spanish
- **Dynamic Switching**: Change language with one click, stored in session
- **Complete Interface**: All interface texts are translated
- **.po Files**: Translation management via standard Gettext files

#### 🔧 **Debug Tools**
- **Bot Connection Test**: Verify token configuration and bot status
- **Single Message Test**: Send test messages to specific users
- **Environment Debug**: Check .env variables and configuration
- **Detailed Logs**: Complete tracking of errors and successes

## Project Structure

```
telegram-group-manager/
├── app/
│   ├── __init__.py              # Flask app initialization with Babel
│   ├── models.py                # Extended database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Homepage and dashboard routes
│   │   ├── groups.py            # Group and template management routes
│   │   ├── telegram_bot.py      # Telegram bot operation routes
│   │   └── i18n.py              # Language management routes
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css       # Custom styles
│   │   └── js/
│   │       └── main.js          # Custom JavaScript
│   ├── templates/
│   │   ├── base.html            # Base template with language selector
│   │   ├── index.html           # Homepage/Dashboard
│   │   ├── group_detail.html    # Group detail with advanced tools
│   │   └── groups/              # Templates for group features
│   │       ├── templates.html   # Saved templates list
│   │       ├── create_template.html  # New template creation
│   │       ├── view_template.html    # Template view
│   │       └── message_history.html # Advanced message history
│   ├── utils/
│   │   ├── __init__.py
│   │   └── telegram_helper.py   # Helper functions for Telegram API
│   └── translations/            # Translation files
│       ├── en/LC_MESSAGES/      # English
│       ├── fr/LC_MESSAGES/      # French
│       ├── de/LC_MESSAGES/      # German
│       └── es/LC_MESSAGES/      # Spanish
├── instance/
├── .env                         # Environment variables
├── babel.cfg                    # Babel configuration
├── requirements.txt             # Updated Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher (or MariaDB 10.2+)
- Telegram bot created via @BotFather
- Telegram bot token

### MySQL Database Setup

1. **Install MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install mysql-server
   
   # macOS with Homebrew
   brew install mysql
   
   # Windows: Download from https://dev.mysql.com/downloads/mysql/
   ```

2. **Configure MySQL**
   ```bash
   # Access MySQL
   sudo mysql -u root -p
   
   # Create dedicated user
   CREATE USER 'telegram_user'@'localhost' IDENTIFIED BY 'your_password';
   
   # Create database
   CREATE DATABASE telegram_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Grant permissions
   GRANT ALL PRIVILEGES ON telegram_manager.* TO 'telegram_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

### Application Setup

1. **Clone or download the project**
   ```bash
   cd telegram-group-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Linux/Mac
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Edit the `.env` file:
   ```env
   # Telegram Bot
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   
   # MySQL Database
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=telegram_manager
   DB_USER=telegram_user
   DB_PASSWORD=your_password
   
   # Security
   SECRET_KEY=your_very_long_random_secret_key_here
   
   # Environment
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Create additional tables**
   ```bash
   python create_message_templates.py
   ```

6. **Start the application**
   ```bash
   python run.py
   ```

7. **Access the application**

   Open browser: `http://127.0.0.1:5000`

## Telegram Bot Configuration

### Bot Creation

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Get the bot token
4. Insert the token in the `.env` file

### Configuration Testing

Use the integrated debug tools:
- `/groups/{group_id}/debug_bot` - Test token and connection
- `/groups/{group_id}/test_message/{user_id}` - Test single message sending

## Using New Features

### 🎯 Message Templates

#### Template Creation
1. Go to group details
2. Click **"New Template"** in Advanced Tools section
3. Enter template name and description
4. Fill personalized messages for each user
5. Click **"Save Template"**

#### Template Usage
1. Go to **"View Templates"** to see saved templates
2. Click **"Load & Send"** to load a template into the form
3. Modify messages if needed
4. Send normally or use **"Direct Send"** from template

#### Template Management
- **View**: See all messages in a template
- **Load**: Load into form for modifications
- **Direct Send**: Send immediately without changes
- **Delete**: Remove templates no longer needed

### 📊 Advanced Message History

#### Viewing
1. Go to group details
2. Click **"Message History"** in Advanced Tools
3. View real-time success statistics

#### Available Filters
- **By Status**: All, Sent, Failed, Pending
- **By User**: Filter messages from specific user
- **Combined**: Use both filters together

#### Features
- **Pagination**: Navigate through message pages
- **Error Details**: Click "Error" to see specific details
- **Full Messages**: Expand truncated long messages
- **Reset Filters**: Return to complete view

### 🌍 Language Switching

1. Use the language selector in the header (top right)
2. Language is stored in session
3. Reload page to see all translated texts

#### Supported Languages
- 🇮🇹 **Italiano** (default)
- 🇬🇧 **English**
- 🇫🇷 **Français**
- 🇩🇪 **Deutsch**
- 🇪🇸 **Español**

## Updated Database Structure

### New Tables

**message_templates**
- `id`: Primary ID
- `name`: Template name (max 200 char)
- `description`: Optional description
- `group_id`: Group reference (FK)
- `created_at`: Creation date
- `updated_at`: Last update
- `is_active`: Soft delete flag

**template_messages**
- `id`: Primary ID
- `template_id`: Template reference (FK)
- `user_id`: User reference (FK)
- `message_text`: Personalized message text
- `order_index`: Order in template
- `created_at`: Creation date

### Existing Tables (Updated)

**message_logs** (improved)
- Now includes detailed `error_message`
- `telegram_message_id` for Telegram tracking
- Better indexes for filter performance

**users** (extended)
- `language_code`: User preferred language
- `display_name`: Improved display name
- Optimized indexes for searches

**groups** (optimized)
- Relationship with `message_templates`
- Automatic timestamp updates
- Improved query performance

## Updated API Endpoints

### Template Routes
- `GET /groups/<id>/templates` - List group templates
- `POST /groups/<id>/templates/create` - Create new template
- `GET /groups/<id>/templates/<template_id>` - View template
- `GET /groups/<id>/templates/<template_id>/load` - Load template into form
- `POST /groups/<id>/templates/<template_id>/send` - Send template messages
- `POST /groups/<id>/templates/<template_id>/delete` - Delete template

### History Routes
- `GET /groups/<id>/message_history` - History with filters
- Query params: `status`, `user_id`, `page` for filters and pagination

### Debug Routes
- `GET /groups/<id>/debug_bot` - Test bot configuration
- `GET /groups/<id>/test_message/<user_id>` - Test single message
- `GET /groups/<id>/debug_env` - Debug environment variables

### Language Routes
- `GET /i18n/set/<language>` - Change interface language
- Supports: `it`, `en`, `fr`, `de`, `es`

## Advanced Features

### Template Intelligence
- **Real-time Statistics**: Count filled messages during creation
- **Smart Preview**: Preview messages before saving
- **Quick Actions**: Automatic filling for all users
- **Smart Validation**: Check template completeness before saving

### History Analytics
- **Success Rates**: Calculate sending success percentage
- **Combined Filters**: Combine multiple filters for detailed analysis
- **Export Ready**: Data structure ready for CSV/Excel export
- **Trend Analysis**: View sending trends over time

### Performance Optimizations
- **Efficient Queries**: Optimized indexes for history filters
- **Smart Pagination**: Progressive loading for large datasets
- **Session Cache**: User preference storage
- **Lazy Loading**: Load components only when needed

## Updated Troubleshooting

### Template Errors

**"Template not saved"**
- Verify at least one message is filled
- Check template name doesn't already exist
- Ensure group has users

**"Template not loaded"**
- Check template exists and is active
- Verify group access permissions
- Refresh page if necessary

### History Errors

**"Empty history"**
- Check messages have been sent
- Verify applied filters (might hide results)
- Check database connection

**"Filters not working"**
- Use "Reset" button to return to complete view
- Verify selected users have messages
- Check filtered statuses exist

### Multilingual Errors

**"Texts not translated"**
- Verify .mo files are compiled
- Check language is supported
- Restart application after translation changes

**"Language change not working"**
- Check i18n route is registered
- Verify Flask sessions work
- Check translation file permissions

### Improved Bot Debug

**Token not found**
```bash
# Verify .env file
cat .env | grep TELEGRAM_BOT_TOKEN

# Manual token test
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

**Messages not arriving**
```bash
# Use debug routes
/groups/{group_id}/debug_env
/groups/{group_id}/test_message/{user_id}

# Check detailed logs in console
```

## Backup and Security

### Template Backup
Templates are saved in `message_templates` and `template_messages`:

```sql
-- Backup templates only
mysqldump -u telegram_user -p telegram_manager message_templates template_messages > templates_backup.sql

-- Restore templates
mysql -u telegram_user -p telegram_manager < templates_backup.sql
```

### Multilingual Security
- Translation files protected from direct access
- Input validation to prevent injection
- Language parameter sanitization

### Template Performance
- Optimized indexes for template searches
- In-memory cache for frequent templates
- Automatic cleanup of unused templates

## Future Roadmap

### V2.1 (Next)
- **History Export**: Export messages to CSV/Excel
- **Shared Templates**: Share templates between groups
- **Scheduled Messages**: Message sending scheduling
- **Rich Text Editor**: Advanced message editor

### V2.2 (Future)
- **Dashboard Analytics**: Advanced charts and metrics
- **REST API**: Public endpoints for integration
- **Webhook Support**: Real-time notifications
- **Mobile App**: Companion app for iOS/Android

### V3.0 (Vision)
- **Multi-Bot Support**: Multiple bot management
- **Team Collaboration**: Share groups between users
- **Advanced Automation**: Automated workflows
- **Enterprise Features**: SSO, audit logs, compliance

## Common Error Solutions

### Database Connection Issues

**"Can't connect to MySQL server"**
- Verify MySQL is running: `sudo systemctl status mysql`
- Check host and port in `.env` file
- Test connection: `mysql -h localhost -u telegram_user -p`

**"Access denied for user"**
- Verify username and password in `.env` file
- Check MySQL user permissions:
  ```sql
  SHOW GRANTS FOR 'telegram_user'@'localhost';
  ```
- Recreate user if necessary

**"Unknown database 'telegram_manager'"**
- Run `python setup_database.py` to create database
- Or create manually:
  ```sql
  CREATE DATABASE telegram_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

### Bot Configuration Issues

**"Bot token not configured"**
- Verify token is correct in `.env` file
- Ensure `.env` file is in main directory
- Check token format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

**"Bot connection error"**
- Check internet connection
- Verify token is valid with @BotFather
- Test manually: `https://api.telegram.org/bot<TOKEN>/getMe`

**"No users imported"**
- Users must have interacted with bot at least once
- Verify bot is not blocked by users
- Check bot has message reading permissions

**"Message sending error"**
- User might have blocked the bot
- Verify Telegram ID is correct
- Check Telegram API rate limits (30 msg/sec)

### Performance Optimization

#### MySQL Configuration

```sql
-- my.cnf or my.ini
[mysqld]
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
max_connections = 200
query_cache_size = 64M
tmp_table_size = 64M
max_heap_table_size = 64M
```

#### Query Monitoring

```sql
-- Slow queries
SHOW PROCESSLIST;

-- Table statistics
SELECT table_name, table_rows, data_length, index_length 
FROM information_schema.tables 
WHERE table_schema = 'telegram_manager';

-- Used indexes
SHOW INDEX FROM users;
SHOW INDEX FROM groups;
SHOW INDEX FROM message_logs;
```

## Requirements

### System Requirements
- **Operating System**: Linux, macOS, Windows
- **Python**: 3.8+ (recommended 3.9+)
- **Database**: MySQL 5.7+ or MariaDB 10.2+
- **Memory**: Minimum 512MB RAM (recommended 1GB+)
- **Storage**: 100MB + database storage

### Python Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Babel==3.1.0
python-dotenv==1.0.0
PyMySQL==1.1.0
requests==2.31.0
```

### Browser Support
- **Chrome**: 80+
- **Firefox**: 75+
- **Safari**: 13+
- **Edge**: 80+

## Security Considerations

### Production Deployment
- Change `SECRET_KEY` to a strong random value
- Use environment variables for all sensitive data
- Enable HTTPS/SSL for web traffic
- Restrict database access to application only
- Regular security updates for dependencies

### Bot Security
- Keep bot token confidential
- Use webhook instead of polling for production
- Implement rate limiting for API calls
- Monitor bot usage and logs

### Data Protection
- Regular database backups
- Encrypt sensitive data at rest
- Implement proper access controls
- Log security events

---

**Version**: 2.0.0  
**Database**: MySQL 5.7+ / MariaDB 10.2+  
**Last Updated**: August 2025  
**Compatibility**: Python 3.8+, Flask 2.3+, Bootstrap 5  
**New Features**: Message Templates, Advanced History, Multilingual Support