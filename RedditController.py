import requests
import json
import praw

with open('config.json') as config_file:
    config = json.load(config_file)

class RedditControler:
    def __init__(self):
        self.reddit = praw.Reddit(client_id=config["reddit"]["client_id"],
                             client_secret=config["reddit"]["client_secret"],
                             user_agent=config["reddit"]["user_agent"])
        # set(nltk.corpus.stopwords.words('english'))
        pass

    def get_posts(self):
        url = config["reddit"]["subreddit"]
        response = requests.get(url, headers={'User-agent': config["reddit"]["user_agent"]})
        print(response)
        if not response.ok:
            print('Error',  response)
        else:
            self.download_image(response)

    def download_image(self, response):
        # array of posts in the page
        data = response.json()['data']['children']

        # get post 5 from array of posts
        post = data[5]['data']
        author = post['author_fullname']
        title = post['title']
        file_name = post['id']
        print(file_name,author,title)
        image_url = post['url']
        if '.jpg' in image_url or '.jpeg' in image_url:
            image = requests.get(image_url)
            if (image.status_code == 200):
                # check if we already have this image
                try:
                    output_filehandle = open("./memes/" + file_name + ".jpeg", mode='bx')
                    output_filehandle.write(image.content)
                except FileExistsError:
                    print("File already exisits, retrying...")


p = RedditControler()
p.get_posts()
