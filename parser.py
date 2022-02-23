import json

import requests
from bs4 import BeautifulSoup as bs4


class Image:
    def __init__(self, **kwargs):
        self.url = None if 'url' not in kwargs else kwargs['url']
        self.format = "" if 'url' not in kwargs else kwargs['format']

    def download(self, filename="image"):
        r = requests.get(self.url)

        if 200 <= r.status_code <= 209:
            with open(filename + "." + self.format, 'wb') as img:
                img.write(r.content)
        else:
            print(f"Error code: { r.status_code }")
            print(r.text)
            print(self.url)

    def __repr__(self):
        return f"<Image { self.url }>"


class Author:
    def __init__(self, **kwargs):
        self.name = None if 'name' not in kwargs else kwargs['name']
        self.url = None if 'url' not in kwargs else kwargs['url']
        self.avatar = None if 'avatar' not in kwargs else kwargs['avatar']
        self.platform = None if 'platform' not in kwargs else kwargs['platform']
        self.id = None if 'id' not in kwargs else kwargs['id']

    def __repr__(self):
        return f"<Author { self.name }>"


class Post:
    def __init__(self, **kwargs):
        self.author = kwargs['author']
        self.image = None if 'image' not in kwargs else kwargs['image']
        self.title = kwargs['title']
        self.description = kwargs['description']
        self.url = kwargs['url']

    def __repr__(self):
        return f"<Post image: { self.image }, author: { self.author }>"


class DeviantartParser:
    @staticmethod
    def load_image(post):
        return post.image

    @staticmethod
    def get_posts(username, page):
        offset = (page - 1) * 24
        limit = 24
        all_folder = "true"
        mode = "newest"
        r = requests.get(f"https://www.deviantart.com/_napi/da-user-profile/api/gallery/contents"
                         f"?username={username}"
                         f"&offset={offset}"
                         f"&limit={limit}"
                         f"&all_folder={all_folder}"
                         f"&mode={mode}")

        if 200 <= r.status_code <= 209:
            results = json.loads(r.text)['results']
            posts = []
            for result in results:
                if 'c' in list(filter(lambda tp: tp['t'] == "fullview", result['deviation']['media']['types']))[0]:
                    image_url = result['deviation']['media']['baseUri'] + '/' + \
                                list(filter(
                                    lambda tp: tp['t'] == "fullview",
                                    result['deviation']['media']['types']))[0]['c'] \
                                .replace("<prettyName>", result['deviation']['media']['prettyName']) + \
                                '?token=' + \
                                result['deviation']['media']['token'][0]
                else:
                    image_url = result['deviation']['media']['baseUri'] + \
                                '?token=' + result['deviation']['media']['token'][-1]

                posts.append(
                    Post(
                        author=Author(
                            name=result['deviation']['author']['username'],
                            url=f"https://www.deviantart.com/{ username }",
                            avatar=result['deviation']['author']['usericon'],
                            platform=DeviantartParser,
                            id=username),
                        image=Image(
                            url=image_url,
                            format=result['deviation']['media']['baseUri'].split('.')[-1]),

                        title=result['deviation']['title'],
                        description="",
                        url=result['deviation']['url']
                    )
                )
            return posts
        else:
            return None

    @staticmethod
    def get_author(username):
        offset = 1
        limit = 1
        all_folder = "true"
        mode = "newest"
        r = requests.get(f"https://www.deviantart.com/_napi/da-user-profile/api/gallery/contents"
                         f"?username={username}"
                         f"&offset={str(offset)}"
                         f"&limit={str(limit)}"
                         f"&all_folder={all_folder}"
                         f"&mode={mode}")

        if 200 <= r.status_code <= 209:
            results = json.loads(r.text)['results']
            if len(results) > 0:
                result = results[0]

                return Author(
                    name=result['deviation']['author']['username'],
                    url=f"https://www.deviantart.com/{ username }",
                    avatar=result['deviation']['author']['usericon'],
                    platform=DeviantartParser,
                    id=username)
            else:
                return None
        else:
            return None


'''
Artstation now has cloudflare
class ArtstationParser:
    @staticmethod
    def load_image(post):
        return post.image

    @staticmethod
    def get_posts(username, page):
        author = ArtstationParser.get_author(username)

        r = requests.get(f"https://www.artstation.com/users/{username}/projects.json?page={str(page)}")

        if 200 <= r.status_code <= 209:
            results = json.loads(r.text)['data']
            posts = []
            for result in results:
                chunks = result['cover']['thumb_url'].split('/')
                if len(chunks) == 12:
                    chunks[10] = 'large'
                else:
                    chunks[11] = 'large'
                    chunks = chunks[:10] + chunks[11:]

                image_url = "/".join(chunks)

                image = Image(
                    url=image_url,
                    format=result['cover']['thumb_url'].split('?')[-2].split('.')[-1])

                posts.append(
                    Post(
                        image=image,
                        author=author,
                        title=result['title'],
                        description=result['description'],
                        url=result['permalink']
                    )
                )
            return posts
        else:
            return None

    @staticmethod
    def get_author(username):
        r = requests.get(f"https://www.artstation.com/{username}")
        lines = r.text.split('\n')
        line_with_info = list(filter(lambda l: l.find("cache.put") != -1, lines))[0]
        info = line_with_info[line_with_info.find("{"):(line_with_info.rfind("}") + 1)].replace("\\", "")
        info = json.loads(info)

        return Author(
            name=info['full_name'],
            url=info['permalink'],
            avatar=info['large_avatar_url'],
            platform=ArtstationParser,
            id=username)
'''


class PixivParser:
    @staticmethod
    def load_image(post):
        r = requests.get(post.url)

        soup = bs4(r.text, 'html.parser')
        data = json.loads(soup.select('meta[name="preload-data"]')[0]['content'])

        image_url = data['illust'][post.url.split('/')[-1]]['urls']['regular']
        image = Image(
            url=image_url,
            format=image_url.split('.')[-1])

        post.image = image
        return post.image

    @staticmethod
    def get_posts(username, page):
        r = requests.get(f"https://www.pixiv.net/ajax/user/{username}/profile/top?lang=en")

        if 200 <= r.status_code <= 209:
            info = json.loads(r.text)

            if info['error']:
                print(info['message'])
                return None

            illusts = info['body']['illusts']

            post_id = list(illusts.keys())[0]

            author = Author(
                name=illusts[post_id]['userName'],
                url=f"https://www.pixiv.net/en/users/{username}",
                avatar=illusts[post_id]['profileImageUrl'],
                platform=PixivParser,
                id=username)

            posts = []
            for post_id in list(illusts.keys()):
                post_info = illusts[post_id]
                posts.append(Post(
                    author=author,
                    title=post_info['title'],
                    description=post_info['description'],
                    url=f"https://www.pixiv.net/en/artworks/{post_id}"))

            return posts
        else:
            print(f"Error: {r.text}")
            return None

    @staticmethod
    def get_author(username):
        r = requests.get(f"https://www.pixiv.net/ajax/user/{username}/profile/top?lang=en")

        if 200 <= r.status_code <= 209:
            info = json.loads(r.text)

            if info['error']:
                print(info['message'])
                return None

            illusts = info['body']['illusts']

            post_id = list(illusts.keys())[0]

            return Author(
                name=illusts[post_id]['userName'],
                url=f"https://www.pixiv.net/en/users/{username}",
                avatar=illusts[post_id]['profileImageUrl'],
                platform=PixivParser,
                id=username)
        else:
            print(f"Error: {r.text}")
            return None
