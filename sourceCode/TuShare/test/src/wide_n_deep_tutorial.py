# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Example code for TensorFlow Wide & Deep Tutorial using TF.Learn API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import tempfile

# import urllib

import pandas as pd
import tensorflow as tf

# 我们训练使用的数据的列的名称  
COLUMNS = ["age", "workclass", "fnlwgt", "education", "education_num",
                     "marital_status", "occupation", "relationship", "race", "gender",
                     "capital_gain", "capital_loss", "hours_per_week", "native_country",
                     "income_bracket"]
LABEL_COLUMN = "label"

# 其实上面的数据的列可以分为两类，即categorical 和 continuous. 
# categorical colum 就是这个列有有限个属性。 
# 例如workclass 有{ Private, Self-emp-not-inc, Self-emp-inc，etc} 
# ccontinuous colum 就是这个列的属性是数字的连续型，如age 
  
CATEGORICAL_COLUMNS = ["workclass", "education", "marital_status", "occupation",
                                             "relationship", "race", "gender", "native_country"]
CONTINUOUS_COLUMNS = ["age", "education_num", "capital_gain", "capital_loss",
                                            "hours_per_week"]

                                        
def maybe_download(train_data, test_data):
    """Maybe downloads training data and returns train and test file names."""
    if train_data:        
        train_file_name = train_data
    else:
#         train_file = tempfile.NamedTemporaryFile(delete=False)
#         urllib.request.urlretrieve("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.data", train_file.name)    # pylint: disable=line-too-long
#         train_file_name = train_file.name
#         train_file.close()
        train_file_name = "d:/adult.txt"
#         train_file_name = "/home/moonlit/studyTensorFlow/wide_n_deep_data/adult.data"

        print("Training data is downloaded to %s" % train_file_name)
        
    if test_data:
        test_file_name = test_data
    else:
#         test_file = tempfile.NamedTemporaryFile(delete=False)
#         urllib.request.urlretrieve("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.test", test_file.name)    # pylint: disable=line-too-long
#         test_file_name = test_file.name
#         test_file.close()
        test_file_name = "d:/adult.txt"
#         test_file_name = "/home/moonlit/studyTensorFlow/wide_n_deep_data/adult.test"
        print("Test data is downloaded to %s" % test_file_name)

    return train_file_name, test_file_name


def build_estimator(model_dir, model_type):
    """ 
            创建预测模型 
    """  
    # 创建稀疏的列. 列表中的每一个键将会获得一个从 0 开始的逐渐递增的id  
    # 例如 下面这句female 为 0，male为1。这种情况是已经事先知道列集合中的元素  
    # 都有那些     
    """Build an estimator."""
    # Sparse base columns.
    gender         = tf.contrib.layers.sparse_column_with_keys(column_name="gender"   , keys=["female", "male"])
    # 对于不知道列集合中元素有那些的情况时，可以用下面这种。  
    # 例如教育列中的每个值将会被散列为一个整数id  
    # 例如  
    # ID  Feature 
    # ...  
    # 9   "Bachelors" 
    # ...  
    # 103 "Doctorate" 
    # ...  
    # 375 "Masters"       
    education      = tf.contrib.layers.sparse_column_with_hash_bucket("education"     , hash_bucket_size=1000)
    relationship   = tf.contrib.layers.sparse_column_with_hash_bucket("relationship"  , hash_bucket_size=100)
    workclass      = tf.contrib.layers.sparse_column_with_hash_bucket("workclass"     , hash_bucket_size=100)
    occupation     = tf.contrib.layers.sparse_column_with_hash_bucket("occupation"    , hash_bucket_size=1000)
    native_country = tf.contrib.layers.sparse_column_with_hash_bucket("native_country", hash_bucket_size=1000)

    # 为连续的列元素设置一个实值列  
    # Continuous base columns.
    age            = tf.contrib.layers.real_valued_column("age"           )
    education_num  = tf.contrib.layers.real_valued_column("education_num" )
    capital_gain   = tf.contrib.layers.real_valued_column("capital_gain"  )
    capital_loss   = tf.contrib.layers.real_valued_column("capital_loss"  )
    hours_per_week = tf.contrib.layers.real_valued_column("hours_per_week")

    # 为了更好的学习规律，收入是与年龄阶段有关的，因此需要把连续的数值划分  
    # 成一段一段的区间来表示收入  
    # Transformations.
    age_buckets = tf.contrib.layers.bucketized_column(age,
                                                      boundaries=[
                                                                  18, 25, 30, 35, 40, 45,
                                                                  50, 55, 60, 65
                                                                  ]
                                                      )
    # 上面所说的模型，  
    # 这个为 wide 模型  
    # Wide columns and deep columns.
    wide_columns = [gender, native_country, education, occupation, workclass,relationship, age_buckets,
                    tf.contrib.layers.crossed_column([education     , occupation           ],hash_bucket_size=int(1e4)),
                    tf.contrib.layers.crossed_column([age_buckets   , education, occupation],hash_bucket_size=int(1e6)),
                    tf.contrib.layers.crossed_column([native_country, occupation           ],hash_bucket_size=int(1e4))
                    ]
    # 这个为 deep 模型 
    deep_columns = [
                    tf.contrib.layers.embedding_column(workclass     , dimension=8),
                    tf.contrib.layers.embedding_column(education     , dimension=8),
                    tf.contrib.layers.embedding_column(gender        , dimension=8),
                    tf.contrib.layers.embedding_column(relationship  , dimension=8),
                    tf.contrib.layers.embedding_column(native_country, dimension=8),
                    tf.contrib.layers.embedding_column(occupation    , dimension=8),
                    age,
                    education_num,
                    capital_gain,
                    capital_loss,
                    hours_per_week,
                    ]

    if model_type == "wide":
        m = tf.contrib.learn.LinearClassifier(model_dir=model_dir,
                                                                                    feature_columns=wide_columns)
    elif model_type == "deep":
        m = tf.contrib.learn.DNNClassifier(model_dir=model_dir,
                                                                             feature_columns=deep_columns,
                                                                             hidden_units=[100, 50])
    else:
        m = tf.contrib.learn.DNNLinearCombinedClassifier(
                model_dir=model_dir,
                linear_feature_columns=wide_columns,
                dnn_feature_columns=deep_columns,
                dnn_hidden_units=[100, 50],
                fix_global_step_increment_bug=True)
    return m


def input_fn(df):
    """这个函数的主要作用就是把输入数据转换成tensor，即向量型"""  

    """Input builder function."""
    # Creates a dictionary mapping from each continuous feature column name (k) to
    # the values of that column stored in a constant Tensor.
    # 为continuous colum列的每一个属性创建一个对于的 dict 形式的 map  
    # 对应列的值存储在一个 constant 向量中      
    continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
    # Creates a dictionary mapping from each categorical feature column name (k)
    # to the values of that column stored in a tf.SparseTensor.
    # 为 categorical colum列的每一个属性创建一个对于的 dict 形式的 map  
    # 对应列的值存储在一个 tf.SparseTensor 中      
    categorical_cols = {
            k: tf.SparseTensor(
                    indices=[[i, 0] for i in range(df[k].size)],
                    values=df[k].values,
                    dense_shape=[df[k].size, 1])
            for k in CATEGORICAL_COLUMNS}
    
    # 合并上面两个dict类型  
    # Merges the two dictionaries into one.
    feature_cols = dict(continuous_cols)
    feature_cols.update(categorical_cols)
    
    # 将 label column 转换成一个 constant 向量 
    # Converts the label column into a constant Tensor.
    label = tf.constant(df[LABEL_COLUMN].values)
    
    # Returns the feature columns and the label.
    # 返回向量形式对应列的数据和label  
    return feature_cols, label


def train_and_eval(model_dir, model_type, train_steps, train_data, test_data):
    # 这个函数是真正的入口函数，用来训练数据，之后才进行 evaluate。 
   
    """Train and evaluate the model."""
    # 首先取得train 和 test 文件的文件名
    train_file_name, test_file_name = maybe_download(train_data, test_data)
    df_train = pd.read_csv(
            tf.gfile.Open(train_file_name),
            names=COLUMNS,
            skipinitialspace=True,
            engine="python")
    print(df_train)
    df_test = pd.read_csv(
            tf.gfile.Open(test_file_name),
            names=COLUMNS,
            skipinitialspace=True,
            skiprows=1,
            engine="python")
    
    # 移除非数字 
    # remove NaN elements
    df_train = df_train.dropna(how='any', axis=0)
    df_test = df_test.dropna(how='any', axis=0)

    # 将 收入一列 即label 转换为 0和1，即大于50K的设置为1  
    # 小于50K的设置为0  
    df_train[LABEL_COLUMN] = (
            df_train["income_bracket"].apply(lambda x: ">50K" in x)).astype(int)
    df_test[LABEL_COLUMN] = (
            df_test["income_bracket"].apply(lambda x: ">50K" in x)).astype(int)

    # 判断输出的目录是否存在，不存在则创建临时的 
    model_dir = tempfile.mkdtemp() if not model_dir else model_dir
    print("model directory = %s" % model_dir)

    # 创建预测模型，返回的是 wide 或者 deep 或者 wide&deep 模型中的一个 
    m = build_estimator(model_dir, model_type)
    
    # 进行训练  
    m.fit(input_fn=lambda: input_fn(df_train), steps=train_steps)
    
    # 使用test 数据进行评价  
    results = m.evaluate(input_fn=lambda: input_fn(df_test), steps=1)
    for key in sorted(results):
        print("%s: %s" % (key, results[key]))


FLAGS = None


def main(_):
    train_and_eval(FLAGS.model_dir, FLAGS.model_type, FLAGS.train_steps,
                                 FLAGS.train_data, FLAGS.test_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument(
            "--model_dir",
            type=str,
            default="",
            help="Base directory for output models."
    )
    parser.add_argument(
            "--model_type",
            type=str,
            default="wide_n_deep",
            help="Valid model types: {'wide', 'deep', 'wide_n_deep'}."
    )
    parser.add_argument(
            "--train_steps",
            type=int,
            default=200,
            help="Number of training steps."
    )
    parser.add_argument(
            "--train_data",
            type=str,
            default="",
            help="Path to the training data."
    )
    parser.add_argument(
            "--test_data",
            type=str,
            default="",
            help="Path to the test data."
    )
    FLAGS, unparsed = parser.parse_known_args()
tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)