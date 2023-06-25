from typing import Any, Tuple
from pipeline_builder import PipelineBuilder

def split_datasets(df) -> Tuple[Any, Any, Any]:
    return (object(), object(), object())

def train_classifier(train, valid) -> Any:
    return object()

def evaluate_classifer(classifier, test) -> Any:
    return object()

pb = PipelineBuilder()
train, valid, test = pb.call(split_datasets, 'raw_data', name='split')
classifier = pb.call(train_classifier, train, valid, name='train')
results = pb.call(evaluate_classifer, classifier, test, name='eval')
pip = pb.build(names=locals())
print(pip)

# # Compare to the equivalent code using regular Kedro API:

# from kedro.pipeline import pipeline, node
# pip = pipeline([
#     node(
#         func=split_datasets,
#         inputs=['raw_data'], outputs=['train', 'valid', 'test'],
#         name='split'
#     ),
#     node(
#         func=train_classifier,
#         inputs=['train', 'valid'], outputs=['classifier'],
#         name='train'
#     ),
#     node(
#         func=evaluate_classifer,
#         inputs=['classifier', 'test'], outputs=['results'],
#         name='eval'
#     ),
# ])
# print(pip)
