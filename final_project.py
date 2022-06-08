# Final Project ~ Patrick Burke
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# 1. Read in the three movie data sets and combines them into a single dataframe
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# Read in the three datafiles
u_col = ['UID','gender','age','job','zip']
users = pd.read_table('users.dat',sep='::',header = None, names = u_col, engine='python', encoding = "ISO-8859-1")

r_col = ['UID','MID','rating','TSDate']
ratings = pd.read_table('ratings.dat',sep='::',header = None, names = r_col,engine='python', encoding = "ISO-8859-1")

m_col = ['MID','Title','genre']
movies = pd.read_table('movies.dat',sep='::',header = None, names = m_col,engine='python', encoding = "ISO-8859-1")


# Merge two dataframes on UID
movie_temp = pd.merge(ratings,users)
# Merge two dataframes on MID
movie_data = pd.merge(movie_temp, movies)

# See the results
movie_data.head()

# 2. Merge with the Bond .csv file to create a single dataframe that only has data for the Bond films in the data sets.
m_col = ['MID','Title','Year','Actor','Director','A_Gross','Adj_Gross','A_Budget','Adj_Budget','Return']
bond_movies = pd.read_table('bond_film_4.csv',sep=',',header = None, names = m_col,engine='python', encoding = "ISO-8859-1")
bond_movies.at[15,'Title']= 'Dr. No'
bond_movies.head()

merged_bond_movies = movie_data.merge(bond_movies, on='MID', how='inner')
merged_bond_movies.drop('Title_x', axis=1, inplace=True)
merged_bond_movies.rename(columns = {'Title_y': 'Title'}, inplace=True)
merged_bond_movies.describe(include = 'all')

# 3. Menu options
def gen_mean_rating():
    gender_ratings = merged_bond_movies.pivot_table('rating',index = 'Title',columns ='gender', aggfunc='mean')
    title_ratings = merged_bond_movies.groupby('Title').size()
    pop_title_ratings = title_ratings.index[title_ratings>= 1]
    pop_mean_ratings = gender_ratings.loc[pop_title_ratings]
    print("Ratings by Gender: \n",pop_mean_ratings, "\n")

def occ_mean_rating():
    # Give a bar chart by occupation as well
    occ_ratings = merged_bond_movies.pivot_table('rating',index = 'Title',columns ='job', aggfunc='mean')
    title_ratings = merged_bond_movies.groupby('Title').size()
    pop_title_ratings = title_ratings.index[title_ratings>= 1]
    pop_mean_ratings = occ_ratings.loc[pop_title_ratings]
    print("Ratings by Job: \n", pop_mean_ratings, "\n")
    pop_mean_ratings.plot(kind = 'bar')
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()
    
def age_mean_rating():
    # Give a bar chart by age as well
    age_ratings = merged_bond_movies.pivot_table('rating',index = 'Title',columns ='age', aggfunc='mean')
    title_ratings = merged_bond_movies.groupby('Title').size()
    pop_title_ratings = title_ratings.index[title_ratings>= 1]
    pop_mean_ratings = age_ratings.loc[pop_title_ratings]
    print("Ratings by Age: \n",pop_mean_ratings, "\n")
    pop_mean_ratings.plot(kind = 'bar')
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()
    
def single_score(movie):
    single_movie =  merged_bond_movies.loc[merged_bond_movies['Title'] == movie]
    single_movie_score = single_movie['rating'].mean()
    print("The average rating of", movie,"is", single_movie_score)


def occ_single_score(movie):
    # Give a bar chart by occupation as well
    single_movie =  merged_bond_movies.loc[merged_bond_movies['Title'] == movie]
    single_movie_age = single_movie['rating'].mean(axis = 0)
    job_rating_single = single_movie.pivot_table('rating',index = 'Title',columns ='job', aggfunc='mean')
    job_rating_single.plot(kind = 'bar', rot = 0)
    print(job_rating_single)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()
    
def age_single_score(movie):
    # Give a bar chart by age as well
    single_movie =  merged_bond_movies.loc[merged_bond_movies['Title'] == movie]
    single_movie_age = single_movie['rating'].mean(axis = 0)
    age_rating_single = single_movie.pivot_table('rating',index = 'Title',columns ='age', aggfunc='mean')
    age_rating_single.plot(kind = 'bar', rot = 0)
    print(age_rating_single)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.show()

while True:
    print("Menu Driven Program \n")
    print("1. Mean Rating of all Bond Movies Based on Gender")
    print("2. Mean Rating of all Bond Movies Based on Occupation")
    print("3. Mean Rating of all Bond Movies Based on Age Range")    
    print("4. Mean Score for a Single Bond Movie")
    print("5. Mean Score for a Single Bond Movie Based on Occupation")
    print("6. Mean Rating for a Single Bond movie Based on Age Range")
    print("7. Exit \n")
    choice=int(input("Enter your choice: \n"))


    if choice==1:
        gen_mean_rating()


    elif choice==2:
        occ_mean_rating()
    
    elif choice==3:
        age_mean_rating()
    
    elif choice==4:
        movie=(input("Enter Bond Movie Name: \n"))
        single_score(movie)
            
    elif choice==5:
        movie=(input("Enter Bond Movie Name: \n"))
        occ_single_score(movie)
            
    elif choice==6:
        movie=(input("Enter Bond Movie Name: \n"))
        age_single_score(movie)

    elif choice==7:
        break
    else:
        print("Invalid Choice \n")
