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
import csv


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


def save_chat(message):
    with open('chat.csv', 'w', encoding='utf-8', newline='') as f:
        fields = ["id", "sent_at", "sent_by", "reply_for", "seen_by", "text"]
        writer = csv.DictWriter(f, fields, delimiter=';')
        writer.writeheader()
        for record in messages:
            writer.writerow(record)


def read_chat():
    with open('chat.csv', 'r', encoding='utf-8', newline='') as f1:
        fields = ["id", "sent_at", "sent_by", "reply_for", "seen_by", "text"]
        records = csv.DictReader(f1, fields, delimiter=';')
        return records


def create_message_senders_list(messages):
    user_list = []
    for record in messages:
        if record['sent_by'] not in user_list:
            user_list.append(record['sent_by'])
    return user_list


def get_quantity_of_posts(messages, user):
    posts_count = 0
    for record in messages:
        if record['sent_by'] == user:
            posts_count += 1
    return posts_count


def get_user_most_posts(messages):
    sender_list = create_message_senders_list(messages)
    user = []
    user.clear()
    max_posts = 0
    for sender in sender_list:
        sender_posts = get_quantity_of_posts(messages, sender)
        if sender_posts > max_posts:
            max_posts = sender_posts
            user.clear()
            user.append(sender)
        elif sender_posts == max_posts:
            user.append(sender)
    return user


def get_user_from_post_id(messages, id):
    user = ''
    for post in messages:
        if post['id'] == id:
            user = post['sent_by']
    return user


def get_posts_from_user(message, user):
    user_posts = []
    for post in messages:
        if post['sent_by'] == user:
            user_posts.append(post['id'])
    return user_posts


def get_user_replies(messages, user):
    count_replies = 0
    for post in messages:
        reply_for_id = post['reply_for']
        sender = get_user_from_post_id(messages, reply_for_id)
        if sender == user:
            count_replies += 1
    return count_replies


def get_user_most_replied(messages):
    sender_list = create_message_senders_list(messages)
    user = []
    user.clear()
    max_replies = 0
    for sender in sender_list:
        user_replies = get_user_replies(messages, sender)
        if user_replies > max_replies:
            max_replies = user_replies
            user.clear()
            user.append(sender)
        elif user_replies == max_replies:
            user.append(sender)
    return user


def get_post_views(messages, id):
    for post in messages:
        if post['id'] == id:
            return len(list(set(post['seen_by'])))


def get_user_posts_views(message, user):
    posts_count = 0
    for post in messages:
        sender = post['sent_by']
        id_message = post['id']
        if sender == user:
            posts_count += get_post_views(messages, id_message)
    return posts_count


def get_user_most_viewed(messages):
    sender_list = create_message_senders_list(messages)
    user = []
    user.clear()
    max_views = 0
    for sender in sender_list:
        user_views = get_user_posts_views(messages, sender)
        if user_views > max_views:
            max_views = user_views
            user.clear()
            user.append(sender)
        elif user_views == max_views:
            user.append(sender)
    return user


def get_list_of_threads(message):
    thread_list = []
    for post in messages:
        if post['reply_for'] is None:
            thread_list.append(post['id'])
    return thread_list


def get_replies_to_post(messages, id):
    list_of_replies = []
    list_of_replies.clear()
    for post in messages:
        if post['reply_for'] == id:
            list_of_replies.append(post['id'])
    return list_of_replies


def merge_lists(list1, list2):
    merged_list = list1.copy()
    for item in list2:
        merged_list.append(item)
    return merged_list


def get_replies_to_posts_list(messages, posts):
    replies_list = []
    replies_list.clear()
    new_replies_list = []
    merged_replies_list = []
    for post in posts:
        new_replies_list = get_replies_to_post(messages, post)
        merged_replies_list = merge_lists(replies_list, new_replies_list)
        replies_list.clear()
        replies_list = merged_replies_list.copy()
    return replies_list


def get_replies_to_thread(messages, id):
    replies_list = get_replies_to_post(messages, id)
    current_level_replies_list = replies_list.copy()
    next_level_replies_list = []
    not_end_of_thread = True
    while not_end_of_thread:
        next_level_replies_list.clear()
        next_level_replies_list = get_replies_to_posts_list(messages, current_level_replies_list)
        if len(next_level_replies_list) == 0:
            return replies_list
        replies_list = replies_list + current_level_replies_list
        current_level_replies_list.clear()
        current_level_replies_list = next_level_replies_list.copy()


def get_longest_thread(messages):
    threads = get_list_of_threads(messages)
    max_length_of_thread = 0
    max_thread = []
    max_thread.clear()
    for thread in threads:
        current_thread_length = len(get_replies_to_thread(messages, thread))
        if current_thread_length > max_length_of_thread:
            max_length_of_thread = current_thread_length
            max_thread.clear()
            max_thread.append(thread)
        elif current_thread_length == max_length_of_thread:
            max_thread.append(thread)
        return max_thread


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

def get_posts_without_reply(messages):
    reply_list_posts = []
    reply_list_posts.clear()
    for post in messages:
        if post['reply_for'] != None:
            reply_list_posts.append(post['reply_for'])
    list_posts = [] 
    list_posts.clear()
    for post in messages:
        if not post['id'] in reply_list_posts:
            list_posts.append(post['id'])
    return list_posts


def get_previous_level_starter_for_post(messages, id):
    for post in messages:
        if post['id'] == id:
            return post['reply_for']
    return None


def get_thread_length(messages, id):
    counter = 1
    current_id = id
    while True:
        prev_level_id = get_previous_level_starter_for_post(messages, current_id)
        if prev_level_id is None:
            return counter
        counter += 1
        current_id = prev_level_id


def get_longest_thread_alt(messages):
    max_thread = 0
    longest_thread = []
    longest_thread.clear()
    check_list = get_posts_without_reply(messages)
    for post in check_list:
        current_thread_length = get_thread_length(messages, post)
        if current_thread_length > max_thread:
            max_thread = current_thread_length
            longest_thread.clear()
            longest_thread.append(post)
        elif current_thread_length == max_thread:
            longest_thread.append(post)
    return longest_thread, max_thread


if __name__ == "__main__":
    messages = generate_chat_history()
    print(f'User with most posts - {get_user_most_posts(messages)}')
    print(f'User with most replies for her posts - {get_user_most_replied(messages)}')
    print(f'User with mosts views for posts - {get_user_most_viewed(messages)}')
    print(f'Longest thread with max replies - {get_longest_thread_alt(messages)}')
    mornings_count, afternoon_counts, evening_counts = get_messages_daytime(messages)
    print(f'Morning posts - {mornings_count}, afternoon posts - {afternoon_counts}, evening posts - {evening_counts}')
