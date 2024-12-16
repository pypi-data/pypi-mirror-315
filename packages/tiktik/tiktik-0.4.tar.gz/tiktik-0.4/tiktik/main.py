def kokul():
    print("kokul, appleornotnaive, appleornotcandi, candsunnyorrain, carpreferencesfinds, dbscan, diabetes_logistic, enjoysportfinds, finds, heirarchialclust, heirarkmeansexam, diabeteshmm, hmmrainy, id3, kmeanscluster, knniris, naiveposorneg, naivetsampletext, orangeorapple, naivespamornot, svmiris, backwardimage")


def appleornotnaive():
    print('''import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split
file_path='../../Downloads/apple.csv'
data=pd.read_csv(file_path)
data.head()
label_encoder=LabelEncoder()
X=data.iloc[:,:-1]
X.head()
X['Color']=label_encoder.fit_transform(X['Color'])
X['Shape']=label_encoder.fit_transform(X['Shape'])
X['Size']=label_encoder.fit_transform(X['Size'])
X.head()
y=data.iloc[:,-1]
y.head()
y_encoded=label_encoder.fit_transform(y)
y_encoded
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
model=CategoricalNB(alpha=1.0)
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
y_pred
accuracy=accuracy_score(y_pred,y_test)
report=classification_report(y_pred,y_test,target_names=label_encoder.classes_)
print("Accuracy is ",accuracy)
print("Classification report is \n",report)''')
    

def appleornotcandi():
    print('''import csv
data=[]
with open('../../Downloads/apple.csv','r') as file:
    
    reader=csv.reader(file)
    next(reader)
    for row in reader:
        data.append(row)
print(data) 
features=[row[:-1] for row in data]
target=[row[-1] for row in data]
def candidate_elimination(data,target):
    S=data[0].copy()
    G=[['?' for _ in range(len(S))]]
    for i,instance in enumerate(data):
        label=target[i]
        print(f"The instance{i+1} is {instance} and its label is {label}")
        if label=='Apple':
            for k in range(len(S)):
                if S[k]!='?' and S[k]!=instance[k]:
                    S[k]='?'
            G=[g for g in G if consistent(instance,g)]
            print(f"Updated specific hypothesis at S[{i+1}] is {S} and general hypothesis G[{i+1}] is {G}")
            
        elif label=='Not Apple':
            print("Updating generic hypothesis")
            new_G=[]
            for g in G:
                for k in range(len(G)):
                    if g[k]=='?':
                        for value in get_values(data,k):
                            if instance[k]!=value:
                                specialised_g=g.copy()
                                specialised_g[k]=value
                                if consistent_with_boundary(S,specialised_g):
                                    new_G.append(specialised_g)
                    elif g[k]!=instance[k]:
                        new_G.append(specialised_g)
                G=remove_more_general(new_G)
                print(f"Updated specific hypothesis at S[{i+1}] is {S} and general hypothesis G[{i+1}] is {G}")
    return S,G
def consistent(instance,hypothesis):
    for i in range(len(hypothesis)):
        if hypothesis[i]!='?' and hypothesis[i]!=instance[i]:
            return False
    return True
def consistent_with_boundary(S,hypothesis):
    for i in range(len(hypothesis)):
        if S[i]!='?' and hypothesis[i]!='?' and hypothesis[i]!=instance[i]:
            return False
    return True
def remove_more_general(hypothesis):
    non_general=[]
    for h1 in hypothesis:
        is_more_general=False
        for h2 in hypothesis:
            if h1!=h2 and more_general(h1,h2):
                is_more_general=True
                break
        if not is_more_general:
            non_general.append(h1)
    return non_general
def more_general(h1,h2):
    is_more_general=False
    for x,y in zip(h1,h2):
        if x=='?':
            is_more_general=True
        elif x!=y:
            return False
        elif y!='?':
            return False
    return is_more_general 
def get_values(data,k):
    return set(row[k] for row in data)
if __name__=="__main__":
    S,G=candidate_elimination(features,target)
    print("Final Specific Hypothesis is ",S)
    print("Final General Hypothesis is ",G)
    

''')
    

def candsunnyorrain():
    print('''import numpy as np
def candidate_elimination(data,target):
    S=data[0].copy()
    G=[['?' for _ in range(len(S))]]
    for i,instance in enumerate(data):
        label=target[i]
        print(f"Instance {i+1}: {instance} and the label is {label}")
        if label=='Yes':
            print("-> Positive Hypothesis: Updating specific Hypothesis")
            for j in range(len(S)):
                if S[j]!=instance[j]:
                    S[j]='?'
            G=[g for g in G if consistent(instance,g)]
            print(f"Updated Specific Hypothesis is {S}")
            print(f"Updated General Hypothesis is {G}")
        elif label=='No':
            print("->Negative Hypothesis : Updating General Hypothesis")
            new_G=[]
            for g in G:
                for k in range(len(g)):
                    if g[k]=='?':
                        for value in get_values(data,k):
                            if value!=instance[k]:
                                specialised_g=g.copy()
                                specialised_g[k]=value
                                if consistent_with_boundary(S,specialised_g):
                                    new_G.append(specialised_g)
                    elif g[k]!=instance[k]:
                        new_G.append(specialised_g)
            G=remove_more_general(new_G)
            print(f"Updating Specific Hypothesis is {S}")
            print(f"Updating General Hypothesis is {G}")
    return S,G
def consistent(instance,hypothesis):
    for i in range(len(hypothesis)):
        if hypothesis[i]!='?' and instance[i]!=hypothesis[i]:
            return False
    return True  
def consistent_with_boundary(S,hypothesis):
    for i in range(len(S)):
        if S[i]!='?' and hypothesis[i]!='?' and S[i]!=hypothesis[i]:
            return False
    return True
def get_values(data,k):
    return set(row[k] for row in data)
def remove_more_general(hypothesis):
    new_G=[]
    for h1 in hypothesis:
        is_more_general=False
        for h2 in hypothesis:
            if h1!=h2 and more_general(h1,h2):
                is_more_general=True
                break
        if not is_more_general:
            new_G.append(h1)
    return new_G
def more_general(h1,h2):
    more_general=True
    for x,y in zip(h1,h2):
        if x=='?':
            more_general=True
        elif x!=y:
            return False
        elif y=='?':
            return False
    return more_general
if __name__=='__main__':
    data=[
        ['Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same'],
        ['Sunny', 'Warm', 'High', 'Strong', 'Warm', 'Same'],
        ['Rainy', 'Cold', 'High', 'Strong', 'Warm', 'Change'],
        ['Sunny', 'Warm', 'High', 'Strong', 'Cool', 'Change']
    ]
    target = ['Yes', 'Yes', 'No', 'Yes']
    S,G=candidate_elimination(data,target)
    print(f"Final Specific Hypothesis : (S) -> {S}")
    print(f"Final General Hypothesis : (G) -> {G}")''')


def carpreferencesfinds():
    print('''import numpy as np
import pandas as pd
data=pd.read_excel('../../Downloads/car preference.xlsx')
target=data.iloc[:,-1].tolist()
features=data.iloc[:,:-1].values.tolist()
target
features
def FindS(data,target):
    S=data[0].copy()
    for i,instance in enumerate(data):
        label=target[i]
        print(f"The instance{i+1} is {instance} and its label is {label}")
        if label=='Apple':
            for k in range(len(S)):
                if S[k]!='?' and S[k]!=instance[k]:
                    S[k]='?'
            
            print(f"Updated specific hypothesis at S[{i+1}] is {S}")
            
        elif label=='Not Apple':
            continue
    return S
if __name__=="__main__":
    S=FindS(features,target)
    print("Final Specific Hypothesis is ",S)''')


def dbscan():
    print('''import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
X,y=make_moons(n_samples=300,noise=0.05,random_state=42)
plt.scatter(X[:,0],X[:,1],s=10,color="blue")
plt.title("Original data")
plt.show()
eps=0.2
min_samples=5
dbscan=DBSCAN(eps=eps,min_samples=min_samples)
clusters=dbscan.fit_predict(X)
plt.scatter(X[:,0],X[:,1],c=clusters,cmap='viridis',s=10)
plt.title("DBSCAN Clustering")
plt.colorbar(label="Cluster Label")
plt.show()''')
    
def diabetes_logistic():
    print('''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
data=pd.read_csv('../../Downloads/diabetes.csv')
data.head()
X=data.iloc[:,:-1]
y=data.iloc[:,-1]
X.head()
y.head()
standard_scaler=StandardScaler()
X_scaled=standard_scaler.fit_transform(X)
X_train,X_test,y_train,y_test=train_test_split(X_scaled,y,test_size=0.2,random_state=42)
model=LogisticRegression()
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
accuracy=accuracy_score(y_pred,y_test)
report=classification_report(y_pred,y_test,labels=model.classes_)
conf_matrix=confusion_matrix(y_pred,y_test)
print("Accuracy is ",accuracy)
print("Classification matrix is\n",report)
print("Confusion matrix is\n",conf_matrix)
from sklearn.ensemble import RandomForestClassifier
random=RandomForestClassifier()
random.fit(X_train,y_train)
y_pred=random.predict(X_test)
#Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print('Confusion Matrix:')
print(conf_matrix)
print('Classification Report:')
print(class_report)''')
    
def enjoysportfinds():
    print('''import pandas as pd
data=pd.read_csv('../../Downloads/enjoysport.csv')
data.head()
X=data.iloc[:,:-1]
y=data.iloc[:,-1]
X.head()
y.head()
def Find_S(data,target):
    S=data[0].copy()
    print(f"Hypothesis S[0] is {S}\n")
    for i,instance in enumerate(data):
        label=target[i]
        print(f"Instance {i+1} is : {instance} and the target value is {target}")
        if label=='yes':
            print("Updating the hypothesis S")
            for k in range(len(S)):
                if S[k]!='?' and S[k]!=instance[k]:
                    S[k]='?'
            print(f"Hypothesis S[{i+1}] is {S}")
        elif label=='no':
            continue
    return S
import csv

# Initialize an empty list to store the data
data = []

# Open and read the CSV file
with open('../../Downloads/enjoysport.csv', mode='r') as file:
    reader = csv.reader(file)
    
    # Skip the header
    next(reader)
    
    # Add each row (excluding the header) to the data list
    for row in reader:
        data.append(row)

# Now `data` contains the 2D list representation of the dataset without the header
print(data)
# Separate the target (last column) from the features (all other columns)
features = [row[:-1] for row in data]  # All columns except the last
target = [row[-1] for row in data]    # Only the last column (target)

# Now `features` contains the 2D list of attributes (without the header)
# And `target` contains the corresponding class labels
print("Features:", features)
print("Target:", target)
S=Find_S(features,target)
print(f"Final Hypothesis is {S}")''')
    
def finds():
    print('''import numpy as np
def Find_S(data,target):
    S=data[0].copy()
    #G=[['?' for _ in range(len(S))]]
    for i,instance in enumerate(data):
        label=target[i]
        print(f"Instance {i+1}: {instance} and the label is {label}")
        if label=='Yes':
            print("-> Positive Hypothesis: Updating specific Hypothesis")
            for j in range(len(S)):
                if S[j]!=instance[j]:
                    S[j]='?'
            #G=[g for g in G if consistent(instance,g)]
            print(f"Updated Specific Hypothesis is {S}")
            #print(f"Updated General Hypothesis is {G}")
        elif label=='No':
            print("No Updation")
            continue
    return S
if __name__="__main__":
    data = [
        ['Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same'],
        ['Sunny', 'Warm', 'High', 'Strong', 'Warm', 'Same'],
        ['Rainy', 'Cold', 'High', 'Strong', 'Warm', 'Change'],
        ['Sunny', 'Warm', 'High', 'Strong', 'Cool', 'Change']
    ]
    target = ['Yes', 'Yes', 'No', 'Yes']

    S = candidate_elimination(data, target)
    print(f"Final H")
          ''')
    
def heirarchialclust():
    print('''import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import dendrogram,linkage
from scipy.cluster.hierarchy import fcluster
def generate_datasets(n_samples=100,n_features=2,n_clusters=3):
    X,y=make_blobs(n_samples=n_samples,centers=n_clusters,n_features=n_features,random_state=42)
    return X,y
def perform_hierarchical_clustering(X,method='ward'):
    Z=linkage(X,method=method)
    return Z
def plot_dendogram(Z):
    plt.figure(figsize=(10,7))
    plt.title("Heirarchical Clustering: ")
    dendrogram(Z)
    plt.xlabel('Sample Index')
    plt.ylabel('Index')
    plt.show()
def extract_clusters(Z,num_clusters):
    clusters=fcluster(Z,num_clusters,criterion='maxclust')
    return clusters
if __name__=="__main__":
    X,y=generate_datasets(n_samples=100,n_clusters=3,n_features=2)
    Z=perform_hierarchical_clustering(X,method='ward')
    plot_dendogram(Z)
    
    num_clusters=3
    clusters=extract_clusters(Z,num_clusters)
    
    plt.figure(figsize=(10,7))
    plt.scatter(X[:,0],X[:,1],c=clusters,cmap='rainbow',s=50)
    plt.title("Hierarchical Clusters with {0} clusters".format(num_clusters))
    plt.xlabel("Feature 1")
    plt.ylabel("feature 2")
    plt.show()
from sklearn.cluster import AgglomerativeClustering
hc=AgglomerativeClustering(n_clusters=3,affinity='euclidean',linkage='ward')
y_pred=hc.fit_predict(X)
import matplotlib.pyplot as mtp
#visulaizing the clusters  
mtp.scatter(X[y_pred == 0, 0], X[y_pred == 0, 1], s = 100, c = 'blue', edgecolors='k',label = 'Cluster 1')  
mtp.scatter(X[y_pred == 1, 0], X[y_pred == 1, 1], s = 100, c = 'green', edgecolors='k',label = 'Cluster 2')  
mtp.scatter(X[y_pred== 2, 0], X[y_pred == 2, 1], s = 100, c = 'red',edgecolors='k', label = 'Cluster 3')   
mtp.title('Clusters of customers')  
mtp.xlabel('Annual Income (k$)')  
mtp.ylabel('Spending Score (1-100)')  
mtp.legend()  
mtp.show() 
Z=linkage(X,'ward')
plt.figure(figsize=(10,7))
plt.title("Heirarchical Clustering: ")
dendrogram(Z)
plt.xlabel('Sample Index')
plt.ylabel('Index')
plt.show()''')
    

def heirarkmeansexam():
    print('''import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram,linkage
from scipy.cluster.hierarchy import fcluster
data=pd.read_csv('../../Downloads/exams.csv')
data.head()
X=data[['math score','reading score','writing score']]
Z=linkage(X,method='ward')
clusters=fcluster(Z,3,criterion='maxclust')
import matplotlib.pyplot as plt
plt.figure(figsize=(10,7))
plt.title("Hierarchical Clustering")
dendrogram(Z)
plt.xlabel('Sample Index')
plt.ylabel('Index')
plt.show()
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# 3D scatter plot
ax.scatter(
    X['math score'], X['reading score'], X['writing score'], 
    c=clusters, cmap='rainbow', s=10
)

ax.set_xlabel('Math Score')
ax.set_ylabel('Reading Score')
ax.set_zlabel('Writing Score')
plt.show()

from sklearn.cluster import KMeans
kmeans=KMeans(n_clusters=3)
from sklearn.preprocessing import StandardScaler
stand=StandardScaler()
X_scaled=stand.fit_transform(X)
kmeans.fit(X_scaled)
y_kmeans=kmeans.fit_predict(X_scaled)
centroid=kmeans.cluster_centers_
fig=plt.figure(figsize=(10,7))
ax=fig.add_subplot(111,projection='3d')
ax.scatter(X_scaled[:,0],X_scaled[:,1],X_scaled[:,2],c=y_kmeans,s=10,cmap='viridis',alpha=0.7)
ax.scatter(centroid[:,0],centroid[:,1],centroid[:,2],c='red',marker='X',s=200,label="Centroids")
ax.set_title("Kmeans clustering")
ax.set_xlabel("math score")
ax.set_ylabel("reading score")
ax.set_zlabel("writing score")
ax.legend()
plt.show()''')
    

def diabeteshmm():
    print('''import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from hmmlearn import hmm
import matplotlib.pyplot as plt
data=pd.read_csv("../../Downloads/diabetes.csv")
data.head()
data.columns
features=data[['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']]
target=data[['Outcome']]
features.head()
target.head()

features_normalized = (features - features.mean()) / features.std()
observations=features_normalized.apply(pd.qcut,q=3,labels=False,duplicates='drop').astype(int).values
n_components=2
model=hmm.MultinomialHMM(n_components=n_components,n_iter=100,random_state=42)
model.stateprob_=np.array([0.5,0.5])
model.transmat_=np.array([[0.7,0.3],[0.4,0.6]])
n_bins=len(np.unique(observations))
model.emissionprob_=np.ones((n_components,n_bins))/n_bins
model.fit(observations)
hidden_states=model.predict(observations)

# Import necessary libraries
import numpy as np
import pandas as pd
from hmmlearn import hmm
import matplotlib.pyplot as plt

# Load the dataset 
data = pd.read_csv('../../Downloads/diabetes.csv')
print(data)
# Drop missing values
data = data.dropna()

# Extract features and outcome
features = data[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
outcomes = data['Outcome']

# Normalize features for better modeling
features_normalized = (features - features.mean()) / features.std()

# Convert features to discrete states (e.g., using quantiles)
# Handle duplicate bin edges and adjust labels accordingly
observations = features_normalized.apply(
    pd.qcut, q=3, labels=False, duplicates='drop'  # Remove labels here
).astype(int).values  

# Define the HMM model
n_components = 2  # Two states: Diabetes (1) and Non-Diabetes (0)
model = hmm.MultinomialHMM(n_components=n_components, n_iter=100, random_state=42)

# Initialize model parameters
model.startprob_ = np.array([0.5, 0.5])  # Equal probability of starting in either state
model.transmat_ = np.array([[0.7, 0.3], [0.4, 0.6]])  # Transition probabilities

# Assume equal emission probabilities for simplicity, adjust for number of bins
n_bins = len(np.unique(observations)) # Get the actual number of bins
model.emissionprob_ = np.ones((n_components, n_bins)) / n_bins 

# Fit the model to the observations
model.fit(observations)

# Predict hidden states (diabetes or non-diabetes)
hidden_states = model.predict(observations)

# Map hidden states to outcomes (0 or 1)
predicted_outcomes = hidden_states

# Compare actual outcomes with predicted outcomes
plt.figure(figsize=(12, 6))
plt.plot(outcomes.values[:50], label='Actual Outcome', marker='o', linestyle='-')
plt.plot(predicted_outcomes[:50], label='Predicted Outcome', marker='x', linestyle='--')
plt.title('Comparison of Actual and Predicted Outcomes')
plt.xlabel('Sample Index')
plt.ylabel('Diabetes Outcome')
plt.legend()
plt.show()

# Print a brief evaluation
accuracy = np.mean(predicted_outcomes == outcomes.values)
print(f"Prediction Accuracy: {accuracy * 100:.2f}%")''')
    

def hmmrainy():
    print('''pip install hmmlearn
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm
import seaborn as sns
states=['Sunny','Rainy']
n_states=len(states)
print(f"Number of states is {n_states} and the states are {n_states}")
observables=['Dry','Wet']
n_obs=len(observables)
print(f"Number of observables are {n_obs} and the observables are {observables}")
state_probability=np.array([0.6,0.4])
print(f"Initial probability of {states} are {state_probability}")
transition_probability=np.array([[0.7,0.3],[0.3,0.7]])
print(f"Transition probability for {states} states and {observables} \n observations are \n{transition_probability}")
emission_probability=np.array([[0.9,0.1],[0.2,0.8]])
print(f"Emission probability for {states} states and {observables} \n observations are \n{emission_probability}")
model=hmm.CategoricalHMM(n_components=n_states)
model.startprob_=state_probability
model.transmat_=transition_probability
model.emissionprob_=emission_probability
observation_sequence=np.array([0,1,0,1,0,0]).reshape(-1,1)
hidden_states=model.predict(observation_sequence)
print(f"Most Likely hidden states are {hidden_states}")
log_probability,hidden_state_viterbi=model.decode(observation_sequence,algorithm='viterbi')
print(f"Log Probability is {log_probability}")
print(f"Hidden States(Viterbi) is {hidden_state_viterbi}")
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
plt.plot(hidden_state_viterbi,'-o',label="Hidden States",color="blue")
plt.xlabel("Time Step")
plt.ylabel("Most Likely Hidden states")
plt.legend(loc="upper left")
plt.xticks(ticks=range(len(observation_sequence)),labels=observation_sequence.flatten())
plt.show()''')
    

def id3():
    print('''import pandas as pd
import numpy as np
from collections import Counter
def id3(data,features,target):
    y=data[target]
    if len(set(y))==1:
        return y.iloc[0]
    if not features:
        return y.mode()[0]
    best_features=max(features,key=lambda f:information_gain(data,f,target))
    tree={best_features:{}}
    for value in data[best_features].unique():
        subset=data[data[best_features]==value]
        subtree=id3(subset,[f for f in features if f!=best_features],target)
        tree[best_features][value]=subtree
    return tree
def entropy(y):
    counts=Counter(y)
    probability=[count/len(y) for count in counts.values()]
    return -sum(p*np.log2(p) for p in probability if p>0)
def information_gain(data,feature,target):
    total_entropy=entropy(data[target])
    values=data[feature].unique()
    weighted_entropy=sum(len(data[data[feature]==v])/len(data) * entropy(data[data[feature]==v][target]) for v in values)
    return total_entropy-weighted_entropy
def predict(tree,instance):
    if not isinstance(tree,dict):
        return tree
    feature=next(iter(tree))
    value=instance[feature]
    if value in tree[feature]:
        return predict(tree[feature][value],instance)
    else:
        return None
def accuracy_score(tree,data,target):
    predictions=data.apply(lambda row:predict(tree,row),axis=1)
    correct=sum(predictions==data[target])
    return correct/len(data)
def display_tree(tree,depth=0):
    if not isinstance(tree,dict):
        print(" " * depth + f"-> {tree}")
        return
    for feature,branches in tree.items():
        for value,subtree in branches.items():
            print(" " * depth + f"{feature}={value}")
            display_tree(subtree,depth+1)
if __name__ == "__main__":
    # Sample dataset (replace with your dataset)
    data = pd.DataFrame({
        "Outlook": ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny", "Rain", "Sunny", "Overcast", "Overcast", "Rain"],
        "Temperature": ["Hot", "Hot", "Hot", "Mild", "Cool", "Cool", "Cool", "Mild", "Cool", "Mild", "Mild", "Mild", "Hot", "Mild"],
        "Humidity": ["High", "High", "High", "High", "Normal", "Normal", "Normal", "High", "Normal", "Normal", "Normal", "High", "Normal", "High"],
        "Wind": ["Weak", "Strong", "Weak", "Weak", "Weak", "Strong", "Strong", "Weak", "Weak", "Weak", "Strong", "Strong", "Weak", "Strong"],
        "PlayTennis": ["No", "No", "Yes", "Yes", "Yes", "No", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "No"]
    })
    
    target = "PlayTennis"
    features=list(data.columns.difference([target]))
    tree=id3(data,features,target)
    print("Decision tree:")
    display_tree(tree,0)
    accuracy=accuracy_score(tree,data,target)
    print("Accuracy of the above model is : ",accuracy)''')



def kmeanscluster():
    print('''import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
iris=load_iris()
X=iris.data
scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)
k=3
kmeans=KMeans(n_clusters=k,random_state=42)
kmeans.fit(X_scaled)
labels=kmeans.labels_
centroids=kmeans.cluster_centers_
plt.figure(figsize=(10,6))
plt.scatter(X_scaled[:,0],X_scaled[:,1],c=labels,cmap='viridis',s=100,edgecolors='k',alpha=0.6)
plt.scatter(centroids[:,0],centroids[:,1],c='red',s=200,marker='x',label='Centroids')
plt.legend(loc='upper right')
plt.show()''')
    
def knniris():
    print('''import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,ConfusionMatrixDisplay
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
import seaborn as sns
import matplotlib.pyplot as plt
iris=load_iris()
X=iris.data
y=iris.target
print("The iris data are: \n",X)
print("The iris target are: \n",y)
features=iris.feature_names
target_names=iris.target_names
print("Features are: ",features)
print("Target names are: ",target_names)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.4,random_state=42)
knn=KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train,y_train)
y_pred=knn.predict(X_test)
y_pred
accuracy=accuracy_score(y_pred,y_test)
classification_report=classification_report(y_pred,y_test)
print(f"Accuracy score is : {accuracy*100:.2f}")
print(f"Classification report is : \n {classification_report}")
cm=confusion_matrix(y_pred,y_test)
print(f"Confusion matrix is :\n {cm}")
conf_table=pd.DataFrame(cm,columns=target_names,index=target_names)
print(conf_table)
disp=ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=target_names)
disp.plot(cmap='Blues')
plt.title("Confusion Matrix of KNN Model")
plt.show()
plt.figure(figsize=(8,6))
sns.scatterplot(x=y_test,y=y_pred)''')
    

def naiveposorneg():
    print('''import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
file_path="../../Downloads/text.csv"
data=pd.read_csv(file_path,header=None)
data=data.reset_index(drop=True)
data.head()
X=data.iloc[:,0]
y=data.iloc[:,1]
X.head()
y.head()
label_encoder=LabelEncoder()
y_encoded=label_encoder.fit_transform(y)
X_train,X_test,y_train,y_test=train_test_split(X,y_encoded,test_size=0.2,random_state=42)
model=Pipeline([('tfidf',TfidfVectorizer(stop_words="english",ngram_range=(1,2))),('nb',MultinomialNB(alpha=1.0))])
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
y_pred
y_pred_encoded=label_encoder.inverse_transform(y_pred)
y_pred_encoded
y_test
accuracy=accuracy_score(y_pred,y_test)
accuracy
classification_report=classification_report(y_pred,y_test,output_dict=True)
print(classification_report)
precision=classification_report['0']['precision']
recall=classification_report['0']['recall']
f1_score=classification_report['0']['f1-score']
support=classification_report['0']['support']
precision
new_text=['This delivery is very slow']
new_text_vector=model.named_steps['tfidf'].transform(new_text)
predictions=model.named_steps['nb'].predict(new_text_vector)
predictions
prediction_label=label_encoder.inverse_transform(predictions)
prediction_label
def give_new_text(new_text):
    new_text_vector=model.named_steps['tfidf'].transform(new_text)
    predictions=model.named_steps['nb'].predict(new_text_vector)
    prediction_label=label_encoder.inverse_transform(predictions)
    return prediction_label
new_text=['The dishes are delicious']
print(give_new_text(new_text))''')
    
def naivetsampletext():
    print('''import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,classification_report
from sklearn.pipeline import Pipeline
file_path="../../Downloads/sample_text_data.csv"
data=pd.read_csv(file_path)
data.head()
X=data['text']
y=data['label']
X.head()
y.head()
label_encoder=LabelEncoder()
y_encoded=label_encoder.fit_transform(y)
y_encoded
X_train,X_test,y_train,y_test=train_test_split(X,y_encoded,test_size=0.3,random_state=42)
pipeline=Pipeline([('tfidf',TfidfVectorizer(stop_words='english',ngram_range=(1,2))),('nb',MultinomialNB(alpha=1.0))])
pipeline.fit(X_train,y_train)
y_pred=pipeline.predict(X_test)
y_pred
y_pred_decoded=label_encoder.inverse_transform(y_pred)
y_pred_decoded
accuracy=accuracy_score(y_pred,y_test)
report=classification_report(y_pred,y_test)
print(f"Accuracy is :{accuracy*100:.2f}")
print("Classification report is \n",report)
#Example classify new text
new_text=["Elections dates to be announced soon."]
new_text_vectorized=pipeline.named_steps['tfidf'].transform(new_text)
predictions=pipeline.named_steps['nb'].predict(new_text_vectorized)
predictions
predicted_label=label_encoder.inverse_transform(predictions)
print(f"Predicted label for the given text : {new_text[0]} is {predicted_label[0]}")
from sklearn.preprocessing import OneHotEncoder
one_hot=OneHotEncoder()
label_one_hot=one_hot.fit_transform(X)''')
    
def orangeorapple():
    print('''import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier,plot_tree
from sklearn.metrics import accuracy_score,classification_report
data=pd.read_csv('../../Downloads/fruits.csv')
data.head()
X=data[['Weight','Size']]
X.head()
y=data[['Class']]
y.head()
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
model=DecisionTreeClassifier(random_state=42)
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
accuracy=accuracy_score(y_pred,y_test)
report = classification_report(y_test, y_pred)
print("Accuracy score is ",accuracy)
print("Classification Report is \n",report)
plt.figure(figsize=(10,7))
plot_tree(model,feature_names=['Weight','Size'],class_names=model.classes_,filled=True)
plt.title('Decision Tree Classifier')
plt.show()''')
    
def naivespamornot():
    print('''import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import csv
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
data=[]
with open('../../Downloads/spam.csv','r') as file:
    reader=csv.reader(file)
    for row in reader:
        data.append(row)
data
df = pd.DataFrame(data[1:], columns=data[0]) 
data1=pd.read_csv('../../Downloads/spam.csv',encoding='latin1')
data1.head()
X=data1['data']
y=data1['target']
encoder=LabelEncoder()
y_encoder=encoder.fit_transform(y)
X_train,X_test,y_train,y_test=train_test_split(X,y_encoder,test_size=0.1,random_state=42)
model=Pipeline([('tfidf',TfidfVectorizer(stop_words="english",ngram_range=(1, 2))),('nb',MultinomialNB(alpha=1.0))])
X_train
y_train
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
X_test
y_test
y_prediction=encoder.inverse_transform(y_pred)
y_prediction
accuracy=accuracy_score(y_pred,y_test)
accuracy
def give_new_text(new_text):
    new_text_vector=model.named_steps['tfidf'].transform(new_text)
    predictions=model.named_steps['nb'].predict(new_text_vector)
    prediction_label=encoder.inverse_transform(predictions)
    return prediction_label
new_text=['Hi darlin did youPhone me? Im atHome if youwanna chat.']
detect=give_new_text(new_text)
detect''')
    

def svmiris():
    print('''import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
iris=load_iris()
X=iris.data[:,:2]
y=iris.target
X=X[y!=2]
y=y[y!=2]
iris
features=iris.feature_names
target_name=iris.target_names
feature_need=features[:2]
target_need=target_name[:2]
print(f"Needed features are: {feature_need}")
print(f"Needed Target are: {target_need}")
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.4,random_state=42)
model=SVC(kernel='linear',C=1.0)
model.fit(X_train,y_train)
#Step 4: Visualization of the decision boundary and the test data points
def plot_svm(X, y, model, X_test, y_test):
    # Create a mesh grid to plot the decision boundaries
    h = 0.02  # step size in the mesh
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Predict the decision boundary for the grid points
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot the decision boundaries
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, edgecolors='k', marker='o', label="Train Data")

    # Highlight the test data points in a different color (X's)
    #plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.coolwarm, edgecolors='k', marker='x', s=100, label="Test Data")
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.coolwarm, marker='x', s=100, label="Test Data")


    # Labeling the plot
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('SVM Decision Boundary with Training and Test Data')
    plt.legend(loc='upper left')

    # Support vectors (highlighted)
    plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=100, facecolors='none', edgecolors='yellow', label='Support Vectors')

    plt.show()

# Step 5: Call the function to plot
plot_svm(X_train, y_train, model, X_test, y_test)
''')
    
def backwardimage():
    print('''import cv2
import matplotlib.pyplot as plt

# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the image
image = cv2.imread("/content/images (1).jpeg")

# Convert the image to grayscale (required for Haar cascades)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(
    gray, 
    minNeighbors=5    # How many neighbors each candidate rectangle should have to retain it
)

if len(faces) > 0:
    print(f"Faces detected: {len(faces)}")
    
    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green rectangle with thickness=2
    
    # Convert image from BGR to RGB for displaying with Matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Display the image with bounding boxes
    plt.imshow(image_rgb)
    plt.title("Face Detected")
    plt.axis("off")  # Turn off axes
    plt.show()
else:
    print("No face detected.")''')