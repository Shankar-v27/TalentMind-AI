# intelligence/optimizer/genetic_optimizer.py

from typing import Dict, List, Any
import random

class GeneticOptimizer:
    def evolve_selection(
        self,
        candidates: List[Dict[str, Any]],
        fitness_fn: Any,
        population_size: int = 50,
        generations: int = 30
    ) -> Dict[str, Any]:
        """
        Runs a standard genetic algorithm to find the single candidate that maximizes a fitness function.
        Supports tournament selection.
        """
        if not candidates:
            return {}
            
        # Population is represented as indices of candidates
        pop = [random.randint(0, len(candidates) - 1) for _ in range(population_size)]
        
        best_candidate = None
        best_fitness = -999999.0
        
        for gen in range(generations):
            # Evaluate fitness
            fits = []
            for idx in pop:
                fit_val = fitness_fn(candidates[idx])
                fits.append(fit_val)
                if fit_val > best_fitness:
                    best_fitness = fit_val
                    best_candidate = candidates[idx]
                    
            # Tournament selection
            new_pop = []
            for _ in range(population_size):
                # Pick 3 tournament entrants
                i1, i2, i3 = random.sample(range(population_size), 3)
                best_idx = i1
                if fits[i2] > fits[best_idx]:
                    best_idx = i2
                if fits[i3] > fits[best_idx]:
                    best_idx = i3
                new_pop.append(pop[best_idx])
                
            # Crossover & Mutation (discrete swaps)
            for idx in range(population_size):
                if random.random() < 0.15: # mutation rate
                    new_pop[idx] = random.randint(0, len(candidates) - 1)
                    
            pop = new_pop
            
        return {
            "best_candidate": best_candidate,
            "fitness": best_fitness
        }
