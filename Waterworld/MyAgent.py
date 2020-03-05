import numpy as np
from ple import PLE

from ple.games.waterworld import WaterWorld
import time
import math

class SmartAgent():
    def __init__(self,actions):
        self.actions = actions #d,r,u,l 
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.target_x =  0.0
        self.target_y =  0.0
        self.target_index_x =  0
        self.target_index_y =  1

    def pickAction(self, reward, obs):
        self.x_pos = obs[0]
        self.y_pos = obs[1]
        self.x_vel = obs[2]
        self.y_vel = obs[3] 
        self.target_x =  obs[self.target_index_x+4]
        self.target_y =  obs[self.target_index_y+4]
        if reward < 0.0:
            self.target_index_x += 6 
            self.target_index_x = self.target_index_x%18
            self.target_index_y += 6
            self.target_index_y = self.target_index_y%18
        dist = [0.0,0.0,0.0,0.0,0.0]
        x1 = self.x_pos+self.x_vel*0.975
        if x1 > 192.0:
            x1 = 192.0
        elif x1 < 0.0:
            x1 = 0.0
        x2 = self.x_pos+(self.x_vel+1.65)*0.975
        if x2 > 192.0:
            x2 = 192.0
        elif x2 < 0.0:
            x2 = 0.0
        x3 = self.x_pos+(self.x_vel-1.65)*0.975
        if x3 > 192.0:
            x3 = 192.0
        elif x3 < 0.0:
            x3 = 0.0
        y1 = self.y_pos+self.y_vel*0.975
        if y1 > 192.0:
            y1 = 192.0
        elif y1 < 0.0:
            y1 = 0.0
        y2 = self.y_pos+(self.y_vel+1.65)*0.975
        if y2 > 192.0:
            y2 = 192.0
        elif y2 < 0.0:
            y2 = 0.0
        y3 = self.y_pos+(self.y_vel-1.65)*0.975
        if y3 > 192.0:
            y3 = 192.0
        elif y3 < 0.0:
            y3 = 0.0
        dist[0] = math.sqrt((x1-self.target_x)**2+(y2-self.target_y)**2)
        dist[1] = math.sqrt((x2-self.target_x)**2+(y1-self.target_y)**2)
        dist[2] = math.sqrt((x1-self.target_x)**2+(y3-self.target_y)**2)
        dist[3] = math.sqrt((x3-self.target_x)**2+(y1-self.target_y)**2)
        dist[4] = math.sqrt((x1-self.target_x)**2+(y1-self.target_y)**2)
        
        m = float('inf')
        index = 0
        for i in range(5):
            if dist[i] < m:
                m = dist[i]
                index = i
        
        return self.actions[index]
    
def nv_state_preprocessor(state):

    colors = ['G','R','Y']
    val = state.values()
    x_pos = state['player_x']
    state['player_x'] = x_pos
    y_pos = state['player_y']
    state['player_y'] = y_pos
    x_vel = state['player_velocity_x']*0.033
    state['player_velocity_x'] = x_vel
    y_vel = state['player_velocity_y']*0.033
    state['player_velocity_y'] = y_vel
    tmp = state['creep_pos']
    all_pos = np.array([])
    for color in colors:
        for position in tmp[color]:
            k = np.array(position)
            all_pos = np.append(all_pos,k)
    all_state = np.append([x_pos,y_pos,x_vel,y_vel],all_pos)
    return all_state.flatten()

###################################


# Don't display window.
# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# create our game
force_fps = True  # slower speed
display_screen = True 
state_preprocessor = nv_state_preprocessor
reward = 0.0
game = WaterWorld()

# make a PLE instance.
p = PLE(game,force_fps=force_fps,display_screen=display_screen,state_preprocessor=state_preprocessor)

# our Naive agent!
agent = SmartAgent(actions = p.getActionSet())

# init agent and game.
p.init()

# start our loop
score = 0.0
for i in range(10):
    # if the game is over
    if p.game_over():
        p.reset_game()
    while p.game_over() == False:
        obs = p.getGameState()
        action = agent.pickAction(reward, obs)
        reward = p.act(action) # reward after an action
    score = game.getScore()
    print "Trial no.{:02d} : score {:0.3f}".format(i,score)

# Screen Shot
#     p.saveScreen("screen_capture.png")
