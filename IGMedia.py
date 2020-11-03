#!/usr/bin/python3
#import the libraries
import sys
import requests
import json
from urllib.parse import urlencode

# IGMedia script
# 0fabris
# 11/2020
# Get the stories and highlights of given username
# REQUIRES => sessionid cookie of valid instagram session

class IGMedia:
    def __init__(self,user):
        
        #set constants
        self.INSTA_URL = 'https://instagram.com'
        self.cookies = "; ".join([
            f"{k}={v}" for k,v in {
                    'sessionid': '%your_sessionid_cookie%',                
                }.items()    
            ]+[''] # to add ; at the end of the cookie row
        )
        print(self.cookies)

        #set user
        self.user = user
        print("username: %s" % user)

        #getting user_id
        self.uid = self._getUserID()
        print("user_id: %s" % self.uid)
        
    #function that gets user_id of given username
    def _getUserID(self):
        r = requests.get(
                self.INSTA_URL+'/'+self.user+'/?__a=1'
            )
        return r.json()['graphql']['user']['id']
   
    #same query for stories and highlights, so pass reel_ids = userids, or highlights ids
    def _StorieQuery(self,rids,hids):
        print(f"requesting {str(rids)}, {str(hids)}")
        url = f'{self.INSTA_URL}/graphql/query/?' + urlencode({
                    'query_hash':'c9c56db64beb4c9dea2d17740d0259d9',
                    'variables':json.dumps({
                        'reel_ids':rids,
                        'tag_names':[],
                        'location_ids':[],
                        'highlight_reel_ids':hids,
                        'precomposed_overlay':False,
                        'show_story_viewer_list':True,
                        'story_viewer_fetch_count':50,
                        'story_viewer_cursor':'',
                        'stories_video_dash_manifest':False
                    }
                )
                }
            )
        r = requests.get(
                url,
                headers={
                    'User-Agent':'Mozilla/5.0',
                    'Accept':'*/*',
                    'Host':'www.instagram.com',
                    'Cookie':self.cookies,
                }
            )
        return r.json()

    #get highlights from given userid
    def _getHighlights(self):
        url = f'{self.INSTA_URL}/graphql/query/?' + urlencode({
                    'query_hash':'d4d88dc1500312af6f937f7b804c68c3',
                    'variables':json.dumps({
                        'user_id':str(self.uid),
                        'include_chaining':False,
                        'include_reel':True,
                        'include_suggested_users':False,
                        'include_logged_out_extras' : True,
                        'include_highlight_reels':True,
                        'include_live_status':True,
                    }
                )
                }
            )
        r = requests.get(
                url,
                headers={
                    'User-Agent':'Mozilla/5.0',
                    'Accept':'*/*',
                    'Host':'www.instagram.com',
                    'Cookie':self.cookies,
                }
            )
        return r.json()

    #open a file stories_username.txt and save every story url on a row
    def saveStories(self):
        with open("stories_" + self.user + ".txt","w") as f:
            for i in self._StorieQuery([str(self.uid)],[])["data"]["reels_media"][0]["items"]:
                if "video_resources" in i.keys():
                    f.write(i["video_resources"][-1]["src"]+"\n")
                else:
                    f.write(i["display_resources"][-1]["src"]+"\n")
    
    #opens a file for every highlight and saves urls as saveStories does
    def saveHighlights(self):
        for reel in self._getHighlights()["data"]["user"]["edge_highlight_reels"]["edges"]:
            with open("highlights_%s_%s.txt" % (self.user,reel["node"]["title"]),"w") as f:
                hg = self._StorieQuery([],[str(reel["node"]["id"])])
                for i in hg["data"]["reels_media"][0]["items"]:
                    if "video_resources" in i.keys():
                        f.write(i["video_resources"][-1]["src"]+"\n")
                    else:
                        f.write(i["display_resources"][-1]["src"]+"\n")

if __name__ == '__main__':
    if len(sys.argv) >= 2 and len(sys.argv) < 4:
        #object
        igs = IGMedia(sys.argv[1])

        #check on what to save/show
        contents = 0
        if len(sys.argv) >= 3:
            try:
                contents = int(sys.argv[2])
            except:
                contents = 0

        if contents < 0 and contents > 2:
            contents = 0

        #save stories
        if contents == 0 or contents == 2:
            try:
                igs.saveStories()
                print("saveStories ok")
            except:
                print("Error getting stories!")

        #save highlights
        if contents == 1 or contents == 2:
            try:
                igs.saveHighlights()
                print("saveHighlights ok")
            except:
                print("Error getting Highlights!")
    else:
        print("Usage: "+sys.argv[0]+" username [0=stories, 1=highlights, 2=both]")
