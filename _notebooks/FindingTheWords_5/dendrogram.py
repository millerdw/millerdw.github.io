
from scipy.cluster.hierarchy import dendrogram
import numpy as np

def wrap(text,max_width=100,max_lines=3):
    """wrap text according to max width and max number of lines"""
    lines=int((len(text)-(len(text) % max_width))/max_width)+1
    return "...\n".join([text[i*max_width:(i+1)*max_width] for i in range(min(lines,max_lines))])\
            +('...' if len(text)>max_width*max_lines else '')
  
    
def leaf_label_function(labels, counts, children, i):
    """generate label for each node based on labels for members of node"""
    if i < len(children): # leaf node
        return '({0}): ({1})'.format(int(counts[i]),
                                     wrap(' | '.join(labels[np.random.choice(children[i],
                                                                             min(10,len(children[i])), 
                                                                             replace=False)])))
    else: # non-leaf node (cluster)
        return leaf_label_function(labels, counts, children, i-len(children)-1)
    
    
def plot_dendrogram(model, questions=None, **kwargs):
    """plot dendrogram from scikit-learn agglomerative (hierarchical) clustering object"""
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    children = [None for _ in range(model.children_.shape[0])]
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        current_children=[]
        for child_idx in merge:
            if child_idx < n_samples:  # leaf node
                current_count += 1
                current_children += [child_idx]
            else:
                current_count += counts[child_idx - n_samples]
                current_children += children[child_idx - n_samples]
        counts[i] = current_count
        children[i] = current_children
    
    linkage_matrix = np.column_stack([model.children_, 
                                      model.distances_,
                                      counts]).astype(float)

    # calculate dendrogram statistics
    R = dendrogram(linkage_matrix, no_plot=True, **kwargs)

    # Plot the corresponding dendrogram
    if not kwargs.get('ax', False):
        ax=plt.gca()
    if questions is None:
        dendrogram(linkage_matrix, ax=ax, **kwargs)
    else:
        dendrogram(linkage_matrix, leaf_label_func = lambda i: leaf_label_function(questions, counts, children, i), ax=ax, **kwargs)
    
    for i, d, c in zip(R['icoord'], R['dcoord'], R['color_list']):
        x = 0.5*sum(i[1:3])
        y = 0.5*sum(d[1:3])
        ax.plot(y, x, 'o', c=c)
#         ax.annotate("%.3g" % y, (y, x), xytext=(+20, +5),
#                     textcoords='offset points',
#                     va='top', ha='center')
            