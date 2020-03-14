import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import os



# ========================================================
# INPUt: p1 	[list] point coords x,y
#		 p2		[list] point coords x,y
# OOUTPUT:		Distance between p1 and p2
# ========================================================
def d2(p1, p2, d='e'):
	d0 = p1[0] - p2[0]
	d1 = p1[1] - p2[1]
	# Distancia euclideana
	if d == 'e':
		return np.sqrt((d0**2 + d1**2))
	# Distancia manhattan
	if d == 'm':
		return abs(d0) + abs(d1)
	# Chebyshev distance
	if d == 'c':
		return max(abs(d0), abs(d1))
	if d == 'r':
		return d2(p1, (p2+[0.1,0]), d='e')



# ========================================================
# DESCRIPTON: Finds the closes cluster of a point for
#			  KMeans grouping.
# INPUt: point 		[list] point coords x,y
#		 centers	[list] list of lists of cluster
#					centers (cx, cy)
# OOUTPUT:		the closes cluster to the point
# ========================================================
def get_cluster(point, centers):
	closest = 0
	dist = np.inf
	for i, c in enumerate(centers):
		thisd = d2(point, c) 
		if thisd < dist:
			closest = i
			dist = thisd
	return closest


# ========================================================
# DESCRIPTON: Finds the closes cluster of a point for
#			  KMeans grouping.
# INPUt: point 		[list] list of points point [x,y]
#		 centers	[list] list of lists of cluster
#					centers (cx, cy)
# OOUTPUT:		list of cluser per point.
# ========================================================
def fit(points, centers):
	km = []
	for point in points:
		k = get_cluster(point, centers)
		km.append(k)
	return km


# ========================================================
# DESCRIPTON: Update cluster centers coords
# INPUt: points 	[list] list of point [x,y]
#		 km 		[list] list of cluster index
#		 centers	[list] list of lists of cluster
#					centers (cx, cy)
# OOUTPUT:		[list] new cluster centers coords (x,y)
# ========================================================
def update_centers(points, km, centers):
	new_centers = np.zeros_like(centers)
	num_centers = len(centers)
	sumx = [0 for i in range(num_centers)]
	sumy = [0 for i in range(num_centers)]
	count = [0 for i in range(num_centers)]
	for k, point in zip(km, points):
		sumx[k] += point[0]
		sumy[k] += point[1]
		count[k] += 1
	for c in range(num_centers):
		if count[c] > 0:
			new_centers[c,0] = sumx[c]/count[c]
			new_centers[c,1] = sumy[c]/count[c]
		else:
			new_centers[c] = np.random.uniform(0,1,2)
	return new_centers



# ========================================================
# DESCRIPTON: The whole KMenas algorithm
# INPUt: 	n_clusters		[int] number of clusters (the K)
#			n_points		[int] number of random points
#			var 			[float] variance distribution
#							around clusters centers.
#							Must be between 0.1 and 0.5
#			runs			[int or None] Number of max runs.
#							If None, only tol is considered
#			tol  			[float] tolerance for convergence
#			save_figs:		[bool] save the figures to fig dir
# ========================================================
def kmeans(n_clusters, n_points, var=0.2, runs=20, tol=0.001, save_figs=False):

	# Just some validations
	if tol < 0.00001:
		print (f'Hey, dont be so radical. Your {tol} tolerance will be replaced with 0.00001')
		tol = 0.00001
	if runs is not None:
		if runs < 1:
			print (f'Come one... dont be so impatient. Your {runs} max runs will be replaced with 5')
			runs = 5
	else:
		runs = np.inf

	# IF save figs... create the dir
	if save_figs:
		try:
			os.mkdir('figs')
		except FileExistsError:
			print ('Directory already exists ... upsi.')


	centers = []
	# Set the random centers
	for c in range(n_clusters):
		# Random coords in range [0,1]
		cluster = np.random.uniform(0,1,2)
		centers.append(cluster)
	centers = np.array(centers)

	# Create random guess for the cluster centers
	# INITIAL SEARCH
	guess = np.array([np.random.uniform(0,1.2,2) for c in centers])

	points = []
	# Create random points equaly distributed around true centers,
	# with fixed variance var
	for n in range(n_points):
		c = np.random.randint(n_clusters)
		cx, cy = centers[c]
		point = np.random.normal(loc=[cx,cy], scale=[var,var])
		points.append(point)
	points = np.array(points)

	# Just a set of colors to use... if n_clusters is greater than
	# the len of this array, plotting will raise IndexError.
	all_colors = ['blue', 'red', 'green', 'purple', 'cyan', 'orange', 'darkred', 'orangered', 'royalblue', 'tan']
	all_colors = all_colors[:n_clusters]

	# Initially, all points are painted red.
	colors = ['red' for point in points]

	# Parche guadalupano número 1
	error = tol + 1


	# Show initial distribution
	plt.title(f'Point distribution and initial guess')
	# draw points
	plt.scatter(points[:,0], points[:,1], c=colors, s=10, alpha=0.5)
	# draw centers
	plt.scatter(guess[:,0],guess[:,1], s=40, c='black')
	plt.show()

	# to save, or not to save
	if save_figs:
		plt.savefig(f'./figs/f{0}.png')
		plt.clf()


	#for i in range(runs):
	i = 1
	while error > tol:
		# ========.. STEP 1 ..========
		# Calculate poitns distribution
		km = fit(points, guess)
		# Set the colors for each point
		colors = [all_colors[j] for j in km]

		# ====.. STEP 1.1 ..====
		# Plot plot plot
		plt.title(f'Try number {i}')
		print (f'====.. STEP {i} ..====')
		# draw points
		plt.scatter(points[:,0], points[:,1], c=colors, s=10, alpha=0.5)
		# draw centers
		plt.scatter(guess[:,0],guess[:,1], s=40, c='black')
		plt.show()

		# to save, or not to save
		if save_figs:
			plt.savefig(f'./figs/f{i}.png')
			plt.clf()

		# ========.. STEP 2 ..========
		# Update centers 
		new_guess = update_centers(points, km, guess)

		# Step size (tolerance)
		error = 0
		for g, ng in zip(guess, new_guess):
			step_size = d2(g, ng)
			error += step_size
			print (f'Center {g} will moved to {ng} --> step size: {step_size}')
		print (f'Total next step size on iteration {i}: {error}')

		guess = new_guess
		i += 1
		if i > runs:
			print (f'Upsi. Time is up. {i-1} runs reached.')
			break

	plt.title(f'Real versus Guess')
	plt.scatter(guess[:,0],guess[:,1], s=40, c='black')
	plt.scatter(centers[:,0],centers[:,1], s=40, c='red')
	plt.show()


	print ('====.. FINAL CLUSTERING ..====')
	for g in guess:
		print (f'Center at {g}')

	print ('====.. REAL CENTERS ..====')
	for c in centers:
		print (f'Center at {c}')




if __name__ == '__main__':
	# Primer argumento: número de clusters
	# Segundo argumento: número de muestras aleatorias
	kmeans(n_clusters=4, n_points=5002, runs=None, tol=0.005, save_figs=False)