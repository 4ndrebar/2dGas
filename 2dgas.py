# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:42:59 2020
Microscopic simulaiton of ideal gas.

The class swarm is composed by particle objects. It has a interaction functions that iterates through the particles
then checks for collisions and updates velocities
https://gist.github.com/schirrecker/982847faeea703dd6f1dd8a09eab13aa
https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
@author: Andrea

TODO: 
    fix initialization issue
    multiple collisions
    
DONE:
    sling issue, acceleration
    merging issue-->seems fixed
    fix size-radius proportions
"""

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import matplotlib.animation as animation
import itertools

class Particle:
    
    def __init__(self,mass=1,radius=1): 
        """
        :param xy: Initial position.
        :param v: Initial velocity.
        """
        self.xy=np.array([rnd.uniform(0,size),rnd.uniform(0,size)])
        self.v=np.array([rnd.uniform(-0.5,0.5),rnd.uniform(-0.5,0.5)])
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
    def create_swarm(cls,n): 
        """
        generates a list particles 
        """
        swarm=[]
        for i in range(n):
            if density_constant==1:
                swarm.append(Particle(rnd.uniform(1,max_mass),rnd.uniform(1,max_radius))) 
            else:
                swarm.append(Particle(rnd.uniform(1,max_mass),rnd.uniform(1,max_radius))) 
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
            #prevents merging
            pass
        else:
            q=-cor*2*(ball1.mass*ball2.mass)/(ball1.mass+ball2.mass)*(np.dot(-v12,r_vers))*r_vers #collision solved in the frame of reference of ball2     
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
    axs[2].plot(x)
    axs[2].hist(energies)
    axs[1].hist(velocities)
    return []


def animate(t):
      # t is time in seconds
   # global xy, v
    velocities=energies=np.array([])
    for ball in balls:
        ball.update()
        velocities=np.append(velocities,ball.vel)
        energies=np.append(energies,ball.energy)
        total_energy=np.sum(energies)

    for ball1, ball2 in itertools.combinations(balls,2): #mettere questo ciclo if qui velocizza la simulazione
        if Particle.dist(ball1,ball2)<ball1.radius+ball2.radius:
            Particle.collision(ball1, ball2)
        else:
            pass 
    axs[0].clear()
    # plt.sca(axs[0])
    # plt.xticks([],[])
    # plt.yticks([],[])
    axs[0].set_xlim(xlim)
    axs[0].set_ylim(ylim)
    axs[2].cla()
    axs[1].cla()
    axs[1].plot(x,n_particles/(2*total_energy)*np.exp(-x*total_energy)) #verificare la relazione
    axs[1].hist(energies,bins=n_particles)
    axs[2].hist(velocities,bins=n_particles)
    axs[2].plot(x,2*n_particles/total_energy*x*np.exp(-total_energy*x**2/2)) #verificare la relazione

    [axs[0].add_patch(ball.pop()) for ball in balls] 
   # return patches
  #  return axs[1].hist(velocities)

if __name__ == "__main__":
    n_particles=20 
    g = 0
    ag = np.array((0,-g))
    # coefficient of restitution (ratio of velocity after and before bounce)
    cor = 1
    size=100 #box size
    
    density_constant=1
    max_mass=1
    max_radius=5
    # bounds of the box
    xlim = (0,size)
    ylim = (0,size)
    
    # 1 millisecond delta t
    delta_t = 0.001
    
    fig , axs= plt.subplots(3,1)
    fig.set_dpi(100)
    fig.set_size_inches(7,21)
    
    plt.sca(axs[0])
    plt.xticks([],[])
    plt.yticks([],[])
    axs[0].set_xlim(xlim)
    axs[0].set_ylim(ylim)
    global x
    x=np.linspace(0., 1, 50)
    
    balls = Particle.create_swarm(n_particles)
    ani = animation.FuncAnimation(fig, animate, np.arange(0,100,delta_t), 
                                  init_func=init, interval=10, blit=False)

    plt.show()
