from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

class Schema(Dict[str, type]):
    """Base class for input and output schemas."""
    def __init__(self, schema: Dict[str, type]):
        self._validate_schema(schema)
        super().__init__(schema)

    @staticmethod
    def _validate_schema(schema: Dict[str, type]) -> None:
        if not isinstance(schema, dict):
            raise TypeError("Schema must be a dictionary")
            
        for key, value in schema.items():
            if not isinstance(key, str):
                raise TypeError("Schema keys must be strings")
            if not isinstance(value, type):
                raise TypeError("Schema values must be types")

class Mappings(Dict[str, str]):
    """"""
    def __init__(self, mappings: Dict[str, str]):
        self._validate_mappings(mappings)
        super().__init__(mappings)

    @staticmethod
    def _validate_mappings(mappings: Dict[str, str]) -> None:
        if not isinstance(mappings, dict):
            raise TypeError("Mappings must be a dictionary")
        
        for key, value in mappings.items():
            if not isinstance(key, str):
                raise TypeError("Mapping keys must be strings")
            if not isinstance(value, str):
                raise TypeError("Mapping values must be strings")

class Arguments(Dict[str, Any]):
    """Dictionary class for storing argument values.
    
    This class extends Dict to store parameter key-value pairs while ensuring
    the parameters are valid (not None unless explicitly allowed).
    """
    def __init__(self, args: Dict[str, Any]):
        self._validate_arguments(args)
        super().__init__(args)
    
    @staticmethod
    def _validate_arguments(args: Dict[str, Any]) -> None:
        if not isinstance(args, dict):
            raise TypeError("Args must be a dictionary")
        
        for key, value in args.items():
            if not isinstance(key, str):
                raise TypeError("Args keys must be strings")
            if value is None:
                raise TypeError("Args values cannot be None")

@dataclass
class TaskExecutionInfo:
    """Contains execution information for a task."""
    status: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[Exception] = None
    dependencies_met: bool = False

@dataclass
class MetaFunc:
    """Metadata container for function information."""
    module: str
    name: str

@dataclass
class MetaTask:
    """Metadata container for task information.
    
    Attributes:
        name: Unique identifier for the task
        description: Human-readable description of what the task does
        func: Reference to the function this task wraps
        args: Arguments for the task
        requires: Schema defining required input types
        provides: Schema defining output types
        input_mappings: Mappings between task inputs and function arguments
        output_mappings: Mappings between function returns and task outputs
    """
    name: str
    description: str
    func: MetaFunc
    args: Arguments = field(default_factory=lambda: Arguments({}))
    requires: Schema = field(default_factory=lambda: Schema({}))
    provides: Schema = field(default_factory=lambda: Schema({}))
    input_mappings: Mappings = field(default_factory=lambda: Mappings({}))
    output_mappings: Mappings = field(default_factory=lambda: Mappings({}))
    
@dataclass
class MetaWorkflow:
    """Metadata container for workflow information.

    Attributes:
        name: Unique identifier for the workflow
        description: Human-readable description of what the workflow does
        tasks: List of MetaTask objects that comprise the workflow
        inputs: Schema defining the required input types for the entire workflow
        outputs: Schema defining the output types produced by the workflow
    """
    name: str
    description: str
    tasks: List[MetaTask]
    inputs: Schema = field(default=lambda: Schema({}))
    outputs: Schema = field(default=lambda: Schema({}))