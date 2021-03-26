import json
xpgain=10
def xps(level):
    return 10*level*level+100
class levels:
    try:
            dict=json.load(open('levels.json','r'))
    except:
            dict={}

    def __init__(self,user,xp, level):
        self.user=user
        self.xp=xp
        self.level=level
        
    
    def gain(self):
        self.xp+=xpgain
        return self
    def fromdict(self):
        
        return levels(self.user, levels.dict[str(self.user)][0], levels.dict[str(self.user)][1])
    def save(self):
        levels.dict.update({str(self.user): [self.xp, self.level]})
        print(levels.dict)
        with open('levels.json', 'w') as f:
            json.dump(levels.dict,f)
        return self
    def setxp(self,val):
        self.xp=val
        self.save()
        return self
    def increaselvl(self,val):
        self.level+=1
        self.save()
        return self        



def update_xp(userid):
    if str(userid) in levels.dict:
        return levels(userid,0,0).fromdict().save()   
    else: 
        return levels(userid,0,0).save()
