import instaloader
import pandas as pd
from IPython.display import clear_output
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import datetime

class Niche():
    """This class creates a bot for istagram
    """    

    def __init__(self):
        """Init method of the class
        """
        #other attributs
        self.hash_df = pd.DataFrame(columns = ['name', 'id', 'hashtag', 'mediacount', 'group', 'top_posts', 'related_hash'])
        self.df = pd.DataFrame(columns = ['hashtag', 'owner', 'post'])
        self.L = instaloader.Instaloader()
        self.L.login("testdeidilio", "test12345678")
        self.discarded_list = pd.Series() #a list with all the discarded hashtags on the process
        #groups
        self.small = False
        self.medium = False
        self.big = False
        self.strategy = []
    
    def hashtags_search(self, size, key_words):
        """
           This function scratch for "size" hashtags related with the given niche

           Arguments:
               key_words {list} -- [the key_words of the nich] 
        """
        #FIRST run time key_words are a list of strings, so convert to a list of hashtag!
        if len(self.hash_df)==0:
            key_words = [instaloader.Hashtag.from_name(self.L.context, x) for x in key_words]
            self.stairs(new_data = key_words, size = size)
            self.hashtags_search(size = size, key_words = key_words)            
            return
                  
            
        #second time and further            
        #this marker take the len of the df
        marker = len(self.hash_df)
        
        for n in key_words: #n is a hashtag object
            #check limits in each loop
            if len(self.hash_df) >= size:
                break            
            #get realated (max 10)            
            #get realated generator from df
            #print("----------------------------------------->{}".format(n)) #--debug
            related_gen = self.hash_df.related_hash[self.hash_df.hashtag == n] #Pick a Serie of one generator
            
            #convert to dict (hash, id)
            related = list(related_gen.iloc[0])
            #print("Related--{}".format(related)) #--debug

            #pick tested ones
            probados = pd.concat([self.hash_df.hashtag, self.discarded_list], ignore_index=True).tolist()            
            #print("probados--{}".format(probados)) #--debug
            
            #pick just the news (not in df, not in discarded)
            nuevos = list(set(related) - set(probados))         
            #print("nuevos--{}".format(nuevos)) #--debug

            #Stair strategies. Clasify
            if len(nuevos) < 0:
                continue
            self.stairs(new_data = nuevos, size = size)
        
        #Execute again while get size
        if len(self.hash_df) < size:
            discovered = self.hash_df.hashtag[marker:]           
            
            #print("discovered--{}".format(discovered)) #--debug
            self.hashtags_search(size = size, key_words = discovered)


    def stairs(self, new_data, size):
        """
            This function apply the stair strategie to a list of hashtags and divide them in 3 groups:
            group1 = 5k to 50k (50%) small
            group2 = 50k to 500k (30%) medium
            group3 = + 500k (20%) big
             Arguments:
            new_data {list} -- [list of related new hashtags]
        """        
        for x in new_data: # x is a single hashtag, new_data is a list of hashtag objects
            self.printstatus(x = x)
            mediacount = x.mediacount

            if not self.small and mediacount >= 5000 and mediacount <= 50000:
                #print('g1-{}'.format(x)) ---debug
                #append to dataFeame
                self.hash_df.loc[len(self.hash_df)] = [
                    x.name, x.hashtagid, x, mediacount, 
                    "small", list(x.get_top_posts()), 
                    list(x.get_related_tags())
                    ]
                #chek size
                if len(self.hash_df[self.hash_df.group == "small"]) >= size*0.5:
                    self.small = True

            elif not self.medium and mediacount > 50000 and mediacount <= 500000:
                #print('g2-{}'.format(x)) ---debug
                #append to dataFeame
                self.hash_df.loc[len(self.hash_df)] = [
                    x.name, x.hashtagid, x, mediacount, 
                    "medium", list(x.get_top_posts()), 
                    list(x.get_related_tags())
                    ]
                #chek size
                if len(self.hash_df[self.hash_df.group == "medium"]) >= size*0.3:
                    self.medium = True

            elif not self.big and mediacount > 500000:
                #print('g3-{}'.format(x)) ---debug
                #append to dataFeame
                self.hash_df.loc[len(self.hash_df)] = [
                    x.name, x.hashtagid, x, mediacount, 
                    "big", list(x.get_top_posts()), 
                    list(x.get_related_tags())
                    ]
                #chek size
                if len(self.hash_df[self.hash_df.group == "big"]) >= size*0.2:
                    self.big = True
             
            else:
               #create a discarted list in order to optimise
               self.discarded_list.loc[len(self.discarded_list)] = x          
            
            #check limits
            if self.hash_df.shape[0] >= size:
                self.printstatus(x = x)
                print("done")
                break
    def hashtags_search_by_top(self, size, keywords):
        #iterate keywords
        for h in keywords:
            h_class = instaloader.Hashtag.from_name(self.L.context, h)
            top_post_gen = h_class.get_top_posts()
            for post in top_post_gen:
                post.get_           
            h.get_top_posts() 
    
    #def chek_top_status():
        #if self.strategy:
    
    def write_strategy(self, number):
        #divide
        rang1 = self.hash_df.name[self.hash_df["group"] == "small"]
        rang2 = self.hash_df.name[self.hash_df["group"] == "medium"]
        rang3 = self.hash_df.name[self.hash_df["group"] == "big"]
        #get samples
        self.strategy = (rang1.sample(round(number*0.5)).tolist() + rang2.sample(round(number*0.3)).tolist() + rang3.sample(round(number*0.2)).tolist())
        #self.strategy.append("idiliodigital")
        print(self.strategy)

        with open('strategy_list.txt', 'w', encoding='utf-8') as f:
            f.truncate(0)
            for item in self.strategy:
                f.write("#%s," % item)
        return self.strategy
    
    def printstatus(self, x):
        df_count = self.hash_df.groupby("group").count()["name"]
        df_count.name = None
        clear_output()
        print("analizing---> {}".format(x.name)) #--debug
        print("*****Status*****")
        #print(df_count)
        if len(df_count)>0:
            print('Big-----', df_count.values[0])
        if len(df_count)>1:
            print('Medium--', df_count.values[1])
        if len(df_count)>2:
            print('Small---', df_count.values[2])
        
        print("__________")
        print("funded --> {}".format(self.hash_df.shape[0]))
        #print("descartados---> {}".format(self.discarded_list)) --debug
        print("__________")
        print(self.hash_df.name.tolist())