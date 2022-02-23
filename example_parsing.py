import textwrap
from typing import List

from parser import *


def print_author(author: Author):
    print(f"""
name: {author.name}
url: {author.url}
avatar: {author.avatar}
platform: {author.platform}
id: {author.id}
    """.strip())


def print_posts(posts: List[Post]):
    for i in range(len(posts)):
        post = posts[i]
        print(f"""
№{i+1}
author: {post.author}
image: {post.image}
title: {post.title}
description: {post.description}
url: {post.url}
        """.strip())


if __name__ == "__main__":
    print_author(DeviantartParser.get_author("yuumei"))
    # print_posts(DeviantartParser.get_posts("yuumei", 0))
    print_author(PixivParser.get_author("12064216"))
    print_posts(PixivParser.get_posts("12064216", 0))
