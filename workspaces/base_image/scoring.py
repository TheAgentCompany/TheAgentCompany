from dataclasses import dataclass
from typing import List, Callable, Optional

@dataclass
class Checkpoint:
    total: int
    result: int
    
    def __post_init__(self):
        if not isinstance(self.total, int):
            raise TypeError(f"total must be an integer, got {type(self.total)}")
        if not isinstance(self.result, int):
            raise TypeError(f"result must be an integer, got {type(self.result)}")
        if self.total < 0:
            raise ValueError(f"total cannot be negative, got {self.total}")
        if self.result < 0:
            raise ValueError(f"result cannot be negative, got {self.result}")
        if self.result > self.total:
            raise ValueError(f"result ({self.result}) cannot be greater than total ({self.total})")

@dataclass
class Result:
    checkpoints: List[Checkpoint]
    scoring_strategy: Optional[Callable[[List[Checkpoint]], dict]] = None
    
    def __post_init__(self):
        if self.scoring_strategy is None:
            # Default scoring strategy: simple sum
            self.scoring_strategy = lambda checkpoints: {
                "total": sum(cp.total for cp in checkpoints),
                "result": sum(cp.result for cp in checkpoints)
            }
    
    @property
    def final_score(self) -> dict:
        return self.scoring_strategy(self.checkpoints)
    
    @classmethod
    def from_dict(cls, data: dict, scoring_strategy: Optional[Callable] = None) -> 'Result':
        """Create a Result instance from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError(f"Input must be a dict, got {type(data)}")
        
        if "checkpoints" not in data:
            raise KeyError("Input must contain 'checkpoints' field")
        
        checkpoints = [
            Checkpoint(**checkpoint_data)
            for checkpoint_data in data["checkpoints"]
        ]
        
        return cls(checkpoints=checkpoints, scoring_strategy=scoring_strategy)
    
    def to_dict(self) -> dict:
        """Convert the Result instance to a dictionary."""
        return {
            "checkpoints": [
                {"total": cp.total, "result": cp.result}
                for cp in self.checkpoints
            ],
            "final_score": self.final_score
        }


# Strategy: get full score if final checkpoint completes
def bonus_for_completing_final(checkpoints: List[Checkpoint]) -> dict:
    """
    If the final checkpoint is completed successfully (full score),
    award full points for all previous checkpoints.
    """
    if not checkpoints:
        return {"total": 0, "result": 0}
    
    total = sum(cp.total for cp in checkpoints)
    
    # Check if final checkpoint got full score
    final_checkpoint = checkpoints[-1]
    if final_checkpoint.result == final_checkpoint.total:
        # Award full points for all checkpoints
        result = sum(cp.total for cp in checkpoints)
    else:
        # Normal scoring
        result = sum(cp.result for cp in checkpoints)
    
    return {"total": total, "result": result}


# Strategy: get credit for 1st checkpoint as long as any checkpoint passes
def bonus_for_completing_any(checkpoints: List[Checkpoint]) -> dict:
    """
    If any checkpoint is completed successfully (full score),
    award full points for the 1st checkpoint, regardless of its completion.

    The rationale is many tasks check trajectory as part of their 1st checkpoint,
    and the information to look up in the trajectory is necessary for any follow-up
    checkpoint to complete. Thus, as long as any follow-up task completes, the 1st
    checkpoint should be considered as complete, even if the trajectory is missing,
    or doesn't contain the keyword that the evaluator is looking for.
    """
    if not checkpoints:
        return {"total": 0, "result": 0}
    
    total = sum(cp.total for cp in checkpoints)
    
    # Check if any checkpoint got full score
    any_checkpoint_complete = any(
        cp.result == cp.total for cp in checkpoints
    )
    
    if any_checkpoint_complete:
        # Award full points for the first checkpoint
        first_checkpoint = checkpoints[0]
        result = first_checkpoint.total + sum(
            cp.result for cp in checkpoints[1:]
        )
    else:
        # Normal scoring
        result = sum(cp.result for cp in checkpoints)
    
    return {"total": total, "result": result}

def bonus_for_completing_any_of_given_checkpoints(given_checkpoints):
    """
    If the given checkpoints are completed successfully (full score),
    award full points for the 1st checkpoint, regardless of its completion.

    The rationale is many tasks check trajectory as part of their 1st checkpoint,
    and the information to look up in the trajectory is necessary for some of the follow-up
    checkpoints to complete. Thus, as long as any of these follow-up tasks completes, the 1st
    checkpoint should be considered as complete, even if the trajectory is missing,
    or doesn't contain the keyword that the evaluator is looking for.
    """
    def scoring_strategy(checkpoints: List[Checkpoint]) -> dict:
        if not checkpoints:
            return {"total": 0, "result": 0}
        
        total = sum(cp.total for cp in checkpoints)
        
        # Check if any of the given checkpoints got full score
        any_checkpoint_complete = any(
            cp.result == cp.total for cp in [checkpoints[i - 1] for i in given_checkpoints]
        )
    
        if any_checkpoint_complete:
            # Award full points for the first checkpoint
            first_checkpoint = checkpoints[0]
            result = first_checkpoint.total + sum(
                cp.result for cp in checkpoints[1:]
            )
        else:
            # Normal scoring
            result = sum(cp.result for cp in checkpoints)
        
        return {"total": total, "result": result}
    
    return scoring_strategy
