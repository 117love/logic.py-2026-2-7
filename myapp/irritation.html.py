<h2>癪に触った出来事を投稿</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">投稿</button>
</form>

<h2>投稿一覧</h2>

{% for item in irritation %}
    <div>
        <p><strong>いつ:</strong> {{ irritation.date }}</p>
        <p><strong>どこで:</strong> {{ irritation.location }}</p>
        <p><strong>誰から:</strong> {{ irritation.person }}</p>
        <p><strong>どんな言動をされた:</strong> {{ irritation.action }}</p>
        <p><strong>どんな気分:</strong> {{ irritation.feeling }}</p>
        <hr>
    </div>
{% endfor %}