#!/usr/bin/python3

# 0fabris
# Programmino per ottenere storie e highlights dato un username pubblico (o privato seguito)
# 11/2020

#Import Librerie
import sys
import requests
import json
import datetime
import re
import os
from urllib.parse import urlencode


#Class IGMedia
class IGMedia:
    #Constructor
    def __init__(self,user, mySessionId):
        
        self.INSTA_URL = 'https://www.instagram.com'
        self.user = user
        self.headers = {
                'User-Agent':'Mozilla/5.0',
                'Accept':'*/*',
                'Host':self.INSTA_URL.split('//')[-1],
                'Cookie':"; ".join([
                    f"{k}={v}" for k,v in {
                        'sessionid': mySessionId,       
                    }.items()
                    ] + ['']
                )
            }
        print("username: %s" % user)
        self.uid = self._getUserID()
        print(self.uid)
        
        #check on what to save/show
        contents = 0
        if len(sys.argv) >= 3:
            try:
                contents = int(sys.argv[2])
            except:
                contents = 0

        if contents < 0 and contents > 2:
            contents = 0
            
        #creation of user folder
        if os.path.exists(user):
            print(f"{user} folder exists")
        else:
            print(f"creating {user} folder...")
            os.mkdir(user)
        print(f"opening {user} directory")
        os.chdir(user)

        #save stories
        try:
            if contents == 0 or contents == 2:
                fname = f"stories_{user}.txt"
                with open(fname,"w") as f:
                    for i in self._StorieQuery([str(self.uid)],[])["data"]["reels_media"][0]["items"]:
                        f.write(datetime.datetime.fromtimestamp(int(i["taken_at_timestamp"])).strftime("%d/%m/%Y %H:%M:%S") + " -> ")
                        url = i["video_resources" if "video_resources" in i.keys() else "display_resources"][-1]["src"]
                        fformat = re.findall(r".*?/.*(\..*)\?",url)[0]
                        f.write(url+"\n")
                        self.download(fname[:-4]+ f'_{i["taken_at_timestamp"]}{fformat}',url)
        except:
            print("Error getting stories")

        try:
        #save highlights
            if contents == 1 or contents == 2:
                for reel in self._getHighlights()["data"]["user"]["edge_highlight_reels"]["edges"]:
                    fname = "highlights_{u}_{rn}.txt".format(u=user,rn=reel["node"]["title"])
                    with open(fname,"w") as f:
                        hg = self._StorieQuery([],[str(reel["node"]["id"])])
                        for i in hg["data"]["reels_media"][0]["items"]:
                            url = i["video_resources" if "video_resources" in i.keys() else "display_resources"][-1]["src"]
                            fformat = re.findall(r".*?/.*(\..*)\?",url)[0]
                            f.write(url+"\n")
                            self.download(fname[:-4]+ f'_{i["taken_at_timestamp"]}{fformat}',url)
        except:
            print("Error getting Highlights")
    
    #Download file given filename and url
    def download(self,name,url):
        if not os.path.exists(name):
            with open(name,"wb") as f:
                r = requests.get(url,headers=self.headers)
                f.write(r.content)
            print(f"downloaded file {name}")
        else:
            print(f"already downloaded file {name}")

    #Private method to get the userId from the username
    def _getUserID(self):
        r = requests.get(
                self.INSTA_URL+'/'+self.user+'/?__a=1',
                headers=self.headers
            )
        return r.json()['graphql']['user']['id']
   
    #Get all infos of the valid stories or highlights
    #same query for stories and highlights, so pass ([userids],[]) or ([],[highlightids])
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
                headers=self.headers
            )
        ##Debug - Show what the response look like
        #with open(f"{self.user}_response.json", "w") as f:
        #    json.dump(r.json(),f)
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
                headers=self.headers
            )
        return r.json()


#
#   Main
#
if __name__ == '__main__':
    fname = "ig_session_id.json"

    if len(sys.argv) >= 2 and len(sys.argv) < 4:
        #check session id
        if not os.path.exists(fname):
            with open(fname,"w") as f:
                json.dump({
                    'session_id':''
                },f)
                exit(f"please fill \"{fname}\" with your sessionid cookie")
        else:
            with open(fname,"r") as f:
                arr = json.load(f)
                if "session_id" not in arr.keys() or arr["session_id"] == "":
                    exit("\"session_id\" field not found")

        #if all ok grab what user asked
        igs = IGMedia(sys.argv[1], arr["session_id"])
    else:
        print("Utilizzo: ./" + sys.argv[0] + " nomeutente [0=stories, 1=highlights, 2=both]")
