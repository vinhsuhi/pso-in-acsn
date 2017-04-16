import random
import math

total_sensors = 130 #
sensor_types = 3 #
number_sensors = [28,41,61] #
#min_number_sensors = 9
radius_sensors = [6.0,4.80,3.84] #
max_radius = 6.00
alpha = 0.9
WIDTH = 100.0 #
HEIGHT = 100.0 #
MAXGEN = 1000 #
w_first = 0.9
w_last = 0.4
c1 = 1.5
c2 = 1.5


Sensor = {'x':0,'y':0,'radius':0,'cell':0}
# Sensors la mot tap hop gom 130 Sensor duoc mo ta boi dict Sensor
Sensors = []
for i in range(0,total_sensors):
	Sensors.append(Sensor)  
Velocity = {'x':0,'y':0}	
# Velocitys la mot tap hop 130 cac velocity chi van toc gom 2 thanh phan van toc x va y
Velocitys = []
for i in range(0,total_sensors):
	Velocitys.append(Velocity)
# G_Pbest la 
G_Pbest = {'sensor':Sensors,'fitness':0} 
Individual = {'sensor':Sensors,'velocity':Velocitys,'fitness':0}

SIZE = 50
population = list(range(0,SIZE))
pbest = []
for i in range(0,SIZE):
	pbest.append(G_Pbest)
gbest = G_Pbest
gbest_copy = []
for i in range(0,SIZE):
	gbest_copy.append(G_Pbest)

def randomInitialization():
	i = 0
	idvd = Individual
	for type in range(0,sensor_types):
		for j in range(0,number_sensors[type]):
			idvd['sensor'][i]['x'] = random.uniform(radius_sensors[type], WIDTH - radius_sensors[type])
			idvd['sensor'][i]['y'] = random.uniform(radius_sensors[type], HEIGHT - radius_sensors[type])
			idvd['sensor'][i]['radius'] = radius_sensors[type]
			idvd['velocity'][i]['x'] = 0
			idvd['velocity'][i]['y'] = 0
			i += 1
# cac sensers co tam trung nhau phai loai bo
	for i in range(0,total_sensors):
		for j in range(0,total_sensors):
			if i==j:
				continue
			while (idvd['sensor'][i]['x'] == idvd['sensor'][j]['x']) and (idvd['sensor'][i]['y'] == idvd['sensor'][i]['y']):
				idvd['sensor'][i]['x'] = random.uniform(radius_sensors[type], WIDTH - radius_sensors[type])
	idvd = VFA(idvd)
	idvd['fitness'] = fitness_fn(idvd)
	return idvd

def VFA(idvd):
	for i in range(0,total_sensors):
		frx = 0
		fry = 0
		nr = 0
		for j in range(0,total_sensors):
			if i==j:
				continue
			dt = distance(idvd['sensor'][i],idvd['sensor'][j])
			sum_radius = idvd['sensor'][i]['radius'] + idvd['sensor'][j]['radius']
			if dt<sum_radius:
				frx += (1 - sum_radius/dt)*(idvd['sensor'][j]['x'] - idvd['sensor'][i]['x'])
				fry += (1 - sum_radius/dt)*(idvd['sensor'][j]['y'] - idvd['sensor'][i]['y'])
				nr += 1
		if nr!=0:
			idvd['sensor'][i]['x'] += frx/nr
			idvd['sensor'][i]['x'] += frx/nr
		idvd['sensor'][i]['x'] = round(idvd['sensor'][i]['x']*1000)/1000
		idvd['sensor'][i]['y'] = round(idvd['sensor'][i]['y']*1000)/1000
	idvd = standardlizeSensors(idvd)
	return idvd

def standardlizeSensors(idvd):
	for i in range(0,total_sensors):
		if idvd['sensor'][i]['x'] < idvd['sensor'][i]['radius']:
			idvd['sensor'][i]['x'] = idvd['sensor'][i]['radius']
		if idvd['sensor'][i]['y'] < idvd['sensor'][i]['radius']:
			idvd['sensor'][i]['y'] = idvd['sensor'][i]['radius']
		max_x = WIDTH - idvd['sensor'][i]['radius']
		max_y = HEIGHT - idvd['sensor'][i]['radius']
		if idvd['sensor'][i]['x'] > max_x:	idvd['sensor'][i]['x'] = max_x
		if idvd['sensor'][i]['y'] > max_y:	idvd['sensor'][i]['y'] = max_y
	return idvd

def initializePopulation():
	for i in range(0,SIZE):
		population[i] = randomInitialization()

def distance(x1,x2):
	x = x2['x'] - x1['x']
	y = x2['y'] - x1['y']
	return math.sqrt(x*x + y*y)

def overlap(s1,s2):
	ol = 0
	dt = distance(s1,s2)
	sum_radius = s1['radius'] + s2['radius']
	if dt >= sum_radius: return 0
	
	if (abs(s1['radius']-s2['radius']) <= dt) and (dt < sum_radius):
		gamme = sum_radius*min(s1['radius'],s2['radius']) / (max_radius*max(s1['radius'],s2['radius']))
		return gamme*(sum_radius-dt)
	beta = 2*max_radius + 0.1
	return beta*min(s1['radius'],s2['radius'])

def fitness_fn(idvd):
	olap = 0
	for i in range(0,total_sensors):
		for j in range(i+1,total_sensors):
			olap += overlap(idvd['sensor'][i],idvd['sensor'][j])

		barrier = [
					[idvd['sensor'][i]['x'],0],
					[idvd['sensor'][i]['x'],HEIGHT],
					[0, idvd['sensor'][i]['y']],
					[WIDTH, idvd['sensor'][i]['y']]
		]
		for j in range(0,4):
			dt = distance(idvd['sensor'][i],barrier[j])
			if dt < idvd['sensor']['radius']:
				olap += (idvd['sensor'][i]['radius'-dt])*idvd['sensor'][i]['radius']
	return olap

def Init_pbest():
	for i in range(0,SIZE):
		for j in range(0,total_sensors):
			pbest[i]['sensor'][j]['x'] = population[i]['sensor'][j]['x']
			pbest[i]['sensor'][j]['y'] = population[i]['sensor'][j]['y']
			pbest[i]['sensor'][j]['radius'] = population[i]['sensor'][j]['radius']
	pbest[i]['fitness'] = population[i]['fitness']

def Update_gbest():
	gbest = pbest[0]
	for i in range(1,SIZE):
		if gbest['fitness'] < pbest[i]['fitness']:	gbest = pbest[i]

def Update_UV(gen):
	w = (w_first - w_last) * (MAXGEN-gen) / MAXGEN + w_last
	r1 = random.uniform(0,1)
	r2 = random.uniform(0,1)
	while (r2==r1):
		r2 = random.uniform(0,1)
	for i in range (0,SIZE):
		for j in range (0,total_sensors):
			population[i]['velocity'][j]['x'] = w * population[i]['velocity']['x'] + c1 * r1 * (pbest[i]['sensor'][j]['x'] - population[i]['sensor'][j]['x']) + c2 * r2 * (gbest['sensor'][j]['x'] - population[i]['sensor'][j]['x'])
			population[i]['velocity'][j]['y'] = w * population[i]['velocity']['y'] + c1 * r1 * (pbest[i]['sensor'][j]['y'] - population[i]['sensor'][j]['y']) + c2 * r2 * (gbest['sensor'][j]['y'] - population[i]['sensor'][j]['y'])
		for j in range(0,total_sensors):
			population[i]['sensor'][j]['x'] += population[i]['velocity'][j]['x']
			population[i]['sensor'][j]['y'] += population[i]['velocity'][j]['y']
		population[i] = VFA(population[i])
		population[i]['fitness'] = fitness_fn(population[i])

def Update_pbest():
	for i in range(0,SIZE):
		if population[i]['fitness'] > pbest[i]['fitness']:
			pbest[i]['fitness'] = population[i]['fitness']
			for j in range(0,total_sensors):
				pbest[i]['sensor'][j]['x'] = population[i]['sensor'][j]['x']
				pbest[i]['sensor'][j]['y'] = population[i]['sensor'][j]['y']
				pbest[i]['sensor'][j]['radius'] = population[i]['sensor'][j]['radius']

def Print_gbest():
	print("olap: " + str(gbest['fitness']))

def Monte():
	L = 1000000
	coA = 0	
	point = []
	for i in range(0,L):
		point.append(Sensor)
		point[i]['x'] = random.uniform(0,WIDTH)
		point[i]['y'] = random.uniform(0,HEIGHT)
	for i in range(0,L):
		for j in range(0,total_sensors):
			if distance(point[i],gbest['sensor'][j]) <= gbest['sensor'][j]['radius']:
				coA += 1
				break
	return coA / L * WIDTH * HEIGHT

initializePopulation()
Init_pbest()
Update_gbest()
gen = 0
while(gen<MAXGEN):
	Update_UV(gen)
	Update_pbest()
	Update_gbest()
	Print_gbest()
	gen += 1
Print_gbest()
coA = Monte()
print("coA = " + str(coA))