<!DOCTYPE html>
<html>
<head>
    <title>出来事を投稿</title>
</head>
<body>
    <h2>嫌な出来事を投稿</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">投稿</button>
    </form>
    <a href="{% url 'user_event_list' %}">投稿一覧へ</a>
</body>
</html>