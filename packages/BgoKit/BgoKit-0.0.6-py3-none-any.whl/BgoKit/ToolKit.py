import numpy as np
import matplotlib.pyplot as plt
import datetime
import platform
import os
from MultiBgolearn.utility import funs


class MultiOpt:
    def __init__(self, vs, scores, names=None):
        """
        ================================================================
        PACKAGE: The Tool Kit of Bgolearn package .
        Author: Bin CAO <binjacobcao@gmail.com> 
        Guangzhou Municipal Key Laboratory of Materials Informatics, Advanced Materials Thrust,
        Hong Kong University of Science and Technology (Guangzhou), Guangzhou 511400, Guangdong, China
        ================================================================
        Please feel free to open issues in the Github :
        https://github.com/Bin-Cao/Bgolearn
        or 
        contact Mr.Bin Cao (bcao686@connect.hkust-gz.edu.cn)
        in case of any problems/comments/suggestions in using the code. 
        ==================================================================
        Thank you for choosing Bgolearn for material design. 
        Bgolearn is developed to facilitate the application of machine learning in research.

        Bgolearn is designed for optimizing single-target material properties. 
        The BgoKit package is being developed to facilitate multi-task design.
        ================================================================
        :param vs: virtual samples, vs .

        :param scores: scores = [score_1,score_2], the scores of different targets

        :param names : default is None, names = [name_1,name_2], the name of two objects 
        example:
        from BgoKit import ToolKit
        # X is the virtual samples
        # score_1, score_2 are output of Bgolearn
        # score_1, _= Mymodel_1.EI() ; score_2, _= Mymodel_2.EI()

        Model = ToolKit.MultiOpt(X,[score_1,score_2])
        Model.BiSearch()
        Model.plot_distribution()
        """
        self.X = np.array(vs)
        self.scores = scores
        self.names = names 
        self.font = {'family' : 'Arial',
                'weight' : 'normal',
                'size'   : 18,
                }
        
        now = datetime.datetime.now()
        self.time = now.strftime('%Y-%m-%d %H:%M:%S')
        os.makedirs('Bgolearn', exist_ok=True)

    def BiSearch(self, ):
        if len(self.scores) == 2: pass
        else: 
            print('Search_bi is implemented for only two design targets')
            raise ValueError

        Tone = (self.scores[0] - self.scores[0].min()) / (self.scores[0].max()-self.scores[0].min())
        Ttwo = (self.scores[1] - self.scores[1].min()) / (self.scores[1].max()-self.scores[1].min())

        pareto_front, index= find_pareto_front(Tone,Ttwo)

        sums = pareto_front[:,0] + pareto_front[:,1]
        opt_index = np.argmax(sums)
        val_one = pareto_front[:,0][opt_index]
        val_two = pareto_front[:,1][opt_index]
        indices = np.where((pareto_front[:,0] == val_one) & (pareto_front[:,1] == val_two))[0]
        write_in_pareto(self.X,self.scores,index)
        xx = np.arange(5,95)/100
        
        fig = plt.figure(figsize=[7,7])
        plt.scatter(Tone, Ttwo, marker='o', edgecolor='gray',label='virtual samples')
        plt.scatter(pareto_front[:,0],pareto_front[:,1], marker='o', c='cyan', edgecolor='k',label='Pareto front')
        plt.scatter(val_one,val_two ,marker='*', c='red', s=150, edgecolor='k',label='candidates')
        plt.plot(xx, val_one+val_two-1*xx,c='y',linestyle='--',alpha=0.6,)
        if self.names == None :
            plt.xlabel('utility values of Object one ',self.font)
            plt.ylabel('utility values of Object two',self.font)
        else : 
            plt.xlabel(f'utility values of {self.names[0]}',self.font)
            plt.ylabel(f'utility values of {self.names[1]}',self.font)
        plt.xlim(-0.05, 1.05)  
        plt.ylim(-0.05, 1.05) 
        plt.legend(fontsize=13,)
        plt.tick_params(labelsize=16)
        plt.legend(fontsize=13,loc=1)
        plt.savefig('ParetoF.png', dpi=400)
        plt.savefig('ParetoF.svg', dpi=400)
        plt.show()

        print('The optimal condidate recommended by BgoKit is :', self.X[indices])

        return self.X[indices]

    def HVSearch(self, y):
        """
        Perform Hypervolume (HV) Search to identify the best candidate for optimization.
        This method is specifically designed for the UCB (Upper Confidence Bound) method
        and requires exactly two design targets.

        Parameters:
        ----------
        y : array-like
            A numpy array of shape (n_samples, 2) containing current data points in the objective space.

        Returns:
        -------
        best_idx : int
            The index of the candidate that provides the highest improvement in hypervolume.
        HV_improve : list
            A list of hypervolume improvements for each candidate.

        Raises:
        -------
        ValueError
            If the method is used for a number of design targets other than two.
        """

        print('Pay attention: This is only available for the UCB method!\n')

        # Check if exactly two design targets are present
        if len(self.scores) != 2:
            print('HVSearch is implemented for only two design targets.')
            raise ValueError("The number of design targets must be exactly two.")

        # Ensure y is a numpy array
        y = np.array(y)
        # Scaling the Pareto front while maintaining its shape
        y[:, 0] = y[:, 0] / y[:, 0].max() * self.scores[0].max() 
        y[:, 1] = y[:, 1] / y[:, 1].max() * self.scores[1].max() 

        # Calculate the current Pareto front and its Lebesgue measure
        pareto_front = funs.get_pareto_front(y, True)
        current_lebesgue_measure = funs.calculate_lebesgue_measure(pareto_front, True)

        index_1 = np.where(self.scores[0] <= pareto_front[:, 0].min())[0]
        index_2 = np.where(self.scores[1] <= pareto_front[:, 1].min())[0]
        merged_indices = np.unique(np.concatenate((index_1, index_2)))


        # Initialize a list to store hypervolume improvements
        HV_improve = []
        HV_index = []

        # Iterate through all candidate points
        for i in range(len(self.scores[0])):
            if i in merged_indices:
                continue
            
            # Create a utility matrix from the score arrays
            # utility_y = np.column_stack((self.scores[0], self.scores[1]))
            # Extract the current candidate's scores
            y_sample = [self.scores[0][i], self.scores[1][i]]
            # Add the candidate to the existing data
            extended_y = np.vstack([y, y_sample])

            # Calculate the new Pareto front and its Lebesgue measure
            new_pareto_front = funs.get_pareto_front(extended_y, True)
            new_lebesgue_measure = funs.calculate_lebesgue_measure(new_pareto_front, True)

            # Compute the hypervolume improvement
            HV_improve.append(new_lebesgue_measure - current_lebesgue_measure)
            HV_index.append(i)
            pass
        # Identify the candidate with the highest hypervolume improvement
        _id = np.argmax(HV_improve)
        best_idx = HV_index[_id]

        fig = plt.figure(figsize=[6,6])
        plt.scatter(self.scores[0], self.scores[1], marker='o', edgecolor='gray',label='Searching space')
        plt.scatter(y[:,0], y[:,1], marker='o', edgecolor='gray',label='Training data')
        plt.scatter(pareto_front[:,0],pareto_front[:,1], marker='o', c='cyan', edgecolor='k',label='Pareto front')
        plt.scatter(self.scores[0][best_idx],self.scores[1][best_idx] ,marker='*', c='red', s=150, edgecolor='k',label='candidates')
    
        if self.names == None :
            plt.xlabel('utility values of Object one ',self.font)
            plt.ylabel('utility values of Object two',self.font)
        else : 
            plt.xlabel(f'utility values of {self.names[0]}',self.font)
            plt.ylabel(f'utility values of {self.names[1]}',self.font)
        #plt.xlim(-0.05, 1.05)  
        #plt.ylim(-0.05, 1.05) 
        plt.legend(fontsize=13,)
        plt.tick_params(labelsize=16)
        plt.legend(fontsize=13,loc=1)
        plt.savefig('HV_UCB.png', dpi=500)
        plt.savefig('HV_UCB.svg', dpi=500)
        plt.show()


        # fig 2
        sorted_data = sorted(zip(pareto_front[:,0],pareto_front[:,1]), key=lambda pair: pair[0])
        x_sorted, y_sorted = zip(*sorted_data)
        fig = plt.figure(figsize=[6,6])
        plt.scatter(y[:,0], y[:,1], marker='o', edgecolor='gray',label='Training data')
        plt.scatter(pareto_front[:,0],pareto_front[:,1], marker='o', c='cyan', edgecolor='k',label='Pareto front')
        plt.scatter(self.scores[0][best_idx],self.scores[1][best_idx] ,marker='*', c='red', s=150, edgecolor='k',label='Candidates')
        for i in range(len(pareto_front[:,0]) - 1):
            plt.plot([x_sorted[i], x_sorted[i+1]], [y_sorted[i], y_sorted[i]], color='gray', linestyle='--', linewidth=2)
            plt.plot([x_sorted[i+1], x_sorted[i+1]], [y_sorted[i], y_sorted[i+1]], color='gray', linestyle='--', linewidth=2)
        
        
        if self.names == None :
            plt.xlabel('utility values of Object one ',self.font)
            plt.ylabel('utility values of Object two',self.font)
        else : 
            plt.xlabel(f'utility values of {self.names[0]}',self.font)
            plt.ylabel(f'utility values of {self.names[1]}',self.font)
        #plt.xlim(-0.05, 1.05)  
        #plt.ylim(-0.05, 1.05) 
        plt.legend(fontsize=13,)
        plt.tick_params(labelsize=16)
        plt.legend(fontsize=13,loc=1)
        plt.savefig('HV_UCB_NOcandidates.png', dpi=500)
        plt.savefig('HV_UCB_NOcandidates.svg', dpi=500)
        plt.show()

        
        print(f"The next recommended data by method EV is: {self.X[best_idx]}")
        print(f'The hypervolume improvement is: {HV_improve[_id]}')

        return self.X[best_idx],best_idx,


    def HVSearch_user(self, y):
        print('================================================')
        print('Please refer to the tutorial at https://github.com/Bgolearn/CodeDemo/tree/main/multiobject_examples_book/MO_selection/EI_HV')
        print('Note: This function is developed for expected improvement and probability improvement. It has not been tested on other UFs yet.')
        print('As this is an educational attempt in the book, it is not recommended for use in real research without rigorous validation.')
        print('================================================')

        # Check if exactly two design targets are present
        if len(self.scores) != 2:
            print('HVSearch is implemented for only two design targets.')
            raise ValueError("The number of design targets must be exactly two.")

        row_num = np.array(y).shape[0]

        scores_1 = self.scores[0][:-row_num]
        scores_2 = self.scores[1][:-row_num]

        y_t1 = self.scores[0][-row_num:]
        y_t2 = self.scores[1][-row_num:]

        y = np.column_stack((y_t1, y_t2))

        # Calculate the current Pareto front and its Lebesgue measure
        pareto_front = funs.get_pareto_front(y, True)
        current_lebesgue_measure = funs.calculate_lebesgue_measure(pareto_front, True)

        
        index_1 = np.where(scores_1 <= pareto_front[:,0].min())[0]
        index_2 = np.where(scores_2 <= pareto_front[:,1].min())[0]
        merged_indices = np.unique(np.concatenate((index_1, index_2)))
  
        # Initialize a list to store hypervolume improvements
        HV_improve = []
        HV_index = []

        

        # Iterate through all candidate points
        for i in range(len(scores_1)):
            if i in merged_indices:
                continue
            
            # Extract the current candidate's scores
            y_sample = [scores_1[i], scores_2[i]]
            # Add the candidate to the existing data
            extended_y = np.vstack([y, y_sample])

            # Calculate the new Pareto front and its Lebesgue measure
            new_pareto_front = funs.get_pareto_front(extended_y, True)
            new_lebesgue_measure = funs.calculate_lebesgue_measure(new_pareto_front, True)

            # Compute the hypervolume improvement
            HV_index.append(i)
            HV_improve.append(new_lebesgue_measure - current_lebesgue_measure)
            pass
        
        # Identify the candidate with the highest hypervolume improvement
        _id = np.argmax(HV_improve)
        best_idx = HV_index[_id]

        fig = plt.figure(figsize=[6,6])
        plt.scatter(scores_1, scores_2, marker='o', edgecolor='gray',label='Searching space')
        plt.scatter(y[:,0], y[:,1], marker='o', edgecolor='gray',label='Training data')
        plt.scatter(pareto_front[:,0],pareto_front[:,1], marker='o', c='cyan', edgecolor='k',label='Pareto front')
        plt.scatter(scores_1[best_idx],scores_2[best_idx] ,marker='*', c='red', s=150, edgecolor='k',label='Candidates')
        
        
        if self.names == None :
            plt.xlabel('utility values of Object one ',self.font)
            plt.ylabel('utility values of Object two',self.font)
        else : 
            plt.xlabel(f'utility values of {self.names[0]}',self.font)
            plt.ylabel(f'utility values of {self.names[1]}',self.font)
        #plt.xlim(-0.05, 1.05)  
        #plt.ylim(-0.05, 1.05) 
        plt.legend(fontsize=13,)
        plt.tick_params(labelsize=16)
        plt.legend(fontsize=13,loc=1)
        plt.savefig('HV_EIorPi.png', dpi=500)
        plt.savefig('HV_EIorPi.svg', dpi=500)
        plt.show()

        # fig2
        sorted_data = sorted(zip(pareto_front[:,0],pareto_front[:,1]), key=lambda pair: pair[0])
        x_sorted, y_sorted = zip(*sorted_data)
        fig = plt.figure(figsize=[6,6])
        plt.scatter(y[:,0], y[:,1], marker='o', edgecolor='gray',label='Training data')
        plt.scatter(pareto_front[:,0],pareto_front[:,1], marker='o', c='cyan', edgecolor='k',label='Pareto front')
        plt.scatter(scores_1[best_idx],scores_2[best_idx] ,marker='*', c='red', s=150, edgecolor='k',label='CCandidates')
        for i in range(len(pareto_front[:,0]) - 1):
            plt.plot([x_sorted[i], x_sorted[i+1]], [y_sorted[i], y_sorted[i]], color='gray', linestyle='--', linewidth=2)
            plt.plot([x_sorted[i+1], x_sorted[i+1]], [y_sorted[i], y_sorted[i+1]], color='gray', linestyle='--', linewidth=2)
        
        
        if self.names == None :
            plt.xlabel('utility values of Object one ',self.font)
            plt.ylabel('utility values of Object two',self.font)
        else : 
            plt.xlabel(f'utility values of {self.names[0]}',self.font)
            plt.ylabel(f'utility values of {self.names[1]}',self.font)
        #plt.xlim(-0.05, 1.05)  
        #plt.ylim(-0.05, 1.05) 
        plt.legend(fontsize=13,)
        plt.tick_params(labelsize=16)
        plt.legend(fontsize=13,loc=1)
        plt.savefig('HV_EIorPi_NOcandidates.png', dpi=500)
        plt.savefig('HV_EIorPi_NOcandidates.svg', dpi=500)
        plt.show()
        
        print(f"The next recommended data by method EV is: {self.X[best_idx]}")
        print(f'The hypervolume improvement is: {HV_improve[_id]}')

        return self.X[best_idx], best_idx,

    def plot_distribution(self):
        plt.figure(figsize=(10, 4))

        for i, task_scores in enumerate(self.scores):
            task_scores = (task_scores - task_scores.min()) / (task_scores.max() - task_scores.min())
            plt.subplot(1, 2, i + 1)
            plt.hist(task_scores, bins=20, alpha=0.7, color='skyblue')
            plt.title(f'Distribution of {self.names[i]}', fontdict=self.font)
            plt.xlabel(f'Score {i + 1}', fontdict=self.font)
            plt.ylabel('Frequency', fontdict=self.font)
            plt.tick_params(axis='both', which='major', labelsize=14)
        plt.tight_layout()
        plt.savefig('distribution.png', dpi=800)
        plt.savefig('distribution.svg', dpi=800)
        plt.show()
        


def is_pareto_efficient(costs):
    """
    Check if a solution is Pareto efficient.
    """
    num_solutions = costs.shape[0]
    is_efficient = np.ones(num_solutions, dtype=bool)

    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] >= c, axis=1)
            is_efficient[i] = True  # Current solution is always part of the Pareto front

    return is_efficient

def find_pareto_front(x_values, y_values):
    """
    Find points belonging to the Pareto front.
    """
    performance_array = np.column_stack((x_values, y_values))
    pareto_front = performance_array[is_pareto_efficient(performance_array)]
    
    return pareto_front,is_pareto_efficient(performance_array)


def update_vs(y,vs):
    train_data = np.array(y)[:,:-2]
    extended_vs = np.vstack([np.array(vs), train_data])
    return extended_vs


def write_in_pareto(vs, scores, index):
    """
    Filters and writes Pareto front data to a file.

    Parameters:
    vs (numpy.ndarray): The data of virtual samples, where each row is a sample.
    scores (list of numpy.ndarray): A list containing two arrays of scores corresponding to the virtual samples.
    index (numpy.ndarray or list): Boolean array or list indicating if a sample is on the Pareto front (True) or not (False).

    Returns:
    numpy.ndarray: The combined data labeled as Pareto front (where index is True).

    Saves:
    A text file './Bgolearn/Paretodata.txt' containing the combined Pareto front data.
    """
    # Convert index to a boolean array if it is not already
    index = np.asarray(index, dtype=bool)
    
    # Filter the data based on the Pareto front index
    pareto_data = vs[index]
    
    # Combine the two score arrays into one
    combined_scores = np.hstack((scores[0][:, np.newaxis], scores[1][:, np.newaxis]))
    
    # Filter the combined scores based on the Pareto front index
    pareto_scores = combined_scores[index]
    
    # Combine pareto_data and pareto_scores into one array
    combined_data = np.hstack((pareto_data, pareto_scores))

    # Generate column names
    num_features = pareto_data.shape[1]
    num_scores = pareto_scores.shape[1]
    feature_names = [f'feature{i+1}' for i in range(num_features)]
    score_names = [f'score{i+1}' for i in range(num_scores)]
    column_names = feature_names + score_names

    # Save the combined data to a text file
    header = ','.join(column_names)
    np.savetxt('./Bgolearn/Paretodata.txt', combined_data, delimiter=',', header=header, comments='', fmt='%s')
    
    return combined_data


