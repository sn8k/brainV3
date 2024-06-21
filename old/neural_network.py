# neural_network.py
# Version 3.0

import torch
import torch.nn as nn
import torch.optim as optim
import random
import json
import logging
import os
from web_searcher import WebSearcher
from threading import Timer, Thread, Event
import time
import requests
import pickle

class NeuralNetwork(nn.Module):
    def __init__(self, num_inputs, num_hidden, num_outputs):
        super(NeuralNetwork, self).__init__()
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs
        self.hidden_layer = nn.Linear(num_inputs, num_hidden)
        self.output_layer = nn.Linear(num_hidden, num_outputs)
        self.plugins = []
        self.data_directory = 'data'
        self.dictionary_file = 'dictionary.txt'
        self.dictionary_url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
        self.words = self.load_dictionary()
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        logging.info(f'Neural Network initialized with {num_inputs} inputs, {num_hidden} hidden neurons, and {num_outputs} outputs')

        # Initialize curiosity
        self.curiosity_interval = 300  # Time interval in seconds
        self.curiosity_event = Event()
        self.curiosity_thread = Thread(target=self.periodic_search_and_learn)
        self.curiosity_thread.start()

    def forward(self, x):
        x = torch.relu(self.hidden_layer(x))
        x = torch.sigmoid(self.output_layer(x))
        return x

    def feedforward(self, inputs):
        inputs = torch.tensor(inputs, dtype=torch.float32)
        output = self.forward(inputs)
        logging.info(f'Feedforward with inputs: {inputs}, outputs: {output}')
        return output.detach().numpy()

    def train_network(self, training_data, learning_rate, epochs):
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        logging.info(f'Training started for {epochs} epochs with learning rate {learning_rate}')
        for epoch in range(epochs):
            for inputs, targets in training_data:
                inputs = torch.tensor(inputs, dtype=torch.float32)
                targets = torch.tensor(targets, dtype=torch.float32)

                optimizer.zero_grad()
                outputs = self.forward(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
        logging.info('Training completed')

    def modify_code(self):
        with torch.no_grad():
            if random.random() < 0.05:
                layer = self.hidden_layer
                weights = layer.weight
                random_weight = random.uniform(-1, 1)
                neuron_index = random.randint(0, weights.size(0) - 1)
                weight_index = random.randint(0, weights.size(1) - 1)
                weights[neuron_index, weight_index] = random_weight
                logging.info(f'Modified weight of neuron {neuron_index}, weight {weight_index} to {random_weight}')

    def search_and_learn(self, query):
        searcher = WebSearcher()
        results = searcher.search(query)
        new_knowledge = results
        logging.info(f'New Knowledge Acquired from query "{query}": {new_knowledge}')
        self.save_raw_data(query, new_knowledge)
        self.modify_code_with_knowledge(new_knowledge)

    def modify_code_with_knowledge(self, knowledge):
        if any("Neural" in item['title'] for item in knowledge):
            self.modify_code()

    def save_state(self, filename):
        state = {
            'model_state_dict': self.state_dict()
        }
        with open(filename, 'wb') as file:
            pickle.dump(state, file)
        logging.info(f'State saved to {filename}')

    def load_state(self, filename):
        with open(filename, 'rb') as file:
            state = pickle.load(file)
        self.load_state_dict(state['model_state_dict'])
        logging.info(f'State loaded from {filename}')

    def load_plugin(self, plugin):
        self.plugins.append(plugin)
        logging.info(f'Loaded plugin: {plugin.__class__.__name__}')

    def handle_message(self, message):
        if message.lower() == "help":
            return self.get_help()
        for plugin in self.plugins:
            response = plugin.process(message)
            if response:
                logging.info(f'Plugin {plugin.__class__.__name__} handled message: {message}')
                return response
        return "I don't understand."

    def save_raw_data(self, query, data):
        filename = os.path.join(self.data_directory, f'data_{len(os.listdir(self.data_directory)) + 1}.json')
        with open(filename, 'w') as file:
            json.dump({'query': query, 'data': data}, file)
        logging.info(f'Raw data saved to {filename}')

    def count_data_files(self):
        return len(os.listdir(self.data_directory))

    def get_plugin_commands(self):
        commands = {}
        for plugin in self.plugins:
            commands.update(plugin.get_commands())
        return commands

    def get_help(self):
        help_text = "Available commands:\n"
        commands = self.get_plugin_commands()
        for command in commands.keys():
            help_text += f"- {command}\n"
        return help_text

    def periodic_search_and_learn(self):
        while not self.curiosity_event.is_set():
            random_query = self.generate_random_query()
            self.search_and_learn(random_query)
            time.sleep(self.curiosity_interval)

    def generate_random_query(self):
        return random.choice(self.words)

    def load_dictionary(self):
        if not os.path.exists(self.dictionary_file):
            self.download_dictionary()
        with open(self.dictionary_file, 'r') as file:
            words = file.read().splitlines()
        return words

    def download_dictionary(self):
        response = requests.get(self.dictionary_url)
        with open(self.dictionary_file, 'wb') as file:
            file.write(response.content)
        logging.info(f'Dictionary downloaded from {self.dictionary_url}')

    def get_statistics(self):
        stats = {
            'num_hidden_neurons': self.num_hidden,
            'num_output_neurons': self.num_outputs,
            'num_data_files': self.count_data_files(),
            'next_search_in': self.curiosity_interval - (time.time() % self.curiosity_interval)
        }
        return stats
