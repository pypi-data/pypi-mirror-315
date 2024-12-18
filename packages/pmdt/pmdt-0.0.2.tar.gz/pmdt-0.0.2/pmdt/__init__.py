import random

import numpy as np

import pandas as pd

from datetime import datetime, timedelta

import matplotlib.pyplot as plt

class Resource:

    def __init__(
        self,
        name: str,
        type: str,
        unit_cost: float = 0.0,
        availability: float = 0.0
    ):
        self.name = name
        self.type = type
        self.unit_cost = unit_cost
        self.availability = availability

class Task:

    def __init__(
        self,
        name: str,
        predecessors: list = None,
        baseline_resources: list = None,
        resources: list = None,
        baseline_duration: float = 0.0,
        direct_cost: float = 0.0,
        indirect_cost: float = 0.0,
        overheads: float = 0.0,
        distribution: str = 'Fixed',
        mean: float = None,
        stdev: float = None,
        params: dict = None,
    ):
        self.name = name
        self.predecessors = predecessors if predecessors is not None else []
        self.baseline_resources = baseline_resources if baseline_resources is not None else []
        self.resources = resources if resources is not None else []
        self.baseline_duration = baseline_duration
        self.direct_cost = direct_cost
        self.indirect_cost = indirect_cost
        self.overheads = overheads
        self.successors = []
        self.duration = baseline_duration if baseline_duration is not None else 0.0
        self.es = 0
        self.ef = 0
        self.ls = 0
        self.lf = 0
        self.slack = 0
        self.critical = True
        self.distribution = distribution
        self.mean = mean if mean is not None else baseline_duration
        self.stdev = stdev
        self.params = params if params is not None else {}
        self.criticality = 0.0
        self.total_cost = 0.0

        self._calculate_duration()
        self._calculate_cost()

    def _calculate_duration(self):
        if self.baseline_resources:
            scaling_factors = []
            for resource, requirement in self.baseline_resources:
                allocated = next(
                    (allocated for res,
                     allocated in self.resources if res.name == resource.name),
                    None
                )
                if resource.type == 'Work':
                    if allocated is None or allocated <= 0:
                        scaling_factors.append(float('inf'))
                    else:
                        scaling_factors.append(requirement / allocated)
                elif resource.type == 'Material' and (allocated is None or allocated < requirement):
                    self.duration = float('inf')
                    return
            self.duration = self.baseline_duration / \
                min(scaling_factors) if scaling_factors else self.baseline_duration
        else:
            self.duration = self.baseline_duration

    def _calculate_cost(self):
        if self.baseline_resources:
            direct_cost_work = sum(
                resource.unit_cost * units * self.baseline_duration
                for resource, units in self.baseline_resources if resource.type == 'Work'
            )
            direct_cost_material = sum(
                resource.unit_cost * units
                for resource, units in self.resources if resource.type == 'Material'
            )
            direct_cost_cost = sum(
                resource.unit_cost
                for resource, units in self.baseline_resources if resource.type == 'Cost'
            )
            self.direct_cost = direct_cost_work + direct_cost_material + direct_cost_cost
        self.indirect_cost = self.overheads * \
            self.duration if self.overheads else self.indirect_cost
        self.total_cost = self.direct_cost + self.indirect_cost

    def _add_predecessor(self, predecessor, precedence_type, lag):
        if (predecessor, precedence_type, lag) not in self.predecessors:
            self.predecessors.append((predecessor, precedence_type, lag))
            predecessor._add_successor(self, precedence_type, lag)

    def _add_successor(self, successor, precedence_type, lag):
        if (successor, precedence_type, lag) not in self.successors:
            self.successors.append((successor, precedence_type, lag))
            successor._add_predecessor(self, precedence_type, lag)

    def _sample_duration(self):
        if self.distribution == 'normal':
            return max(0, self.mean + self.stdev * self._pseudo_random())
        elif self.distribution == 'uniform':
            low = self.params.get('low', self.mean - self.stdev)
            high = self.params.get('high', self.mean + self.stdev)
            return self._uniform_random(low, high)
        elif self.distribution == 'exponential':
            rate = 1 / self.mean if self.mean > 0 else 1.0
            return self._exponential_random(rate)
        elif self.distribution == 'log-normal':
            return self._log_normal_random(self.mean, self.stdev)
        elif self.distribution == 'triangular':
            low = self.params.get('low', self.mean - self.stdev)
            high = self.params.get('high', self.mean + self.stdev)
            mode = self.params.get('mode', self.mean)
            return self._triangular_random(low, mode, high)
        elif self.distribution == 'gamma':
            shape = self.params.get('shape', (self.mean / self.stdev) ** 2)
            scale = self.stdev ** 2 / self.mean
            return self._gamma_random(shape, scale)
        elif self.distribution == 'weibull':
            shape = self.params.get('shape', 2.0)
            scale = self.mean
            return self._weibull_random(shape, scale)
        elif self.distribution == 'beta':
            alpha = self.params.get('alpha', 2)
            beta = self.params.get('beta', 2)
            low = self.params.get('low', 0)
            high = self.params.get('high', 1)
            beta_sample = self._beta_random(alpha, beta)
            return low + beta_sample * (high - low)
        elif self.distribution == 'student-t':
            df = self.params.get('df', 10)
            return self._student_t_random(df)
        elif self.distribution == 'fixed':
            return self.duration

    def _pseudo_random(self):
        return random.random()

    def _uniform_random(self, low, high):
        return low + self._pseudo_random() * (high - low)

    def _exponential_random(self, rate):
        return -1 / rate * self._pseudo_random()

    def _log_normal_random(self, mean, stdev):
        variance = stdev ** 2
        mu = (2 * mean ** 2) / (mean ** 2 + variance)
        sigma = (variance / mean ** 2) ** 0.5
        return max(0, self._pseudo_random() * sigma + mu)

    def _triangular_random(self, low, mode, high):
        u = self._pseudo_random()
        if u < (mode - low) / (high - low):
            return low + ((mode - low) * u) ** 0.5
        return high - ((high - mode) * (1 - u)) ** 0.5

    def _gamma_random(self, shape, scale):
        return shape * scale * self._pseudo_random()

    def _weibull_random(self, shape, scale):
        return scale * (-1.0 * self._pseudo_random()) ** (1.0 / shape)

    def _beta_random(self, alpha, beta):
        x = sum(self._pseudo_random() for _ in range(alpha))
        y = sum(self._pseudo_random() for _ in range(beta))
        return x / (x + y) if (x + y) > 0 else 0.5

    def _student_t_random(self, df):
        return self.mean + self.stdev * ((self._pseudo_random() - 0.5) * 2 * df ** 0.5)


class Project:
    def __init__(
        self,
        name: str,
        start_date: int,
        tasks: list,
        overheads: float = 0.0,
    ):
        self.name = name
        self.start_date = datetime.strptime(str(start_date), '%Y%m%d')
        self.tasks = tasks
        if isinstance(self.tasks, list) and self.tasks:
            self._update_dependencies()
        self.overheads = overheads if overheads is not None else 0

        self.planned_start = start_date
        self.actual_start = start_date

    def _update_dependencies(self):
        for task in self.tasks:
            for predecessor, rel_type, lag in task.predecessors:
                predecessor._add_successor(task, rel_type, lag)
            for successor, rel_type, lag in task.successors:
                successor._add_predecessor(task, rel_type, lag)

    def _calculate_cost(self):
        self.direct_cost = sum(task.direct_cost for task in self.tasks)
        self.indirect_cost = sum(
            task.indirect_cost for task in self.tasks) + self.duration * self.overheads
        self.total_cost = self.direct_cost + self.indirect_cost

    def CPM(self):
        for task in self.tasks:
            if not task.predecessors:
                task.es = 0
                task.ef = task.duration
        for _ in self.tasks:
            for task in self.tasks:
                if task.predecessors:
                    max_start = 0
                    for predecessor, rel_type, lag in task.predecessors:
                        if rel_type == 'fs':
                            max_start = max(max_start, predecessor.ef + lag)
                        elif rel_type == 'ss':
                            max_start = max(max_start, predecessor.es + lag)
                        elif rel_type == 'ff':
                            max_start = max(
                                max_start, predecessor.ef - task.duration + lag)
                        elif rel_type == 'sf':
                            max_start = max(
                                max_start, predecessor.es - task.duration + lag)
                    task.es = max(0, max_start)
                    task.ef = task.es + task.duration
        self.duration = max(task.ef for task in self.tasks)
        self.finish_date = self.start_date + timedelta(days=self.duration)
        for task in self.tasks:
            if not task.successors:
                task.lf = self.duration
                task.ls = task.lf - task.duration
        for _ in self.tasks:
            for task in self.tasks:
                if task.successors:
                    min_finish = self.duration
                    for successor, rel_type, lag in task.successors:
                        if rel_type == 'fs':
                            min_finish = min(min_finish, successor.ls + lag)
                        elif rel_type == 'ss':
                            min_finish = min(
                                min_finish, successor.ls + successor.duration - task.duration + lag)
                        elif rel_type == 'ff':
                            min_finish = min(min_finish, successor.lf + lag)
                        elif rel_type == 'sf':
                            min_finish = min(
                                min_finish, successor.lf + successor.duration - task.duration + lag)
                        
                    task.lf = max(task.ef, min_finish)
                    task.ls = task.lf - task.duration
                task.slack = round(task.ls - task.es, 4)
                task.critical = task.slack <= 0
        self._calculate_cost()
    
    def df_CPM(self):
        self.CPM()
        return pd.DataFrame({
            'Name': [task.name for task in self.tasks],
            'Total Cost': [task.total_cost for task in self.tasks],
            'Direct Cost': [task.direct_cost for task in self.tasks],
            'Indirect Cost': [task.indirect_cost for task in self.tasks],
            'Predecessors': [', '.join(f'{p.name}({r})+{l}' for p, r, l in task.predecessors) for task in self.tasks],
            'Successors': [', '.join(f'{s.name}({r})+{l}' for s, r, l in task.successors) for task in self.tasks],
            'Duration': [task.duration for task in self.tasks],
            'ES': [task.es for task in self.tasks],
            'EF': [task.ef for task in self.tasks],
            'LS': [task.ls for task in self.tasks],
            'LF': [task.lf for task in self.tasks],
            'ES(date)': [self.start_date + timedelta(days=task.es) for task in self.tasks],
            'EF(date)': [self.start_date + timedelta(days=task.ef) for task in self.tasks],
            'LS(date)': [self.start_date + timedelta(days=task.ls) for task in self.tasks],
            'LF(date)': [self.start_date + timedelta(days=task.lf) for task in self.tasks],
            'Slack': [task.slack for task in self.tasks],
            'Critical': [task.critical for task in self.tasks],
        })
    
    def df_Project(self):
        self.CPM()
        return pd.DataFrame({
            'Name': [self.name],
            'Start Date': [self.start_date],
            'Finish Date': [self.finish_date],
            'Duration': [self.duration],
            'Total Cost': [self.total_cost],
            'Direct Cost': [self.direct_cost],
            'Indirect Cost': [self.indirect_cost],
        })

    def MC(self, S):
        original_tasks = [task for task in self.tasks]
        for task in self.tasks:
            task.criticality = 0

        simulated_results = []
        for _ in range(S):
            for task in self.tasks:
                task.duration = task._sample_duration()
                task._calculate_cost()
            self.CPM()
            for task, original_task in zip(self.tasks, self.tasks):
                if task.critical:
                    original_task.criticality += 1/S
            simulated_results.append([
                max(task.ef for task in self.tasks),
                self.total_cost,
                self.direct_cost,
                self.indirect_cost,
            ])
        self.tasks = [task for task in original_tasks]
        return simulated_results

    def df_MC(self, S):
        return pd.DataFrame(self.MC(S), columns=['Duration', 'Total Cost', 'Direct Cost', 'Indirect Cost'])

