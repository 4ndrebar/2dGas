# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:42:59 2020
Microscopic simulaiton of ideal gas.

The class swarm is composed by particle objects. It has a interaction functions that iterates through the particles
then checks for collisions and updates velocities
https://gist.github.com/schirrecker/982847faeea703dd6f1dd8a09eab13aa
https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
@author: Andrea
"""

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import matplotlib.animation as animation
import itertools
from Particle import *

       
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
