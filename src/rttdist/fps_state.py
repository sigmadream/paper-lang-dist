"""Pure state counting and termination rules, independent of model and tools."""
from dataclasses import dataclass, field
import hashlib

def source_hash(source):
    return hashlib.sha256(source.replace('\r\n','\n').replace('\r','\n').encode('utf-8')).hexdigest()

@dataclass
class FPSState:
    seed_language: str
    source: str
    threshold: float = .85
    max_fps_size: int = 10
    max_translation_steps: int = 20
    states: dict = field(default_factory=dict)
    history: list = field(default_factory=list)
    completed_roundtrips: int = 0
    all_functional: bool = True

    def __post_init__(self):
        self.states[(self.seed_language,source_hash(self.source))]=0

    def add(self, language, source):
        step=len(self.history)+1
        key=(language,source_hash(source))
        first=self.states.setdefault(key,step)
        item={'step':step,'language':language,'source_sha256':key[1],
              'first_seen_step':first,'duplicate':first!=step,'fps_size':len(self.states)}
        self.history.append(item)
        return item

    def decide(self, functional_status, restored, adjacent=None, similarity_available=True):
        if functional_status!='success':
            self.all_functional=False
            return functional_status
        if restored: self.completed_roundtrips+=1
        if len(self.states)>self.max_fps_size: return 'max_distance_reached'
        if restored:
            if not similarity_available or adjacent is None: return 'similarity_unavailable'
            if adjacent>=self.threshold: return 'success'
        if len(self.history)>=self.max_translation_steps: return 'translation_budget_reached'
        return None
