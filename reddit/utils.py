from typing import Optional

import praw
from django.conf import settings
from . import models

reddit = praw.Reddit(
    client_id=settings.PRAW_CLIENT_ID,
    client_secret=settings.PRAW_CLIENT_SECRET,
    user_agent=settings.PRAW_USER_AGENT,
)


def get_submission(channel: models.Channel) -> Optional[models.Submission]:
    subreddits = '+'.join((models.Subscription.objects.filter(channel=channel).values_list('subreddit', flat=True)))

    posts = reddit.subreddit(subreddits).hot()
    posts = filter(lambda p: 'jpg' in p.url or 'png' in p.url, posts)

    for post in posts:
        if models.Submission.objects.filter(channel=channel, post_id=post.id).exists():
            continue
        return models.Submission.objects.create(
            channel=channel,
            post_id=post.id,
            title=post.title,
            url=post.url,
            subreddit=post.subreddit,
        )


def send_submission(submission: models.Submission):
    perma_link = f'https://reddit.com/r/{submission.subreddit}/comments/{submission.post_id}/'

    blocks = [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': f'*<{perma_link}|{submission.title}>*'}}]

    if 'jpg' in submission.url or 'png' in submission.url:
        blocks.append({'type': 'image', 'image_url': submission.url, 'alt_text': submission.url})

    blocks.append({'type': 'context', 'elements': [{'type': 'mrkdwn', 'text': f'/r/{submission.subreddit}'}]})

    settings.SLACK_CLIENT.chat_postMessage(
        channel=submission.channel.id,
        text='',
        as_user=False,
        blocks=blocks,
    )


def trigger_submissions():
    for channel_id in models.Subscription.objects.values_list('channel', flat=True).distinct():
        channel = models.Channel.objects.get(pk=channel_id)
        submission = get_submission(channel)
        if submission:
            send_submission(submission)