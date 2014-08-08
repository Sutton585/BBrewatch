import praw
import time
import re

##-----------------------------------------------------------------------

number_posts_pull = 5 #How many posts do you want to return?
pull_subreddit = 'BigBrother'

reddit_username = 'caltoru'
reddit_password = 'xxx'
reddit_user_agent = 'BBrewatch_testing'

##-----------------------------------------------------------------------

def prepare_csv(text):
	text = re.sub('"',"'",text)
	text = re.sub('&amp;','&',text)
	text = re.sub('\n','*#*#*#*',text)
	text_out = '"' + text + '"'
	return text_out

r = praw.Reddit(user_agent=reddit_user_agent) ##Assign ourselves a user agent
r.login(reddit_username,reddit_password)

URL = 'http://www.reddit.com/r/' + pull_subreddit

##Gets number of posts up to "limit" in listed subreddit URL:
posts = list(r.get_content(URL, params=None, limit=number_posts_pull, place_holder=None, root_field='data', thing_field='children', after_field='after', _use_oauth=False, object_filter=None)) 

for post in posts: ##For each post in the subreddit (that was returned, apparently there is a limit to how many can be returned by API?)

	date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(post.created_utc))	##Time that the original post was created, converted from Unix epoch
	
	try:
		print '''
		Post Title: %s
		Post Score: %s
		Creation Date: %s
		Post Text: %s
		Post URL: %s
		''' % (post.title,post.score,date,post.selftext,post.url)
		
		post_title = prepare_csv(post.title)
		post_self_text = prepare_csv(post.selftext)
		post_url = prepare_csv(post.url)
		post_text = prepare_csv(post.selftext)
				
		write_text = str(post_title) + ',' + str(post.score) + ',' + str(date) + ',' + str(post_text) + ',' + str(post_url) + '\n'
		
		with open("reddit_posts.txt", "a") as myfile:
			myfile.write(write_text)

	except:
		print '\n\n\n\n\nUnable to print a character in the post title. Should still be able to be saved though.\n\n\n\n\n'
		print post.url
