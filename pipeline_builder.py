from typing import *
import typing
from kedro.pipeline.modular_pipeline import pipeline
from kedro.pipeline import node

class PipelineBuilder(object):
    
    def __init__(self) -> None:
        self.steps = []
        self._data_set_counter = 0
    
    def call(self, 
            func: Callable,
            *args: List[str],
            inputs: Dict[str, str] = None,
            outputs: Union[None, str, List[str]] = None,
            name: str = None,
            tags: Union[str, Iterable[str]] = None,
            confirms: Union[str, List[str]] = None,
            namespace: str = None):
        assert not (args and inputs), "Cannot mix positional and keyword parameters"
        assert not isinstance(outputs, dict), "Dict is not supported for outputs"
        inputs = list(args or inputs)
        if isinstance(outputs, str): outputs = [outputs]
        outputs = outputs or self._infer_outputs(func)
        self.steps.append(dict(func=func, inputs=inputs, outputs=outputs, 
                               name=name, tags=tags, confirms=confirms, namespace=namespace))
        if not outputs: return None
        if len(outputs) == 1: return outputs[0]
        else: return outputs
        
    def build(self, names=None):
        # turn local variable names into dataset names
        if names:
            for key, val in names.items():
                if isinstance(val, _DataSetPlaceholder) and val.name is None:
                    val.name = key
        # generate names for the remaining annonymous datasets
        for step in self.steps:
            for dataset in step['inputs'] + step['outputs']:
                if isinstance(dataset, _DataSetPlaceholder) and dataset.name is None:
                    dataset.name = f'_dataset{self._data_set_counter}'
                    self._data_set_counter += 1
        # replace placeholders with strings
        for step in self.steps:
            step['inputs'] = _replace_placeholder(step['inputs'])
            step['outputs'] = _replace_placeholder(step['outputs'])
        return pipeline([node(**step) for step in self.steps])
    
    def _infer_outputs(self, func):
        return_types = func.__annotations__.get('return')
        if return_types is None: return []
        if return_types._name.startswith('Tuple'):
            return_types = return_types.__args__
        else:
            return_types = [return_types]
        return [_DataSetPlaceholder() for _ in return_types]
        
class _DataSetPlaceholder(object):
    name = None
        
def _replace_placeholder(datasets):
    return [(ds.name if isinstance(ds, _DataSetPlaceholder) else ds) for ds in datasets]
