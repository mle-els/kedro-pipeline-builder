from typing import Any, Tuple
from pipeline_builder import PipelineBuilder

def preprocess_companies(companies) -> Any:
    return object()

def preprocess_shuttles(shuttles) -> Any:
    return object()

def create_model_input_table(preprocessed_shuttles, preprocessed_companies, reviews) -> Any:
    return object()

def split_data(model_input_table, params) -> Tuple[Any, Any, Any, Any]:
    return (object(), object(), object(), object())

def train_model(X_train, X_test) -> Any:
    return object()

def evaluate_model(regressor, X_test, y_test) -> None:
    return object()

pb = PipelineBuilder()
preprocessed_companies = pb.call(preprocess_companies, 'companies', name='preprocess_companies_node')
preprocessed_shuttles = pb.call(preprocess_shuttles, 'shuttles', name='preprocess_shuttles_node')
model_input_table = pb.call(create_model_input_table, preprocessed_shuttles, 
                            preprocessed_companies, "reviews", name='create_model_input_table_node')
X_train, X_test, y_train, y_test = pb.call(split_data, model_input_table, "params:model_options", 
                                           name="split_data_node")
regressor = pb.call(train_model, X_train, y_train, name="train_model_node")
pb.call(evaluate_model, regressor, X_test, y_test, name="evaluate_model_node")
pip = pb.build(names=locals())
print(pip)

# # Compare to the equivalent code using regular Kedro API:

# from kedro.pipeline import pipeline, node
# pip = pipeline([
#     node(
#         func=preprocess_companies,
#         inputs="companies",
#         outputs="preprocessed_companies",
#         name="preprocess_companies_node",
#     ),
#     node(
#         func=preprocess_shuttles,
#         inputs="shuttles",
#         outputs="preprocessed_shuttles",
#         name="preprocess_shuttles_node",
#     ),
#     node(
#         func=create_model_input_table,
#         inputs=["preprocessed_shuttles", "preprocessed_companies", "reviews"],
#         outputs="model_input_table",
#         name="create_model_input_table_node",
#     ),
#     node(
#         func=split_data,
#         inputs=["model_input_table", "params:model_options"],
#         outputs=["X_train", "X_test", "y_train", "y_test"],
#         name="split_data_node",
#     ),
#     node(
#         func=train_model,
#         inputs=["X_train", "y_train"],
#         outputs="regressor",
#         name="train_model_node",
#     ),
#     node(
#         func=evaluate_model,
#         inputs=["regressor", "X_test", "y_test"],
#         outputs=None,
#         name="evaluate_model_node",
#     ),
# ])
# print(pip)
