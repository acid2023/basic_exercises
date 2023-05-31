"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""
import random
import uuid
import datetime
import lorem


def generate_chat_history():
    messages_amount = random.randint(200, 1000)
    users_ids = list(
        {random.randint(1, 10000) for _ in range(random.randint(5, 20))}
    )
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": random.choice(
                [
                    None,
                    (
                        random.choice([m["id"] for m in messages])
                        if messages else None
                    ),
                ],
            ),
            "seen_by": random.sample(users_ids,
                                     random.randint(1, len(users_ids))),
            "text": lorem.sentence(),
        })
    return messages


day_period = {'morning': 12, 'afternoon': 18, 'evening': 24}


def get_post_time(messages, id):
    for post in messages:
        if post['id'] == id:
            return post['sent_at'].hour


def get_messages_daytime(messages):
    mornings_count = 0
    afternoon_counts = 0
    evening_counts = 0
    for post in messages:
        post_daytime = get_post_time(messages, post['id'])
        if post_daytime <= day_period['morning']:
            mornings_count += 1
        elif post_daytime <= day_period['afternoon']:
            afternoon_counts += 1
        else:
            evening_counts += 1
    return mornings_count, afternoon_counts, mornings_count


def indexing_replies(messages):
    messages_index = {'sender': {}, 'thread': {}}
    for post in messages:
        messages_index['sender'][post['id']] = post['sent_by']
        messages_index['thread'][post['id']] = post['reply_for']
    return messages_index


def get_posts_stats(messages, replies_index):
    post_stat = {'most_posts': {}, 'most_replies': {}, 'most_views': {}}
    max_posts = 0
    max_replies = 0
    max_views = 0
    for post in messages:
        if post_stat['most_posts'].get(post['sent_by'], None) is None:
            post_stat['most_posts'][post['sent_by']] = 1
        else:
            post_stat['most_posts'][post['sent_by']] += 1
        if post_stat['most_posts'][post['sent_by']] > max_posts:
            max_posts = post_stat['most_posts'][post['sent_by']]
            max_posts_user = [post['sent_by']]
        elif post_stat['most_posts'][post['sent_by']] == max_posts:
            max_posts_user.append(post['sent_by'])
        if post_stat['most_views'].get(post['sent_by'], None) is None:
            post_stat['most_views'][post['sent_by']] = post['seen_by']
        else:
            post_stat['most_views'][post['sent_by']] = post_stat['most_views'][post['sent_by']] + post['seen_by']
        if len(post_stat['most_views'][post['sent_by']]) > max_views:
            max_views = len(post_stat['most_views'][post['sent_by']])
            max_views_user = [post['sent_by']]
        elif len(post_stat['most_views'][post['sent_by']]) == max_views:
            max_views_user.append(post['sent_by'])
        reply_for = post.get('reply_for', None)
        if reply_for is not None:
            sender = replies_index['sender'][post['reply_for']]
        else:
            sender = ''
        if sender != '':
            if post_stat['most_replies'].get(sender, 'None') == 'None':
                post_stat['most_replies'][sender] = 1
            else:
                post_stat['most_replies'][sender] += 1
            if post_stat['most_replies'][sender] > max_replies:
                max_replies = post_stat['most_replies'][sender]
                max_replies_user = [sender]
            elif post_stat['most_replies'][sender] == max_replies:
                max_replies_user.append(sender)
    user_stats = [max_posts_user, max_replies_user, max_views_user]
    return user_stats


def get_longest_thread_new(messages, replies_index):
    max_thread = []
    max_thread_count = 0
    for post in messages:
        thread_count = 0
        reply_for = post['reply_for']
        while True:
            thread_count += 1
            if reply_for is None or reply_for == '':
                break
            next_reply_for = replies_index['thread'].get(reply_for, None)
            if next_reply_for is None:
                break
            reply_for = next_reply_for
        if thread_count > max_thread_count:
            max_thread_count = thread_count
            max_thread = [reply_for]
        elif thread_count == max_thread_count:
            max_thread.append(reply_for)
    return max_thread


if __name__ == "__main__":
    messages = generate_chat_history()
    chat_index = indexing_replies(messages)
    chat_stat = get_posts_stats(messages, chat_index)
    longest_thread = get_longest_thread_new(messages, chat_index)
    print(f'User with most posts - {chat_stat[0]}')
    print(f'User with most replies for her posts - {chat_stat[1]}')
    print(f'User with mosts views for posts - {chat_stat[2]}')
    print(f'Longest thread - {longest_thread[0]}')
    mornings_count, afternoon_counts, evening_counts = get_messages_daytime(messages)
    print(f'Morning posts - {mornings_count}, afternoon posts - {afternoon_counts}, evening posts - {evening_counts}')
