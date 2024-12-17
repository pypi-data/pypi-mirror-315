import networkx as nx
import numpy as np
import itertools
import random
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
import time
import matplotlib.pyplot as plt
import warnings

import BayesianNetworkVisualizations as bnv

import mlflow
import pickle
from datetime import datetime
import os
from pathlib import Path

import logging

import concurrent.futures

# Helper functions - ensure directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Configure logging
date_today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_directory = 'outputs/logs/'
ensure_directory_exists(log_directory)  # Ensure the log directory exists
filename = f'{log_directory}{date_today}_create_cpds.log'

# Create logger for 'create_cpds'
cgt_logger = logging.getLogger('create_cpds')
cgt_logger.setLevel(logging.DEBUG)  # Set the minimum log level

# Create file handler which logs messages to a file
cgt_handler = logging.FileHandler(filename)
cgt_handler.setLevel(logging.DEBUG)  # Set the handler's log level

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
cgt_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
cgt_logger.addHandler(cgt_handler)
cgt_logger.addHandler(console_handler)


# It's better to handle specific warnings locally rather than suppressing them globally.
# warnings.filterwarnings('ignore') but the below can be commented to remove this specific warning.

"""
Often the code shows a warning. Similar to this:
    WARNING:pgmpy:Probability values don't exactly sum to 1. Differ by: 1.1102230246251565e-16. Adjusting values.
This warning is normal and can be supressed.
"""
#import warnings     
#warnings.filterwarnings('ignore') 

#SET UP DEFAULT_DIR
DEFAULT_DIR = 'datasets/rmulaudzi/'
ensure_directory_exists(DEFAULT_DIR)

# Function: Add Noise to Data
def add_noise_to_data(data, noise_level=0.1):
    """
    Adds random noise to the data.

    Parameters:
    data (DataFrame): The dataset to which noise is to be added.
    noise_level (float): The proportion of data to be noised, between 0 and 1.

    Returns:
    DataFrame: The dataset with added noise.

    Raises:
    ValueError: If noise_level is not between 0 and 1.
    """
    if not 0 <= noise_level <= 1:
        raise ValueError("Noise level must be between 0 and 1")
    noisy_data = data.copy()
    num_rows, num_cols = noisy_data.shape
    total_values = num_rows * num_cols
    num_noisy_values = int(total_values * noise_level)
    for _ in range(num_noisy_values):
        row_index = np.random.randint(num_rows)
        col_index = np.random.randint(num_cols)
        column_name = noisy_data.columns[col_index]
        max_value = noisy_data[column_name].max()
        noisy_data.iat[row_index, col_index] = np.random.randint(max_value + 1)
    return noisy_data

# Function: Add Missing Data
def add_missing_data(data, missing_data_percentage=0.1):
    """
    Introduces missing data into the dataset.

    Parameters:
    data (DataFrame): The dataset.
    missing_data_percentage (float): The proportion of data to be made missing, between 0 and 1.

    Returns:
    DataFrame: The dataset with missing data.

    Raises:
    ValueError: If missing_data_percentage is not between 0 and 1.
    """
    if not 0 <= missing_data_percentage <= 1:
        raise ValueError("Missing data percentage must be between 0 and 1")
    missing_data = data.copy()
    num_rows, num_cols = missing_data.shape
    total_values = num_rows * num_cols
    num_missing_values = int(total_values * missing_data_percentage)
    for _ in range(num_missing_values):
        row_index = np.random.randint(num_rows)
        col_index = np.random.randint(num_cols)
        missing_data.iat[row_index, col_index] = np.nan
    return missing_data

# Function: Generate Edges
def generate_edges(num_nodes, name_of_nodes, max_indegree, density):
    """
    Generates edges for the Bayesian Network based on given parameters.

    Parameters:
    num_nodes (int): Number of nodes in the network.
    name_of_nodes (list): List of node names.
    max_indegree (int): Maximum in-degree for any node in the network.
    density (str): Density of the network ('normal', 'sparse', 'dense').

    Returns:
    list: List of edges for the Bayesian Network.

    Raises:
    ValueError: For invalid input parameters.
    """
    if not isinstance(num_nodes, int) or num_nodes <= 0:
        raise ValueError("num_nodes must be a positive integer")
    if not isinstance(max_indegree, int) or max_indegree < 1:
        raise ValueError("max_indegree must be a positive integer")
    all_possible_edges = list(itertools.permutations(name_of_nodes, 2))
    random.shuffle(all_possible_edges)
    graph = nx.DiGraph()
    edges = set()
    for edge in all_possible_edges:
        if len([e for e in edges if e[1] == edge[1]]) < max_indegree:
            graph.add_edge(*edge)
            if nx.is_directed_acyclic_graph(graph):
                edges.add(edge)
            else:
                graph.remove_edge(*edge)
    max_edges = len(edges)
    edge_count = {"normal": max_edges // 2, "sparse": max_edges // 4, "dense": max_edges}.get(density, max_edges)
    return list(edges)[:edge_count]

#Optimized Edge Generation
def generate_edges_optimized(num_nodes, name_of_nodes, max_indegree, density):
    all_possible_edges = list(itertools.permutations(name_of_nodes, 2))
    random.shuffle(all_possible_edges)
    graph = nx.DiGraph()
    edges = set()
    while all_possible_edges and len(edges) < max_edges:
        edge = all_possible_edges.pop()
        if len([e for e in edges if e[1] == edge[1]]) < max_indegree:
            graph.add_edge(*edge)
            if nx.is_directed_acyclic_graph(graph):
                edges.add(edge)
            else:
                graph.remove_edge(*edge)
    # Adjust edge count based on the specified density
    edge_count = {"normal": len(edges) // 2, "sparse": len(edges) // 4, "dense": len(edges)}.get(density, len(edges))
    return list(edges)[:edge_count]

# Function: Generate CPDs

# Helper functions _prepare_nodes_and_model, _generate_samples, and _visualize_model to be defined accordingly.
def _prepare_nodes_and_model(num_nodes, node_cardinality, max_indegree, density):
    """
    Prepares node names, generates edges, and initializes the Bayesian Network model.

    Parameters:
    num_nodes (int): Number of nodes in the network.
    node_cardinality (int or dict): Cardinality of nodes.
    max_indegree (int): Maximum in-degree for any node.
    density (str): Network density ('normal', 'sparse', 'dense').

    Returns:
    tuple: Tuple containing node names, edges, model, and node cardinality dictionary.

    Raises:
    ValueError: If node_cardinality is neither an integer nor a dictionary.
    """
    # Generate node names based on node_cardinality type
    if isinstance(node_cardinality, dict) and len(node_cardinality) > 1:
        existing_names = set(node_cardinality.keys()) - {'default'}
        name_of_nodes = list(existing_names)
        additional_nodes_needed = num_nodes - len(existing_names)

        if additional_nodes_needed > 0:
            additional_names = [f'N{i}' for i in range(len(existing_names), num_nodes)]
            name_of_nodes.extend(additional_names)
    else:
        name_of_nodes = [f'N{i}' for i in range(num_nodes)]

    # Remove 'default' if it accidentally becomes a node name
    if 'default' in name_of_nodes:
        index = name_of_nodes.index('default')
        del name_of_nodes[index]

    # Generate edges for the Bayesian Network
    edges = generate_edges(num_nodes, name_of_nodes, max_indegree, density)

    # Initialize Bayesian Network model with generated edges
    model = BayesianNetwork(edges)

    # Setup node cardinality dictionary
    if isinstance(node_cardinality, int):
        node_cardinality_dict = {node: node_cardinality for node in name_of_nodes}
    elif isinstance(node_cardinality, dict):
        default_cardinality = node_cardinality.get('default', 2)
        node_cardinality_dict = {node: node_cardinality.get(node, default_cardinality) for node in name_of_nodes}
    else:
        raise ValueError("node_cardinality must be an integer or a dictionary")

    # Remove 'default' from node_cardinality dictionary if present
    if 'default' in node_cardinality_dict:
        del node_cardinality_dict['default']

    return name_of_nodes, edges, model, node_cardinality_dict


def _generate_samples(model, sample_size, noise, missing_data_percentage):
    """
    Generates samples from the Bayesian Network model, applying noise and missing data.

    Parameters:
    model (BayesianNetwork): The Bayesian Network model.
    sample_size (int): Number of samples to generate.
    noise (float): Noise level to be added.
    missing_data_percentage (float): Percentage of missing data in the samples.

    Returns:
    DataFrame: Generated samples with noise and missing data.
    """
    sampler = BayesianModelSampling(model)
    samples = sampler.forward_sample(size=sample_size)

    if noise > 0:
        samples = add_noise_to_data(samples, noise_level=noise)

    if missing_data_percentage > 0:
        samples = add_missing_data(samples, missing_data_percentage=missing_data_percentage)

    return samples

def _visualize_model(model, cpds, ground_truth_model=None, show_plot=True, save_dir="output/graphs", save_path="bayesian_network.png"):
    """
    Visualizes the Bayesian Network and its Conditional Probability Distributions (CPDs).

    Parameters:
    model (BayesianNetwork): The Bayesian Network model.
    cpds (dict): Dictionary of Conditional Probability Distributions.
    """
    for node, cpd in cpds.items():
        print(f"CPD for {node}:\n{cpd}")

    # Visualization logic using a Bayesian Network visualization library
    visualize_bayesian_network(model, ground_truth_model=None, show_plot=True, save_dir="output/graphs", save_path="bayesian_network.png")

def visualize_bayesian_network(model, ground_truth_model=None, show_plot=True, save_dir="output/graphs", save_path="bayesian_network.png"):
    """
    Visualize the Bayesian network with nodes and directed edges. Optionally, compare with ground truth.

    Parameters:
    - model (BayesianNetwork): The Bayesian network model from pgmpy.
    - ground_truth_model (BayesianNetwork, optional): The ground truth Bayesian network model for comparison.
    - show_plot (bool, optional): Whether to display the plot. Defaults to True.
    - save_path (str, optional): File path to save the generated image. Defaults to 'bayesian_network.png'.
    """
    if not isinstance(model, BayesianNetwork):
        raise ValueError("Model must be a BayesianNetwork object from pgmpy")

    cpds = model.cpds

    if not cpds:
        raise ValueError("Model must be a BayesianNetwork with valid CPDs")

    # Ensure save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(save_dir, f"{timestamp}_{filename}.png")

    # Initialize a directed graph
    graph = nx.DiGraph()

    # Add nodes and edges to the graph
    for cpd in cpds:
        graph.add_node(cpd.variable)
        for evidence in cpd.variables[1:]:  # Skipping the first variable which is the node itself
            graph.add_edge(evidence, cpd.variable)

    # Generate positions for each node for consistent graphs
    pos = nx.layout.circular_layout(graph)

    # Initialize edge colors
    edge_colors = {}

    # Compare with ground truth if provided
    if ground_truth_model:
        ground_truth_edges = set(ground_truth_model.edges)
        learned_edges = set(model.edges)

        # Compute edges that are an exact match (in green)
        exact_match_edges = ground_truth_edges.intersection(learned_edges)

        # Compute edges with the wrong direction (in red)
        wrong_direction_edges = {
            edge for edge in learned_edges if edge[::-1] in ground_truth_edges
        }

        # Calculate SHD
        shd = len(ground_truth_edges - exact_match_edges) + len(wrong_direction_edges)

        # Assign colors to edges
        edge_colors = {edge: 'green' if edge in exact_match_edges else 'red' if edge in wrong_direction_edges else 'black' for edge in graph.edges}

        # Display SHD and legend with colors
        plt.figtext(1.05, 0.75, f"SHD Result: {shd}", fontsize=12, color="black", verticalalignment="center", horizontalalignment="left")
        plt.figtext(1.05, 0.70, f"Missing Edges: {len(ground_truth_edges - exact_match_edges)}", fontsize=12, color="grey", verticalalignment="center", horizontalalignment="left")
        plt.figtext(1.05, 0.65, "Exact Match", fontsize=12, color="green", verticalalignment="center", horizontalalignment="left")
        plt.figtext(1.05, 0.60, "Changed Direction", fontsize=12, color="red", verticalalignment="center", horizontalalignment="left")
        plt.figtext(1.05, 0.55, "New Addition", fontsize=12, color="black", verticalalignment="center", horizontalalignment="left")

    # Draw the graph with edge coloring
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", edge_color=[edge_colors.get(edge, 'black') for edge in graph.edges], font_size=16, arrowsize=20)

    # Draw edge labels (conditional dependencies)
    edge_labels = {(parent, child): f"P({child}|{parent})" for parent, child in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=12, label_pos=0.5)

    # Compute and display confusion matrix below the graph
    if ground_truth_model:
        y_true = np.array([1 if edge in ground_truth_edges else 0 for edge in learned_edges])
        y_pred = np.array([1 if edge in learned_edges else 0 for edge in ground_truth_edges])

        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap="Blues")  # This will automatically create a new figure for the confusion matrix

    if show_plot:
        # Show the plot
        plt.show()

    # Save the figure to a file
    # Save the figure to a file
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()

    print(f"Visualization saved to {save_path}")

# Function: Apply Skew
import numpy as np

def apply_skew(values, max_skew):
    """
    Applies random skew to the CPD values if max_skew is greater than 1.

    Parameters:
    values (ndarray): Array of CPD values.
    max_skew (float): Maximum skewness factor.

    Returns:
    ndarray: Skewed CPD values.
    """
    if max_skew is None or max_skew == 0:
        return values  # No skew applied if max_skew is None or not greater than 1

    num_states = values.shape[0]
    if max_skew >= 1:
        random_skew_factors = np.random.uniform(1, max_skew, size=num_states)
    else:
        random_skew_factors = np.random.uniform(max_skew, 1, size=num_states)

    for i in range(num_states):
        values[i, :] *= random_skew_factors[i]

    values /= values.sum(axis=0, keepdims=True)
    return values

def generate_cpds(model, node_cardinality, max_skew):
    """
    Generates CPDs for the Bayesian Network, applying random skew based on max_skew.

    Parameters:
    model (BayesianNetwork): The Bayesian Network model.
    node_cardinality (dict): Dictionary of node cardinalities.
    max_skew (float): Maximum skewness factor to be applied.

    Returns:
    dict: Dictionary of generated CPDs.

    Raises:
    ValueError: If max_skew is not a positive float.
    """
    # Check if max_skew is of the correct type
    if max_skew is not None and not isinstance(max_skew, (float, int)):
        cgt_logger.error("max_skew must be a float or an integer")
        raise ValueError("max_skew must be a float or an integer.")

    # Check if max_skew is greater than 0
    if max_skew is not None and max_skew < 0:
        cgt_logger.error("max_skew must be a positive value greater than 0")
        raise ValueError("max_skew must be a positive value greater than 0.")

    cpds = {}
    
    for node in model.nodes():
        try:
            parents = model.get_parents(node)
            variable_card = node_cardinality.get(node, 2)  # Default cardinality
            parent_cardinalities = [node_cardinality.get(parent, 2) for parent in parents]
            #values = np.ones((variable_card, np.prod(parent_cardinalities) if parents else 1))
            values = np.random.rand(variable_card, np.prod(parent_cardinalities) if parents else 1)

            # Normalize the values to ensure they sum up to 1
            values = values / values.sum(axis=0, keepdims=True)
    
            # Apply random skew if max_skew is greater than 1
            values = apply_skew(values, max_skew)
    
            cpd = TabularCPD(variable=node, variable_card=variable_card, values=values, evidence=parents, evidence_card=parent_cardinalities)
            cpds[node] = cpd
        except Exception as e:
            cgt_logger.error("Error while generating CPD for node {%s}:",node)
            raise ValueError(f"Error while generating CPD for node {node}: {e}")

    return cpds


#Parallel CPD Generation
def generate_cpds_concurrently(model, node_cardinality, max_skew):
    """
    Generates CPDs for the Bayesian Network in parallel, applying random skew based on max_skew.
    This function assumes generate_cpds_vectorized is correctly defined to take the model,
    node_cardinality, and max_skew as arguments.

    Parameters:
    model (BayesianNetwork): The Bayesian Network model.
    node_cardinality (dict): Dictionary of node cardinalities.
    max_skew (float): Maximum skewness factor to be applied.

    Returns:
    dict: Dictionary of generated CPDs.
    """
    cpds = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_cpds = {executor.submit(generate_cpds, model, {node: node_cardinality[node]}, max_skew): node for node in model.nodes()}
        for future in concurrent.futures.as_completed(future_cpds):
            node = future_cpds[future]
            try:
                cpd = future.result()  # This should now correctly call generate_cpds_vectorized
                cpds.update(cpd)  # Assuming generate_cpds_vectorized returns a dict {node: cpd}
            except Exception as exc:
                print(f'Generated CPD for node {node} generated an exception: {exc}')
    return cpds


# Function: Create PGM

def create_pgm(num_nodes=3, node_cardinality=2, max_indegree=2, density="normal", 
               skew=1, noise=0, missing_data_percentage=0, sample_size=1000, visualize=True, 
               artifacts_output_dir = 'outputs', run_id=None, experiment_id=None): #, mlflow_uri='experiment_tracking/mlruns/'):
    """
    Main function to create a probabilistic graphical model (PGM).

    Parameters:
    num_nodes (int): Number of nodes in the PGM.
    node_cardinality (int or dict): Cardinality of nodes.
    max_indegree (int): Maximum in-degree for any node.
    density (str): Network density - 'normal', 'sparse', or 'dense'.
    skew (float, int, dict): Skew to be applied.
    noise (float): Noise level to be added to the data.
    missing_data_percentage (float): Percentage of missing data.
    sample_size (int): Number of samples to be generated.
    visualize (bool): Whether to visualize the network and CPDs.
    artifacts_output_dir (str): directory to store created artifacts like the pickle model and sample data
    mlflow_uri (str): directory where mlflow stores it's outputs, if not specific mlruns will be created in . folder

    Returns:
    dict: Dictionary containing the model, samples, and runtime.

    Raises:
    ValueError: For incorrect parameter specifications.
    
    Example uses:
    # Example Usage
    with only defaults
    result = create_pgm()
    
    With specific paramters 1
    result = create_pgm(num_nodes=3, node_cardinality=5, max_indegree=2, density="normal", 
                        skew=0.75, noise=0, missing_data_percentage=0, sample_size=1000, visualize=True)
    result
    
    With specific paramters 2
    g = create_pgm(
        num_nodes=6, 
        node_cardinality={'A': 5, 'default':3}, 
        max_indegree=2, 
        density="normal", 
        skew=1.3, 
        noise=0.5, 
        missing_data_percentage=0, 
        sample_size=1000, 
        visualize=False
    )

    g
    
    in all cases: 
    artifacts_output_dir can be updated to paths where ouputs should be stored
    similarly for mlflow set mlflow_uri
    
    """
    cgt_logger.info("Starting PGM creation")
    
    start_time = time.time()

    sample_size = int(sample_size)

    # Validate input parameters
    if not isinstance(num_nodes, int) or num_nodes <= 0:
        cgt_logger.error("num_nodes must be a positive integer")
        raise ValueError("num_nodes must be a positive integer")
    if not isinstance(max_indegree, int) or max_indegree < 1:
        cgt_logger.error("max_indegree must be a positive integer, set to 2")
        max_indegree = 2
    if density not in ["normal", "sparse", "dense"]:
        cgt_logger.error("density must be 'normal', 'sparse', or 'dense', set to 'normal'")
        density = 'normal'
    if not isinstance(noise, (float, int)) or not 0 <= noise <= 1:
        cgt_logger.error("noise must be a float between 0 and 1, set to 0")
        noise = 0
    if not isinstance(missing_data_percentage, (float, int)) or not 0 <= missing_data_percentage <= 1:
        cgt_logger.error("missing_data_percentage must be a float between 0 and 1, set to 0")
        missing_data_percentage = 0
    if not isinstance(sample_size, int) or sample_size <= 0:
        cgt_logger.error("sample_size must be a positive integer, set to 1000")
        sample_size = 1000
    if not isinstance(visualize, bool):
        cgt_logger.error("visualize must be a boolean value")
        visualize = False
    
    run_name = f"{num_nodes}_{sample_size}_{node_cardinality}_{max_indegree}_{skew}_PGM_GT"
    
    # Node names and edge generation
    try:
        name_of_nodes, edges, model, node_cardinality_dict = _prepare_nodes_and_model(num_nodes, node_cardinality, max_indegree, density)
        cgt_logger.info('Prepared, name_of_nodes, edges, model, node_cardinality_dict = %s, %s, %s, %s', name_of_nodes, edges, model, node_cardinality_dict)

    except Exception as e:
        cgt_logger.error("Error in preparing nodes and model: %s", e)
        raise ValueError(f"Error in preparing nodes and model: {e}")

    # Generate CPDs
    # If skew is None or not greater than 1, set a default positive value
    max_skew = skew if skew is not None and skew > 1 else 1  # Default to 1 (no skew)
    cpds = generate_cpds_concurrently(model, node_cardinality_dict, skew)
    cgt_logger.info("Generated {%s} edges for the Bayesian Network", len(edges))

    # Add CPDs to model and validate
    for cpd in cpds.values():
        model.add_cpds(cpd)
    if not model.check_model():
        cgt_logger.error("Invalid model configuration with \n %s \n", cpd)
        raise ValueError("Invalid model configuration")

    # Sample generation with noise and missing data handling
    try:
        samples = _generate_samples(model, sample_size, noise, missing_data_percentage)
    except Exception as e:
        cgt_logger.error("Error in creating PGM and generating samples: %s", e)
        raise ValueError(f"Error in creating PGM and generating samples: {e}")

    # Visualization if required
    
    if visualize:
        _visualize_model(model, cpds)
    
    end_time = time.time()
    cgt_logger.info("PGM creation completed in %s seconds", end_time - start_time)

    # Save and log the Bayesian Network model as an artifact   
    '''
    #REMOVE FILE SAVES
    
    model_file_pkl = "bayesian_network_model.pkl"
    date_today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    model_file = f"{DEFAULT_DIR}/ground_truth/bn_models/{date_today}_{len(name_of_nodes)}_nodes_{model_file_pkl}"
    '''
    # Define the output directory
    #output_dir = Path(f"{artifacts_output_dir}/bn_models")
    output_dir = os.path.join(DEFAULT_DIR, 'ground_truth', 'bn_models')
    ensure_directory_exists(output_dir)
    
    # Create the output directory if it does not exist
    ensure_directory_exists(output_dir)
    #output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(model_file, "wb") as f:
        pickle.dump(model, f)  # Serialize model using pickle

    # Save and log the samples as an artifact
    samples_file_csv = "generated_samples.csv"
    date_today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    node_names_str = f"{len(name_of_nodes)}_nodes_{sample_size}_sample_size"
    samples_file = f"{DEFAULT_DIR}/ground_truth/data/{date_today}_{node_names_str}_{samples_file_csv}"
    
    # Define the output directory
    #output_dir = Path(f"{artifacts_output_dir}/data")
    output_dir = os.path.join(DEFAULT_DIR, 'ground_truth', 'data')
    # Create the output directory if it does not exist
    #output_dir.mkdir(parents=True, exist_ok=True)
    ensure_directory_exists(output_dir)
    '''
    samples.to_csv(samples_file, index=False)  # Assuming samples is a pandas DataFrame
    
    create_params_dict = {
        "num_nodes": num_nodes,
        "node_cardinality": node_cardinality,
        "max_indegree": max_indegree,
        "density": density,
        "skew": skew,
        "noise": noise,
        "missing_data_percentage": missing_data_percentage,
        "sample_size": sample_size,
        "runtime": end_time - start_time
    }

    createrun_params_dict = {
        "run_name": run_name,
        "run_params": create_params_dict
    }

    create_params_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{run_name}_create_gt_params.json"
    '''
    # Save the data as JSONdatetime
    output_dir = os.path.join(DEFAULT_DIR, 'ground_truth', 'params')
    ensure_directory_exists(output_dir)
    '''
    saved_filepath = utility_function.save_as_json(createrun_params_dict, output_dir, create_params_filename)

    if saved_filepath:
        cgt_logger.info(f"Ground truth parameters saved to {saved_filepath}")
    else:
        cgt_logger.warning("Failed to save Ground truth parameter data.")
    '''
    
    cgt_logger.removeHandler(cgt_handler)
    cgt_handler.close()

    return {'model': model, 'samples': samples, 'runtime': end_time - start_time}


# Example usage
#if __name__ == "__main__":
    # Example call to create_pgm with default parameters
#    result = create_pgm()
#    print(result)


"""
# Example 1: Using default parameters
result = create_pgm()

# Example 2: Specifying parameters
result = create_pgm(
    num_nodes=5,
    node_cardinality=3,
    max_indegree=2,
    density="normal",
    skew=1.5,
    noise=0.1,
    missing_data_percentage=0.05,
    sample_size=1000,
    visualize=True,
    artifacts_output_dir='output_directory'
)

# Example 3: Specifying more detailed parameters
result = create_pgm(
    num_nodes=6,
    node_cardinality={'A': 5, 'default': 3},
    max_indegree=2,
    density="normal",
    skew=1.3,
    noise=0.5,
    missing_data_percentage=0.1,
    sample_size=500,
    visualize=False,
    artifacts_output_dir='output_directory'
)


"""