# Example 1: Simple Text Translation
example_simple_text = {
    "input_query": "Hello, how are you today?",
    "target_language": "Spanish",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": "Hola, ¿cómo estás hoy?",
        "current_translation": "Hola, ¿cómo estás hoy?",
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Translation is accurate and natural with proper punctuation",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 5,
    },
    "format_state": {
        "final_translation": "Hola, ¿cómo estás hoy?",
        "final_translation_rating": 5,
    },
}

# Example 2: JSON Object Translation
example_json = {
    "input_query": '{"greeting": "Hello", "question": "How are you?", "farewell": "Goodbye"}',
    "target_language": "French",
    "query_info": {
        "is_json": True,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": '{"greeting": "Bonjour", "question": "Comment allez-vous?", "farewell": "Au revoir"}',
        "current_translation": '{"greeting": "Bonjour", "question": "Comment allez-vous?", "farewell": "Au revoir"}',
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "JSON structure preserved perfectly, all values translated accurately with proper French grammar",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 5,
    },
    "format_state": {
        "final_translation": '{\n  "greeting": "Bonjour",\n  "question": "Comment allez-vous?",\n  "farewell": "Au revoir"\n}',
        "final_translation_rating": 5,
    },
}

# Example 3: HTML Document Translation
example_html = {
    "input_query": "<h1>Welcome to our website</h1><p>This is a <strong>great</strong> product.</p>",
    "target_language": "German",
    "query_info": {
        "is_json": False,
        "is_html": True,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": "<h1>Willkommen auf unserer Website</h1><p>Dies ist ein <strong>großartiges</strong> Produkt.</p>",
        "current_translation": "<h1>Willkommen auf unserer Website</h1><p>Dies ist ein <strong>großartiges</strong> Produkt.</p>",
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "HTML tags preserved correctly, German translation is natural and grammatically correct",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 4,
    },
    "format_state": {
        "final_translation": "<h1>Willkommen auf unserer Website</h1>\n<p>Dies ist ein <strong>großartiges</strong> Produkt.</p>",
        "final_translation_rating": 4,
    },
}

# Example 4: Markdown Document Translation
example_markdown = {
    "input_query": "# User Guide\n\n## Getting Started\n\nWelcome to our **amazing** application!\n\n- Feature 1: Easy to use\n- Feature 2: Fast performance",
    "target_language": "Japanese",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": True,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": "# ユーザーガイド\n\n## はじめに\n\n私たちの**素晴らしい**アプリケーションへようこそ！\n\n- 機能1：使いやすい\n- 機能2：高速パフォーマンス",
        "current_translation": "# ユーザーガイド\n\n## はじめに\n\n私たちの**素晴らしい**アプリケーションへようこそ！\n\n- 機能1：使いやすい\n- 機能2：高速パフォーマンス",
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Markdown formatting preserved perfectly, Japanese translation is natural and culturally appropriate",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 5,
    },
    "format_state": {
        "final_translation": "# ユーザーガイド\n\n## はじめに\n\n私たちの**素晴らしい**アプリケーションへようこそ！\n\n- 機能1：使いやすい\n- 機能2：高速パフォーマンス",
        "final_translation_rating": 5,
    },
}

# Example 5: SQL Query Translation (Comments)
example_sql = {
    "input_query": "-- Get all active users\nSELECT * FROM users WHERE status = 'active' -- Filter active users only",
    "target_language": "Portuguese",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": False,
        "is_sql": True,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": "-- Obter todos os usuários ativos\nSELECT * FROM users WHERE status = 'active' -- Filtrar apenas usuários ativos",
        "current_translation": "-- Obter todos os usuários ativos\nSELECT * FROM users WHERE status = 'active' -- Filtrar apenas usuários ativos",
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "SQL syntax preserved correctly, comments translated accurately to Portuguese",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 5,
    },
    "format_state": {
        "final_translation": "-- Obter todos os usuários ativos\nSELECT * FROM users WHERE status = 'active' -- Filtrar apenas usuários ativos",
        "final_translation_rating": 5,
    },
}

# Example 6: Code Blocks Translation
example_code_blocks = {
    "input_query": 'Here\'s how to create a function:\n\n```python\ndef greet_user(name):\n    """Greet the user by name"""\n    return f"Hello, {name}!"\n```\n\nThis function says hello to the user.',
    "target_language": "Italian",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": True,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": True,
    },
    "translation_state": {
        "initial_translation_result": 'Ecco come creare una funzione:\n\n```python\ndef greet_user(name):\n    """Saluta l\'utente per nome"""\n    return f"Ciao, {name}!"\n```\n\nQuesta funzione saluta l\'utente.',
        "current_translation": 'Ecco come creare una funzione:\n\n```python\ndef greet_user(name):\n    """Saluta l\'utente per nome"""\n    return f"Ciao, {name}!"\n```\n\nQuesta funzione saluta l\'utente.',
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Code structure preserved, comments and text translated naturally, good Italian flow",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 4,
    },
    "format_state": {
        "final_translation": 'Ecco come creare una funzione:\n\n```python\ndef greet_user(name):\n    """Saluta l\'utente per nome"""\n    return f"Ciao, {name}!"\n```\n\nQuesta funzione saluta l\'utente.',
        "final_translation_rating": 4,
    },
}

# Example 7: Multiple Translation Iterations
example_iterations = {
    "input_query": '{"error_message": "Invalid credentials provided", "retry_prompt": "Please try again"}',
    "target_language": "Arabic",
    "query_info": {
        "is_json": True,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": '{"error_message": "بيانات اعتماد غير صحيحة مقدمة", "retry_prompt": "يرجى المحاولة مرة أخرى"}',
        "current_translation": '{"error_message": "بيانات الاعتماد المقدمة غير صالحة", "retry_prompt": "يرجى المحاولة مرة أخرى"}',
        "iteration": 2,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Significant improvement after iterations - more formal and accurate Arabic translation achieved",
        "defective_keys": [],
        "review_iteration": 2,
        "review_translation_rating": 4,
    },
    "format_state": {
        "final_translation": '{\n  "error_message": "بيانات الاعتماد المقدمة غير صالحة",\n  "retry_prompt": "يرجى المحاولة مرة أخرى"\n}',
        "final_translation_rating": 4,
    },
}

# Example 8: JSON with Defective Keys
example_defective_json = {
    "input_query": '{"user_name": "John Doe", "email": "john@example.com", "preferences": {"theme": "dark", "language": "English"}}',
    "target_language": "Chinese",
    "query_info": {
        "is_json": True,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": '{"user_name": "约翰·多", "email": "john@example.com", "preferences": {"theme": "黑暗", "language": "英语"}}',
        "current_translation": '{"user_name": "约翰·多伊", "email": "john@example.com", "preferences": {"theme": "深色", "language": "英语"}}',
        "iteration": 1,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Initial translation had issues with name truncation and theme terminology, corrected in iteration 1",
        "defective_keys": ["user_name", "theme"],
        "review_iteration": 1,
        "review_translation_rating": 3,
    },
    "format_state": {
        "final_translation": '{\n  "user_name": "约翰·多伊",\n  "email": "john@example.com",\n  "preferences": {\n    "theme": "深色",\n    "language": "英语"\n  }\n}',
        "final_translation_rating": 3,
    },
}

# Example 9: API Endpoint Translation
example_api = {
    "input_query": "GET /api/users?status=active&limit=10 - Retrieve active users with pagination",
    "target_language": "Russian",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": True,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": "GET /api/users?status=active&limit=10 - Получить активных пользователей с пагинацией",
        "current_translation": "GET /api/users?status=active&limit=10 - Получить активных пользователей с пагинацией",
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "API endpoint syntax preserved correctly, Russian description is accurate and technical",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 5,
    },
    "format_state": {
        "final_translation": "GET /api/users?status=active&limit=10 - Получить активных пользователей с пагинацией",
        "final_translation_rating": 5,
    },
}

# Example 10: URL with Description
example_url = {
    "input_query": "Visit our homepage at https://example.com for more information about our services",
    "target_language": "Korean",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": True,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": "서비스에 대한 자세한 정보는 https://example.com 홈페이지를 방문하세요",
        "current_translation": "서비스에 대한 자세한 정보는 https://example.com 홈페이지를 방문하세요",
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "URL preserved intact, Korean translation is polite and natural with appropriate honorifics",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 5,
    },
    "format_state": {
        "final_translation": "서비스에 대한 자세한 정보는 https://example.com 홈페이지를 방문하세요",
        "final_translation_rating": 5,
    },
}

# Example 11: Complex Mixed Content
example_11_mixed = {
    "input_query": '# API Documentation\n\n## User Registration\n\n```json\n{\n  "username": "Enter your username",\n  "password": "Enter secure password"\n}\n```\n\nSend POST to `/api/register` - Creates new user account',
    "target_language": "Dutch",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": True,
        "is_sql": False,
        "is_api": True,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": True,
    },
    "translation_state": {
        "initial_translation_result": '# API Documentatie\n\n## Gebruikersregistratie\n\n```json\n{\n  "username": "Voer uw gebruikersnaam in",\n  "password": "Voer veilig wachtwoord in"\n}\n```\n\nStuur POST naar `/api/register` - Maakt nieuw gebruikersaccount aan',
        "current_translation": '# API Documentatie\n\n## Gebruikersregistratie\n\n```json\n{\n  "username": "Voer uw gebruikersnaam in",\n  "password": "Voer een veilig wachtwoord in"\n}\n```\n\nStuur POST naar `/api/register` - Maakt een nieuw gebruikersaccount aan',
        "iteration": 1,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Mixed content handled excellently, minor Dutch grammar improvements in iteration 1 for natural flow",
        "defective_keys": [],
        "review_iteration": 1,
        "review_translation_rating": 4,
    },
    "format_state": {
        "final_translation": '# API Documentatie\n\n## Gebruikersregistratie\n\n```json\n{\n  "username": "Voer uw gebruikersnaam in",\n  "password": "Voer een veilig wachtwoord in"\n}\n```\n\nStuur POST naar `/api/register` - Maakt een nieuw gebruikersaccount aan',
        "final_translation_rating": 4,
    },
}

# Example 12: Low Quality Translation Requiring Multiple Fixes
example_poor_quality = {
    "input_query": '{"welcome_message": "Welcome to our platform", "instructions": "Follow these steps to get started", "support_contact": "Contact support for help"}',
    "target_language": "Hindi",
    "query_info": {
        "is_json": True,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": '{"welcome_message": "हमारे प्लेटफॉर्म में आपका स्वागत है", "instructions": "शुरू करने के लिए इन चरणों का पालन करें", "support_contact": "सहायता के लिए सपोर्ट से संपर्क करें"}',
        "current_translation": '{"welcome_message": "हमारे प्लेटफॉर्म पर आपका स्वागत है", "instructions": "आरंभ करने के लिए इन चरणों का पालन करें", "support_contact": "सहायता के लिए समर्थन से संपर्क करें"}',
        "iteration": 3,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Multiple iterations needed to achieve proper Hindi formality, consistency, and natural flow. Final version much improved.",
        "defective_keys": ["welcome_message", "instructions", "support_contact"],
        "review_iteration": 3,
        "review_translation_rating": 2,
    },
    "format_state": {
        "final_translation": '{\n  "welcome_message": "हमारे प्लेटफॉर्म पर आपका स्वागत है",\n  "instructions": "आरंभ करने के लिए इन चरणों का पालन करें",\n  "support_contact": "सहायता के लिए समर्थन से संपर्क करें"\n}',
        "final_translation_rating": 3,
    },
}

# Example 13: File-based Translation
example_file = {
    "input_query": "config.properties:\napp.name=My Application\napp.version=1.0.0\napp.description=This is a sample application for demonstration",
    "target_language": "Spanish",
    "query_info": {
        "is_json": False,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": True,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": "config.properties:\napp.name=Mi Aplicación\napp.version=1.0.0\napp.description=Esta es una aplicación de muestra para demostración",
        "current_translation": "config.properties:\napp.name=Mi Aplicación\napp.version=1.0.0\napp.description=Esta es una aplicación de muestra para demostración",
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Properties file format preserved, appropriate values translated, version numbers kept intact",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 5,
    },
    "format_state": {
        "final_translation": "config.properties:\napp.name=Mi Aplicación\napp.version=1.0.0\napp.description=Esta es una aplicación de muestra para demostración",
        "final_translation_rating": 5,
    },
}

# Example 14: Review vs Format Rating Difference
example_rating_difference = {
    "input_query": '{"notification": "You have 5 new messages", "action_button": "View Messages", "dismiss": "Dismiss"}',
    "target_language": "Vietnamese",
    "query_info": {
        "is_json": True,
        "is_html": False,
        "is_markdown": False,
        "is_sql": False,
        "is_api": False,
        "is_file": False,
        "is_url": False,
        "contains_code_blocks": False,
    },
    "translation_state": {
        "initial_translation_result": '{"notification": "Bạn có 5 tin nhắn mới", "action_button": "Xem Tin nhắn", "dismiss": "Bỏ qua"}',
        "current_translation": '{"notification": "Bạn có 5 tin nhắn mới", "action_button": "Xem Tin nhắn", "dismiss": "Bỏ qua"}',
        "iteration": 0,
    },
    "review_state": {
        "review_decision": "APPROVE",
        "review_reasoning": "Translation accuracy is good but could be more natural in Vietnamese context",
        "defective_keys": [],
        "review_iteration": 0,
        "review_translation_rating": 3,
    },
    "format_state": {
        "final_translation": '{\n  "notification": "Bạn có 5 tin nhắn mới",\n  "action_button": "Xem Tin nhắn",\n  "dismiss": "Bỏ qua"\n}',
        "final_translation_rating": 4,
    },
}

# Collection of all updated examples
translation_examples = [
    example_simple_text,
    example_json,
    example_html,
    example_markdown,
    example_sql,
    example_code_blocks,
    example_iterations,
    example_defective_json,
    example_api,
    example_url,
    example_poor_quality,
    example_file,
    example_rating_difference,
]
