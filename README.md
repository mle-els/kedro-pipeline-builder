# kedro-pipeline-builder
Sketching a readable and functional way to build Kedro pipelines

With the class `PipelineBuilder`, we can build a pipeline just by calling functions in a concise
and readable manner. Because datasets are now variables that are returned and passed to another
function, typos can be easily detected.

As an example, the `spaceflights` pipeline (Kedro starter) can be written as follows:

```python
pb = PipelineBuilder()
preprocessed_companies = pb.call(preprocess_companies, 'companies', name='preprocess_companies_node')
preprocessed_shuttles = pb.call(preprocess_shuttles, 'shuttles', name='preprocess_shuttles_node')
model_input_table = pb.call(create_model_input_table, "preprocessed_shuttles", 
                            "preprocessed_companies", "reviews", name='create_model_input_table_node')
X_train, X_test, y_train, y_test = pb.call(split_data, "model_input_table", "params:model_options", 
                                           name="split_data_node")
regressor = pb.call(train_model, X_train, y_train, name="train_model_node")
pb.call(evaluate_model, regressor, X_test, y_test, name="evaluate_model_node")
pip = pb.build(names=locals())
```

Please see `example1.py` and `example2.py` for more details.