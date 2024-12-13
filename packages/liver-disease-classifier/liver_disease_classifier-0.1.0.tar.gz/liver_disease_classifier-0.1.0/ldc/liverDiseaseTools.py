from .data_preprocessing import load_and_clean_data, split_and_scale_data

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.preprocessing import StandardScaler

from .model_training import (
    train_logistic_regression,
    train_knn,
    train_svc,
    train_decision_tree,
    train_random_forest,
    train_gradient_boosting,
    )

import os

import pandas as pd


class PreProcessingChecks:
    # extensions for files allowed
    allowed_extensions = ['.csv']

    # fields expected in the dataset
    allowed_fields = sorted(["CATEGORY", "AGE", "SEX", "ALB", "ALP", "ALT", "AST", "BIL", "CHE", "CHOL","CREA","GGT","PROT"])

    def validateTypes(self, file_path, target_column, columns_to_drop, desired_test_size):
        assert isinstance(file_path, str), "File path should be a string.."

        assert isinstance(target_column, str), "Target label should be a string.."

        assert isinstance(columns_to_drop, list) or columns_to_drop is None, "It should be a list of labels of type string.."

        assert isinstance(desired_test_size, float) or isinstance(desired_test_size, int), "Test size percentage should be a float or integer..."

        # test size
        raw_test_size = float(desired_test_size)

        assert 1 <= raw_test_size <= 100, "Test size should be a valid percentage of the range 1-100"

        return raw_test_size / 100

    def validateFilePath(self, path_to_dataset_file:str):
        # initial
        assert len(path_to_dataset_file.strip()) > 0, "Please provide a valid path"

        # existence
        assert os.path.exists(path_to_dataset_file), f"Dataset path `{path_to_dataset_file}` appears not to exist.."

        # check if its a csv file
        _, file_extension = os.path.splitext(path_to_dataset_file)

        assert file_extension.lower() in self.allowed_extensions, f"Invalid dataset file only, datasets with extensions {self.allowed_extensions} are allowed"


    def validateDatasetFields(self, filePath:str):
        # read file
        df = pd.read_csv(filePath, index_col=0)

        original_fields = df.columns.to_list()

        loaded_fields = sorted([eachField.upper() for eachField in original_fields])

        are_the_same = loaded_fields == self.allowed_fields

        return are_the_same, original_fields, self.allowed_fields
    
    
    def validateDropColumns(self, present_fields:list, drop_columns:list):
        """_summary_

        Args:
            present_fields (list): A list of presently found fields
            drop_columns (list): A list of fields to drop
        """

        presence_count = [True for eachField in drop_columns if eachField in present_fields]

        drop_columns_present = len(drop_columns) == presence_count.count(True)

        assert drop_columns_present is True, f"Some labels provided cant be found... expected include:{present_fields}"

        return 
    
    def extractGenderAndCrea(self, fields_list:list):
        """_summary_

        Args:
            fields_list (list): List of the original fields in the dataset

        Returns:
            _type_: Its a list of labels as strings
        """
        original_gender = [eachField for eachField in fields_list if eachField.lower() == 'sex']

        original_crea = [eachField for eachField in fields_list if eachField.lower() == 'crea']

        return [original_gender[0], original_crea[0]] 

class Model:
    """Represents a trained model that can be used to make predictions
    """
    def __init__(self, model_object, model_name, model_details, fields_size, data_sets):
        self.__model_item = model_object

        self.__model_name = model_name

        self.details = model_details

        self.__fields_size = fields_size - 1 

        self.__data_sets = data_sets

    def __not2D(self, feedList):
        # Check that no elements in the list are themselves lists
        return all(not isinstance(sublist, list) for sublist in feedList)
    
    def __scale_data(self, input_data:list):
        scaler_instance = StandardScaler()

        # scale
        _ = scaler_instance.fit_transform(self.__data_sets[-1])
        
        scaled_data = scaler_instance.transform(input_data)

        return scaled_data
    

    def metrics(self):
        """Returns the performance of the model on the testing sets

        Returns:
            - `model_accuracy` : Accuracy of the model
            - `confusion_matrix`: Details about results
            - `classification_report`: Report on performance
            
        """
        # make prediction using testing set
        predicted_value = self.__model_item.predict(self.__data_sets[0])

        # format: X_train, X_test, y_train, y_test

        # metrics
        _model_accuracy = accuracy_score(self.__data_sets[1], predicted_value)

        _confusion_matrix = confusion_matrix(self.__data_sets[1], predicted_value)

        _classification_report = classification_report(self.__data_sets[1], predicted_value)

        return _model_accuracy, _confusion_matrix, _classification_report


    def predict(self, input_list:list):
        # ensure there is data
        assert len(input_list) > 0, f"Ensure that there is data about `{self.__fields_size}` fields not including the `target`"

        assert len(input_list) == self.__fields_size, f"{self.__fields_size} fields are expected, Note: provided fields shouldn`t include `target`"

        assert self.__not2D(feedList=input_list), "Feed values should be a plain list and not an n-dimension array"

        # structure
        assert isinstance(input_list[1], str) and input_list[1] in ['m', 'f'], "Expected values are `m` and `f`"

        numeric_fields_indices = [0] + [i for i in range(2, len(input_list))]

        numeric_fields = [input_list[each_index] for each_index in numeric_fields_indices]

        all_numeric = all([isinstance(each_value, float) or isinstance(each_value, int) for each_value in numeric_fields])

        assert all_numeric is True, "Ensure that all other fields apart from the `gender` are numeric (float or int)"

        # format
        # 32,"m",38.5,52.5,7.7,22.1,7.5,6.93,3.23,106,12.1,69
        copy_of_input = input_list.copy()

        copy_of_input[1] = 0 if copy_of_input[1].lower() == "m" else 1

        # remove sex and crea
        copy_of_input.pop(1)

        copy_of_input.pop(-2)

        # prepare
        input_data = [copy_of_input]

        prepared_data = self.__scale_data(input_data)

        # print(input_data)

        # print(prepared_data)

        try:
            # make prediction
            predicted_value = self.__model_item.predict(prepared_data)

        except:
            predicted_value = None

        return predicted_value



class Dataset:
    model_tags = {
        1: 'Logistic Regression',
        2: 'Decision Tree',
        3: 'K-Means',
        4: 'Random Forest',
        5: 'Gradient Boost',
        6: 'Support Vector Machine'
    }


    def __init__(self, data_portions, present_fields, target_field):
        # allowed gamma values
        self.__gamma_values = ['auto', 'scale']

        # data
        self.__x_train = data_portions[0]

        self.__x_test = data_portions[1]

        self.__y_train = data_portions[2]

        self.__y_test = data_portions[3]

        # fields
        self.__fields = present_fields

        # target
        self.__target_field = target_field

    def train_sets(self):
        """Returns the present train sets as a tuple

        Returns:
            _type_: (X training set, Y training set)
        """
        return self.__x_train, self.__y_train
    
    def test_sets(self):
        """Returns the present test sets as a tuple

        Returns:
            _type_: (X testing set, Y testing set)
        """
        return self.__x_test, self.__y_test
    

    def target(self):
        """Returns the label of the target field

        Returns:
            _type_: As a string 
        """
        return self.__target_field
    

    def train_model(self, tag_of_model:int, **kwargs):
        """Trains the selected model on the dataset based on the model tag
            - For Support Vector Machines, the `gamma` and `C` values should be provided

        Args:
            tag_of_model (int): takes on values in `1` through `6`

        Returns:
            _type_: A trained model on the data
        """
        # check
        assert tag_of_model in self.model_tags, f"Tag should be in {self.model_tags}"

        # get the name of the model
        model_name = self.model_tags[tag_of_model]

        model_details = model_name

        if tag_of_model in [1, 2, 3, 4, 5]:
            if tag_of_model == 1:
                trained_model = train_logistic_regression(
                    X_train=self.__x_train,
                    y_train=self.__y_train
                )
            
            elif tag_of_model == 2:
                trained_model = train_decision_tree(
                    X_train=self.__x_train,
                    y_train=self.__y_train
                )

            elif tag_of_model == 3:
                trained_model = train_knn(
                    X_train=self.__x_train,
                    y_train=self.__y_train
                )

            elif tag_of_model == 4:
                trained_model = train_random_forest(
                    X_train=self.__x_train,
                    y_train=self.__y_train
                )

            else:
                trained_model = train_gradient_boosting(
                    X_train=self.__x_train,
                    y_train=self.__y_train
                )

        else:
            # get the gamma and C data
            gammaValue = kwargs.get('gamma', 'scale')

            regularizationValue = kwargs.get('C', 1)

            assert not gammaValue is None and not regularizationValue is None, "`gamma` : str  and `C` : float | int values should be provided"

            # validate
            assert isinstance(gammaValue, str) and gammaValue in self.__gamma_values, f"Gamma value should be in : {self.__gamma_values}"

            assert isinstance(regularizationValue, float) or isinstance(regularizationValue, int), "The expected type of C (regularization parameter) should be a float or int"

            # cast to float
            regularizationValue = float(regularizationValue)

            # details
            model_details = f"C: {regularizationValue}, gamma: {gammaValue}"

            # train
            trained_model = train_svc(
                    X_train=self.__x_train,
                    y_train=self.__y_train,
                    gamma=gammaValue,
                    C=regularizationValue
                )
        
        # prepare
        model_item = Model(
            model_object=trained_model,
            model_name=model_name,
            model_details=model_details,
            fields_size=len(self.__fields),
            data_sets=[
                self.__x_test,
                self.__y_test,
                self.__x_train
            ]
        )

        return model_item

            

            
        

        




class LiverDiseaseTools:
    @staticmethod
    def load(data_set_path:str, target_column:str, columns_to_drop:list=None, desired_test_size:int=20):
        """Takes in the file location of the dataset file (should be .csv) and the column of interest `target`

        Args:
            data_set_path (str): Where the dataset file is located
            target_column (str): What column is of interest
            desired_test_size (int): What percentage of the dataset will be used as the test size
        """

        # make checks
        test_size_value = PreProcessingChecks().validateTypes(
            file_path=data_set_path,
            target_column=target_column,
            columns_to_drop=columns_to_drop,
            desired_test_size=desired_test_size
        )

        # validate the file path
        PreProcessingChecks().validateFilePath(path_to_dataset_file=data_set_path)

        validity_, fields_, allowed_ = PreProcessingChecks().validateDatasetFields(filePath=data_set_path)

        assert validity_ is True, f"Dataset contains unexpected fields, expected fields include: {allowed_}"

        if columns_to_drop is None:
            # extract the sex and crea related labels
            columns_to_drop = PreProcessingChecks().extractGenderAndCrea(fields_list=fields_)

        else:
            # check if those fields exist
            PreProcessingChecks().validateDropColumns(fields_, columns_to_drop)

        # target
        assert target_column in fields_, f"Target label `{target_column}` cant be found in {fields_}"
        
        # get dataset data
        loaded_data = load_and_clean_data(file_path=data_set_path)

        # split and scale data
        data_portions = split_and_scale_data(
            data=loaded_data,
            target_column=target_column,
            drop_columns=columns_to_drop,
            test_size=test_size_value
        )

        # create a dataset object
        data_set_object = Dataset(
            data_portions=data_portions,
            present_fields=fields_,
            target_field=target_column
        )

        return data_set_object




        
        


