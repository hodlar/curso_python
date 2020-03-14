import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import os
import random



# War, Action, Horror, Children, Film-Noir, Drama, Crime, Adventure, Sci-Fi, Thriller, Mystery, Comedy,
# Western, Fantasy, Animation, Documentary, Romance, IMAX, (no genres listed), Musical
tags = 	['War',
		 'Action',
		 'Horror',
		 'Children',
		 'Film-Noir',
		 'Drama',
		 'Crime',
		 'Adventure',
		 'Sci-Fi',
		 'Thriller',
		 'Mystery',
		 'Comedy',
		 'Western',
		 'Fantasy',
		 'Animation',
		 'Documentary',
		 'Romance',
		 'IMAX',
		 '(no genres listed)',
		 'Musical']
sensitive_tags = ['War', 'Horror', 'Crime']
tags_val = [1 if tag != '(no genres listed)' else 0 for tag in tags]
#tags_val = [tval+2 if tag in sensitive_tags else tval for tag, tval in zip(tags,tags_val)]


# ========================================================
# INPUt: p1 	[list] point coords x,y
#		 p2		[list] point coords x,y
# OOUTPUT:		Distance between p1 and p2
# ========================================================
def distance(p1, p2):
	global tags_val
	#return sum([tag*(abs(x1-x2)) for x1,x2,tag in zip(p1,p2,tags_val)])
	return sum(tags_val*abs(p1-p2))

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
		thisd = distance(point, c) 
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
	global tags
	new_centers = np.zeros_like(centers)
	num_centers = len(centers)
	sum_points_in_k = np.zeros_like(centers)
	count = [0 for i in sum_points_in_k]
	for k, point in zip(km, points):
		sum_points_in_k[k] += point
		count[k] += 1
	for c in range(num_centers):
		if count[c] > 0:
			new_centers[c] = sum_points_in_k[c]/count[c]
		else:
			new_centers[c] = np.random.uniform(0,1,len(tags))
	return new_centers



# ========================================================
# DESCRIPTON: The whole KMenas algorithm
# INPUt: 	n_clusters		[int] number of clusters (the K)
#			runs			[int or None] Number of max runs.
#							If None, only tol is considered
#			tol  			[float] tolerance for convergence
# ========================================================
def kmeans(n_clusters, runs=20, tol=0.001):

	global tags

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


	# Create random guess for the cluster centers
	guess = np.array([np.random.uniform(0,1,len(tags)) for c in range(n_clusters)])

	# ==================== FROM JUPYTER ==========================
	# Leo la tabla de películas
	movies = pd.read_csv('data/movies.csv')
	# Creo una tabla con (0,1) para cada película/categoría
	pelis, _ = movies.shape
	tagged_data = []
	for indx in movies.index:
		genres = movies.at[indx, 'genres']
		genres_list = genres.split('|')
		movie_tags_list = [1 if t in genres_list else 0 for t in tags]
		tagged_data.append(movie_tags_list)

	# Ahora, guardo esa información de tags en un DataFrame de pandas, por si a caso
	data = pd.DataFrame(tagged_data, columns=tags)
	# Y en un np array
	points = np.array(tagged_data)


	# Parche guadalupano número 1
	error = tol + 1


	#for i in range(runs):
	i = 1
	while error > tol:
		# ========.. STEP 1 ..========
		# Calculate poitns distribution
		km = fit(points, guess)

		# ========.. STEP 2 ..========
		# Update centers 
		new_guess = update_centers(points, km, guess)

		# Step size (tolerance)
		error = 0
		for g, ng in zip(guess, new_guess):
			step_size = distance(g, ng)
			error += step_size
			#print (f'Center {g} will moved to {ng} --> step size: {step_size}')
		print (f'Total next step size on iteration {i}: {error}')

		guess = new_guess
		i += 1
		if i > runs:
			print (f'Upsi. Time is up. {i-1} runs reached.')
			break


	#print ('====.. FINAL CLUSTERING ..====')
	#for g in guess:
	#	print (f'Center at {g}')


	print ('\n INICIAN RECOMENDACIONES ')
	# ========.. paso 1 .. ========
	#Selecciono una pelicula equis
	peli = np.random.randint(pelis)
	peli = 0
	# peli = 0 # Uncomment this line to set peli = 0, selecting Toy Story
	#Obtengo sus generos
	peli_name = movies.at[peli,'title']
	peli_genres = movies.at[peli, 'genres']
	#Separo los tags
	peli_genres_list = peli_genres.split('|')
	# peli_genres_list = ['Action','Western','Fantasy'] # Uncomment these linen for La película rara de Flor
	# peli_name = 'La pelicula rara de Flor'  # Uncomment these linen for La película rara de Flor
	peli_tags_list = [1 if t in peli_genres_list else 0 for t in tags]
	peli_cluster = get_cluster(peli_tags_list, guess)

	# ========.. paso 2 ..========
	# REPORTING:
	print (f'If you like the movie "{peli_name}", you may also like:')
	recomendeishon = []
	count = 0
	for indx in movies.index:
		p_genres = movies.at[indx, 'genres']
		p_genres_list = p_genres.split('|')
		p_tags_list = [1 if t in p_genres_list else 0 for t in tags]
		p_cluster = get_cluster(p_tags_list, guess)
		if p_cluster == peli_cluster and peli != indx:
			count += 1
			recomendeishon.append(movies.at[indx, 'title'])
			#if count >= 10:
			#    break
	# En lugar de este random, se mezclaría con raitings 
	random.shuffle(recomendeishon)
	[print(f'\t- {TITLE}') for TITLE in recomendeishon[:10]];



if __name__ == '__main__':
	# Primer argumento: número de clusters
	# Segundo argumento: número de muestras aleatorias
	kmeans(n_clusters=10, runs=10, tol=1.0)
