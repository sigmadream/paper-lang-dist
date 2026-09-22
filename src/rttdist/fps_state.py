"""Pure state counting and termination rules, independent of model and tools.

Protocol v2 (v1/abs_PLAN.md 2.4): every threshold in `thresholds` records its
first reach step; the attempt keeps translating until the largest threshold is
reached or a failure/limit/budget rule fires. The primary result is read from
the primary `threshold` reach record, so later steps never change it.
"""
from dataclasses import dataclass, field
import hashlib

FUNCTIONAL_FAILURES = ('format_error', 'compile_error', 'compile_timeout', 'runtime_error',
                       'wrong_answer', 'timeout')
CATEGORY = {'max_distance_reached': 'fps_limit', 'translation_budget_reached': 'budget',
            'collection_complete': 'collection_complete', 'infrastructure_error': 'invalid', None: 'invalid'}

def source_hash(source):
    return hashlib.sha256(source.replace('\r\n','\n').replace('\r','\n').encode('utf-8')).hexdigest()

def threshold_key(value):
    return f'{float(value):.2f}'

def category(status):
    """Map a terminal step status to the five plan outcome types (success is per threshold)."""
    if status in FUNCTIONAL_FAILURES: return 'functional_failure'
    return CATEGORY.get(status, 'invalid')

@dataclass
class FPSState:
    seed_language: str
    source: str
    threshold: float = .85
    max_fps_size: int = 10
    max_translation_steps: int = 20
    thresholds: list = None
    states: dict = field(default_factory=dict)
    history: list = field(default_factory=list)
    reached: dict = field(default_factory=dict)
    completed_roundtrips: int = 0
    all_functional: bool = True
    similarity_unavailable_steps: int = 0

    def __post_init__(self):
        self.states[(self.seed_language,source_hash(self.source))]=0
        values=sorted({float(v) for v in (self.thresholds or [])}|{float(self.threshold)})
        self.thresholds=values

    def add(self, language, source):
        step=len(self.history)+1
        key=(language,source_hash(source))
        first=self.states.setdefault(key,step)
        item={'step':step,'language':language,'source_sha256':key[1],
              'first_seen_step':first,'duplicate':first!=step,'fps_size':len(self.states)}
        self.history.append(item)
        return item

    def decide(self, functional_status, restored, adjacent=None, similarity_available=True):
        """Return the terminal status after the latest step, or None to continue."""
        if functional_status!='success':
            self.all_functional=False
            return functional_status
        if restored: self.completed_roundtrips+=1
        if len(self.states)>self.max_fps_size: return 'max_distance_reached'
        if restored:
            if not similarity_available or adjacent is None:
                self.similarity_unavailable_steps+=1
            else:
                step=len(self.history)
                for value in self.thresholds:
                    key=threshold_key(value)
                    if key not in self.reached and adjacent>=value:
                        self.reached[key]={'step':step,'fps_size':len(self.states),
                                           'roundtrip':self.completed_roundtrips,'sym_adj':adjacent}
                if threshold_key(self.thresholds[-1]) in self.reached: return 'collection_complete'
        if len(self.history)>=self.max_translation_steps: return 'translation_budget_reached'
        return None

    def outcome(self, terminal_status, value=None):
        """Per-threshold outcome: success with d_n when reached before the attempt ended."""
        key=threshold_key(self.threshold if value is None else value)
        hit=self.reached.get(key)
        if hit: return {'threshold':key,'category':'success','success':True,'d_n':hit['fps_size'],
                        'reached_step':hit['step'],'reached_roundtrip':hit['roundtrip'],'sym_adj':hit['sym_adj']}
        cat=category(terminal_status)
        if cat=='collection_complete': cat='invalid'  # unreachable: the largest threshold implies all lower ones
        return {'threshold':key,'category':cat,'success':False,'d_n':None,
                'reached_step':None,'reached_roundtrip':None,'sym_adj':None}

    def outcomes(self, terminal_status):
        return {threshold_key(v):self.outcome(terminal_status,v) for v in self.thresholds}
