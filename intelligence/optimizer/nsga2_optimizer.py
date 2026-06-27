# intelligence/optimizer/nsga2_optimizer.py

from typing import Dict, List, Any
import random
import numpy as np
from intelligence.optimizer.pareto_engine import ParetoEngine

class NSGA2Optimizer:
    def __init__(self):
        self.pareto = ParetoEngine()

    def optimize(
        self,
        candidates: List[Dict[str, Any]],
        objectives: List[str],
        maximize_flags: List[bool],
        population_size: int = 100,
        generations: int = 50,
        mutation_rate: float = 0.05,
        crossover_rate: float = 0.8
    ) -> List[Dict[str, Any]]:
        """
        Runs NSGA-II to find the Pareto-optimal candidates directly from a candidate pool.
        For candidate selection, each individual represents a ranking preference vector (weights).
        """
        if not candidates:
            return []
            
        n_objectives = len(objectives)
        
        # 1. Create initial population of preference weights
        population = []
        for _ in range(population_size):
            individual = [random.random() for _ in range(n_objectives)]
            total = sum(individual) or 1.0
            population.append([x / total for x in individual])
            
        for gen in range(generations):
            # 2. Crossover & Mutation to create offspring
            offspring = []
            for i in range(0, population_size, 2):
                parent1 = population[i]
                parent2 = population[(i + 1) % population_size]
                
                # Single-point crossover
                if random.random() < crossover_rate:
                    cut = random.randint(1, n_objectives - 1) if n_objectives > 1 else 0
                    child1 = parent1[:cut] + parent2[cut:]
                    child2 = parent2[:cut] + parent1[cut:]
                else:
                    child1 = parent1.copy()
                    child2 = parent2.copy()
                    
                # Mutation
                for child in [child1, child2]:
                    for j in range(n_objectives):
                        if random.random() < mutation_rate:
                            child[j] = random.random()
                    total = sum(child) or 1.0
                    offspring.append([x / total for x in child])
                    
            # Combine parents and offspring
            combined = population + offspring
            
            # Evaluate all individuals by computing the best candidate they rank as Rank 1
            evaluated_frontier_candidates = []
            for ind in combined:
                # Calculate weighted score for each candidate
                best_cand = None
                best_score = -999999.0
                
                for cand in candidates:
                    cand_objs = cand.get("objectives", {})
                    score = 0.0
                    for k, obj_key in enumerate(objectives):
                        val = cand_objs.get(obj_key, 50.0)
                        # Normalize val to [0, 100] scale dynamically if needed
                        # Maximize vs minimize
                        if not maximize_flags[k]:
                            score += ind[k] * (100.0 - min(100.0, val))
                        else:
                            score += ind[k] * val
                            
                    if score > best_score:
                        best_score = score
                        best_cand = cand
                        
                if best_cand and best_cand not in evaluated_frontier_candidates:
                    evaluated_frontier_candidates.append(best_cand)
                    
            # Filter non-dominated candidates from the evaluated list
            frontier = self.pareto.find_pareto_frontier(
                evaluated_frontier_candidates,
                objectives,
                maximize_flags
            )
            
            # Keep population of weights aligned with top fitnesses
            population = combined[:population_size]
            
        # Return Pareto-optimal candidates discovered
        return frontier
