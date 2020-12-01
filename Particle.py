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
