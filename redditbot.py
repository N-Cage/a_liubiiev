import praw
reddit = praw.Reddit(client_id='IZbMt4yWOAg3Gbq9aC18zA', client_secret='6_LN2oQBqB10Gb115WIhcZAUXWq6Hg',
                             password='14nigger88', user_agent='Repost indentifying bot 0.0.1 by u/GooseConscious7501', 
                             username='GooseConscious7501')

reddit.validate_on_submit = True

'''
1. crawl r/all & r/popular for posts 
2. check if there are any multimedia files
    2a. if ture --> extract data --> google img search with site:reddit.com tag
    2b. if false --> extract text --> google serach with site:reddit.com tag
3. if results are >= 1 
4. check if it is the post that is bieng analized
5. compare timestamps 
6. count reposts and collect urls
7. form the answer and post it as a new comment
'''
 