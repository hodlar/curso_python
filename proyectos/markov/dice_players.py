import numpy as np

class Dado:
    
    def __init__(self, n):
        self.size = n
    
    def lanzamiento(self):
        return np.random.randint(1, self.size+1)
    
    def get_size(self):
        return self.size

class mlplayer:
    
    def __init__(self, dado_obj, actions, turns):
        self.dado = dado_obj
        self.size = dado_obj.get_size()
        self.turns = turns
        self.actions = len(actions)
        self.m = np.zeros([self.size * (self.turns), self.actions])
        self.t = np.zeros([self.size * (self.turns), self.actions])
        self.plays = 0
        self.toss = 0
        self.epsilon = 0.5
        self.TotalReward = 0
        self.avg_reward = 0
        self.learn = True
        self.full_history = []
    
    def get_m(self):
        return self.m
    
    def start(self):
        self.ing = True
        self.toss = 0
        self.reward = 0
        self.history = []
        
    def stop(self):
        self.ing = False
        
    def play_n(self, n):
        for i in range(n):
            self.start()
            while self.ing:
                self.play()
        print (f'All games have ended')
        #return self.m
        
    def play(self):
        r = self.dado.lanzamiento()
        self.reward = r
        self.state = (self.toss*self.size + r) - 1 # -1 for array indexing
        self.toss = self.toss + 1
        
        a = int(self.choose())
        #print (f'action: {a} on reward {r} in toss {self.toss} over game {self.plays}')
        self.history.append([self.state, a])
        self.t[self.state, a] = self.t[self.state, a] + 1
        
        # 1: continue
        if a == 1:
            pass
        # 0: Stop 
        elif a == 0:
            n = self.plays
            self.plays = n + 1 
            self.TotalReward = self.TotalReward + self.reward
            self.full_history.append(self.reward)
            self.avg_reward = self.avg_reward * (n / (n + 1) )  + r / (n + 1)
            if self.learn:
                self.update()
            self.stop()
            
    def update(self):
        r = self.reward
        for s, a in self.history:
            t = self.t[s, a]
            self.m[s, a] = (self.m[s, a] * (t-1) + r)/(t)
        self.give_me_epsilon()
        
    def choose(self):
        if self.toss == self.turns:
            return 0
        else:
            if np.random.rand() < self.epsilon:
                return np.random.randint(self.actions)
            return self.m[self.state].argmax()
        
    def give_me_epsilon(self):
        e = max(0.05, self.epsilon/self.plays)
        self.epsilon = (e + self.epsilon)/2.0
        
    def consolidate(self):
        self.epsilon = 0.0
        self.stop_learning()
        
    def deconsolidate(self, e):
        self.epsilon = e
        
    def clone(self, P):
        self.m = P.get_m()
        self.epsilon = P.epsilon
        
    def start_learning(self):
        self.learn = True
        
    def stop_learning(self):
        self.learn = False
        
        
        
# Create a deterministic player
class dplayer:
    def __init__(self, dado_obj, actions, turns):
        self.dado = dado_obj
        self.actions = len(actions)
        self.turns = turns
        self.toss = 0
        self.plays = 0
        self.reward = 0
        self.TotalReward = 0
        self.avg_reward = 0
        self.ing = False
        self.full_history = []
    
    def stop(self):
        self.ing = False
        
    def start(self):
        self.toss = 0
        self.ing = True
    
    def play(self):
        r = self.dado.lanzamiento()
        self.reward = r
        self.toss += 1
        c = self.choose()
        
        if c == 1:
            pass
        elif c == 0:
            n = self.plays
            self.TotalReward += r
            self.full_history.append(self.reward)
            self.plays = n + 1 
            self.avg_reward = self.avg_reward * (n / (n + 1) )  + r / (n + 1)
            self.stop()
        
    def play_n(self, n):
        for i in range(n):
            self.start()
            while self.ing:
                self.play()
        print (f'All games have ended')
        #return self.m
        
    def choose(self):
        if self.toss == 1:
            if self.reward <= 4:
                # Continue
                return 1
            # Stop
            return 0
        elif self.toss == 2:
            if self.reward <= 3:
                # Continue
                return 1
            # Stop
            return 0
        elif self.toss == 3:
            # Stop
            return 0
        return 0