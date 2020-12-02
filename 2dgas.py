# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:42:59 2020
Microscopic simulaiton of a 2d ideal gas in a fixed volume box.

The class swarm is composed by particle objects. 
It has a interaction functions that iterates through particle pairs
checks for collisions and updates velocities

ISSUES:
    - slow rendering (matplotlib bottleneck) 
    - parallelization for collision check could help

https://gist.github.com/schirrecker/982847faeea703dd6f1dd8a09eab13aa
https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
@author: AB

"""

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import matplotlib.animation as animation
import itertools

class Particle:
    
    def __init__(self,mass=1,radius=1,v=False): 
        """
        :param xy: Initial position.
        :param v: Initial velocity.
        """
        self.xy=np.array([rnd.uniform(0,size),rnd.uniform(0,size)])
        if v==False:
            self.v=np.array([rnd.uniform(-0.5,0.5),rnd.uniform(-0.5,0.5)])
        else:
            self.v=v
        # self.v=np.array([0.5,0.5])
        self.mass=mass
        self.radius=radius
     #   self.radius=mass #if the density is assumed constant
      
        # circle = plt.Circle(self.xy, self.radius, color='blue')
        # self.scatter,=circle
    @property
    def energy(self):
        return 0.5*np.linalg.norm(self.v)**2*self.mass
    @property
    def vel(self):
        return np.linalg.norm(self.v)
        
    @classmethod    
    def create_swarm(cls,n,fix_mass=True,fix_radius=True, only_one_fast=False, all_right=False ): 
        """
        generates a list particles 
        
        if fix_mass is True -> mass=1 by default
        if fix_radius is True -> radius=1 by default
        
        """
        swarm=[]
        for i in range(n):
            if fix_mass and fix_radius:
                swarm.append(Particle()) 
            elif fix_mass:
                swarm.append(Particle(radius=rnd.uniform(1,max_radius))) 
            elif fix_radius:
                swarm.append(Particle(mass=rnd.uniform((1,max_mass))))
        if only_one_fast:
            for i in range(n):
                if i==0:
                    swarm[i].v=np.array([10.,10.])
                else:
                    swarm[i].v=np.array([.0,.0])
        if only_one_fast: #ignored if onlyonefast is true
            pass
        elif all_right:
            for i in range(n):
                swarm[i].v=np.array([1.,.0])
        
        return swarm
    
    def pop(self):
           return plt.Circle(tuple(self.xy), self.radius)
    @staticmethod   
    def dist(ball1,ball2):
        dist=np.linalg.norm(ball1.xy-ball2.xy)
        return dist
    
    @staticmethod
    def collision(ball1,ball2): 
        r12=ball1.xy-ball2.xy
        v12=-ball1.v+ball2.v
        r_vers=r12/np.linalg.norm(r12)
        v_vers=v12/np.linalg.norm(v12)
        if  np.dot(v_vers,r_vers)<0: 
            #if particles are merged pass
            #avoidss initialization issues
            pass
        else:
            #exchanged momentum q
            #collision solved in the frame of reference of ball2     
            q=-cor*2*(ball1.mass*ball2.mass)/(ball1.mass+ball2.mass)*(np.dot(-v12,r_vers))*r_vers 
            ball1.v+=q/ball1.mass
            ball2.v-=q/ball2.mass
                                                                 
           
    def update(self):
        if self.xy[0] <= xlim[0]+self.radius:
            # hit the left wall, reflect x component
            self.v[0] = cor * np.abs(self.v[0])
        elif self.xy[0] >= xlim[1]-self.radius:
            self.v[0] = - cor * np.abs(self.v[0])
        if self.xy[1] <= ylim[0]+self.radius:
            # hit the left wall, reflect y component
            self.v[1] = cor * np.abs(self.v[1])
        elif self.xy[1] >= ylim[1]-self.radius:
            self.v[1] = - cor * np.abs(self.v[1])

        # delta t is 0.1
        delta_v = delta_t * ag
        self.v += delta_v

        self.xy += self.v

        self.xy[0] = np.clip(self.xy[0], xlim[0]+self.radius, xlim[1]-self.radius)
        self.xy[1] = np.clip(self.xy[1], ylim[0]+self.radius, ylim[1]-self.radius)

        self.pop()
        

def init(): 

    velocities=np.array([])
    energies=np.array([])
    
    for ball in balls:
        velocities=np.append(velocities,ball.energy)
        energies=np.append(energies,ball.energy)
    axs[2].hist(energies)
    axs[1].hist(velocities)
  
    return []


def animate(t):
      # t is time in seconds
    
    velocities=energies=np.array([])
    for ball in balls:
        ball.update()
        velocities=np.append(velocities,ball.vel)
        energies=np.append(energies,ball.energy)

    for ball1, ball2 in itertools.combinations(balls,2): 
        if Particle.dist(ball1,ball2)<ball1.radius+ball2.radius: #check for collision only if contact
            Particle.collision(ball1, ball2)
        else:
            pass 
    axs[0].clear()
    plt.sca(axs[0])
    plt.xticks([],[])
    plt.yticks([],[])
    axs[0].set_xlim(xlim)
    axs[0].set_ylim(ylim)
    axs[2].cla()
    axs[1].cla()
    axs[1].hist(energies,bins=int(n_particles/3),density=True)
    axs[2].hist(velocities,bins=int(n_particles/3),density=True)
    axs[2].set_xlabel("Speed")
    axs[1].set_xlabel("Energy")

    [axs[0].add_patch(ball.pop()) for ball in balls] 


if __name__ == "__main__":
    ###setting the experiment
    n_particles=300
    g = 0 #gravity
    ag = np.array((0,-g))
    cor = 1 # coefficient of restitution (ratio of velocity after and before bounce)
    size=150 #box size
    
    max_mass=1
    max_radius=5
    # bounds of the box
    xlim = (0,size)
    ylim = (0,size)
    
    delta_t = 0.001   # 1 millisecond delta t
    
    fig , axs= plt.subplots(3,1)
    fig.set_dpi(100)
    fig.set_size_inches(7,21)
    
    plt.sca(axs[0])
    plt.xticks([],[])
    plt.yticks([],[])
    axs[0].set_xlim(xlim)
    axs[0].set_ylim(ylim)
    
    balls = Particle.create_swarm(n_particles,all_right=True )
    ani = animation.FuncAnimation(fig, animate, frames=np.arange(0,1,delta_t), 
                                  init_func=init, blit=False,repeat=False)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('allright_2.mp4', writer=writer)

    plt.show()
