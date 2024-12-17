import numpy as np
import copy
import sklearn.base
import sklearn.utils.validation
import sklearn.utils.multiclass



class BaseOrdinalClassifier(sklearn.base.BaseEstimator, sklearn.base.ClassifierMixin):
    # BaseEstimator provides get and set_params() functions and ClassifierMixin provides weighted accuracy function
    def __init__(self, classifier):
        # receive a classifier instance (with preset parameters); we will make copies of it
        # classifier could also be: an sklearn randomSearchCV or gridSearchCV object
        # future potential support for: classifier being an array of classifiers
        self.original_classifier = classifier

    def check_classes(self, classes, y):
        # for each class, check 1) it is numeric and 2) there exist y in those classes
        for class_i in classes:
            if type(class_i) != int and type(class_i) != float:
                raise ValueError("Classes must be numeric (type int or float).")
            if np.sum(np.isclose(y, np.ones(len(y))*class_i)) == 0:
                raise ValueError(f"No training samples were given of class {class_i}")

    def fit(self, X, y, classes=None, sample_weight=None, classifier_fit_kwargs={},
            best_split_threshold='best_clf'):
        """ # copied in part from sklearn, enabling interoperability
        Fit original_classifier according to X, y in a thresholded ordinal
        regression paradigm.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training vectors, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        y : array-like of shape (n_samples,)
            Target values that are ordinal classes. If some of these classes
            are floats, then parameter `classes` must be given.

        classes : array-like of shape (num_classes), default=None
            Array of discrete ordinal classes present in the training data.
            Default is None, where classes are the unique values given in y.
            User is required to provide the array if some classes are floats.
            All inputs must be numeric or None.

        sample_weight : array-like of shape (n_samples,), default=None
            Weights applied to individual samples, inputted into the classifier.

        classifier_fit_kwargs : dictionary, default={}
            A dictionary of hyperparameters to dumped to the classifier's .fit() function.

        best_split_threshold : str, int default="best_clf"
            The threshold that is considered most reliable.
            String options are methods:
                best_clf : the threshold corresponding to the classifier that performs
                    the best (in terms of F1 score) in a 4-fold validation scheme on
                    the training set; note, this method often performs best but is
                    more computationally expensive than the other options
                even_split : threshold that would split the data most evenly in half
                first_split : threshold between the 2 smallest classes
                last_split : threshold between the 2 greatest classes


        Returns
        -------
        self : object
            Returns the instance itself.
        """

        # Check that X and y have correct shape
        X, y = sklearn.utils.validation.check_X_y(X, y)

        # Store the classes seen during fit
        if classes is None:
            self.classes_ = sklearn.utils.multiclass.unique_labels(y)
        else:
            self.check_classes(classes, y)
            self.classes_ = classes

        self.classes_ = np.sort(np.array(self.classes_))

        # thresholds are just above the class labels
        self.thresholds = self.classes_[:-1] + (1e-6 * np.abs(self.classes_[:-1])) + 1e-9 # provide relative and absolute tolerance

        self.X_ = X
        self.y_ = y
        self.sample_weight_ = sample_weight

        self.classifier_objs = np.empty(len(self.thresholds), dtype=object)
        self.classifier_fit_kwargs_ = classifier_fit_kwargs

        for i, threshold_i in enumerate(self.thresholds):
            self.classifier_objs[i] = copy.deepcopy(self.original_classifier).fit(X, y > threshold_i, sample_weight=sample_weight, **classifier_fit_kwargs)

        if best_split_threshold == 'even_split':
            self.best_split_ind = np.argmin([np.sum(y <= threshold)**2 + np.sum(y > threshold)**2 for threshold in self.thresholds])
        elif best_split_threshold == 'best_clf':
            self.best_split_ind = self.calculate_best_threshold_by_clf_performance()
            print("best_clf ind:", self.best_split_ind)
        elif best_split_threshold == 'first_split':
            self.best_split_ind = 0
        elif best_split_threshold == 'last_split':
            self.best_split_ind = len(self.thresholds) - 1
        elif best_split_threshold == 'middle':
            self.best_split_ind = (len(self.thresholds) - 1) // 2 # rounded down
        else: # assume best_split_threshold is an int or float
            if (best_split_threshold < self.classes_[0]) or (best_split_threshold > self.classes_[-1]):
                raise ValueError("best_split_threshold must be between the smallest and largest classes.")
            self.best_split_ind = np.argmin( np.abs(self.thresholds - best_split_threshold) )
        print("Chosen best_split_ind:", self.best_split_ind)
        # Return the classifier
        return self


    def calculate_best_threshold_by_clf_performance(self):
        # should there be functionality for providing a different validation set, without k-fold?
        val_classifier_performances = np.zeros(len(self.thresholds))

        kf = sklearn.model_selection.StratifiedKFold(n_splits=4, random_state=0, shuffle=True)
        for i, (train_indices, val_indices) in enumerate(kf.split(self.X_, self.y_)):
            X_train, X_val = self.X_[train_indices], self.X_[val_indices]
            y_train, y_val = self.y_[train_indices], self.y_[val_indices]

            for j, threshold_j in enumerate(self.thresholds):
                clf_j = copy.deepcopy(self.original_classifier).fit(X_train, y_train > threshold_j, sample_weight=self.sample_weight_, **self.classifier_fit_kwargs_)
                val_classifier_performances[j] += sklearn.metrics.f1_score(y_val > threshold_j, clf_j.predict(X_val), sample_weight=self.sample_weight_)
            print(f"updated val_classifier_performances (fold {i}):", val_classifier_performances)
        return np.argmax(val_classifier_performances) # equivalent to argmax of average

    def predict(self, X, use_predict_proba):
        if use_predict_proba:
            return self.classes_[np.argmax(self.predict_proba(X), axis=1)]
        else:
            scores = np.zeros(X.shape[0], dtype=int)
            for classifier in self.classifier_objs:
                scores += classifier.predict(X)
            return self.classes_[scores]

    def predict_proba(self, X):
        # abstract function; not implemented
        raise Exception("predict_proba() functions as an abstract function and cannot be called.")



class TreeOrdinalClassifier(BaseOrdinalClassifier):
    def __init__(self, classifier):
        super().__init__(classifier)

    # inherit fit(X, y) from base class

    def predict(self, X):
        return super().predict(X, True)

    def predict_proba(self, X):
        # Check if fit has been called
        sklearn.utils.validation.check_is_fitted(self)

        # Input validation
        X = sklearn.utils.validation.check_array(X)

        classifier_probabilities = np.zeros((X.shape[0], len(self.thresholds)))
        leaf_probabilities = np.ones((X.shape[0], len(self.classes_)))
        for i, classifier in enumerate(self.classifier_objs):
            classifier_probabilities[:,i] = classifier.predict_proba(X)[:,1]

        # far left leaf of tree:
        for i in range(self.best_split_ind+1):
            leaf_probabilities[:,0] *= (1 - classifier_probabilities[:,i])

        # left of the best split threshold:
        for i in range(1, self.best_split_ind+1):
            leaf_probabilities[:,i] *= classifier_probabilities[:,i-1]
            for j in range(i, self.best_split_ind+1):
                leaf_probabilities[:,i] *= (1 - classifier_probabilities[:,j])

        # right of the best split threshold:
        for i in range(self.best_split_ind+1, len(self.classes_)-1):
            leaf_probabilities[:,i] *= (1 - classifier_probabilities[:,i])
            for j in range(self.best_split_ind, i):
                leaf_probabilities[:,i] *= classifier_probabilities[:,j]

        # for right leaf of the tree:
        for i in range(self.best_split_ind, len(self.classes_)-1):
            leaf_probabilities[:,-1] *= classifier_probabilities[:,i]

        # normalize probabilities
        leaf_probabilities = sklearn.preprocessing.normalize(leaf_probabilities, 'l1')

        return leaf_probabilities


class SubtractionOrdinalClassifier(BaseOrdinalClassifier):
    def __init__(self, classifier):
        super().__init__(classifier)

    # inherit fit(X, y) from base class

    def predict(self, X):
        return super().predict(X, True)

    def predict_proba(self, X):
        # Check if fit has been called
        sklearn.utils.validation.check_is_fitted(self)

        # Input validation
        X = sklearn.utils.validation.check_array(X)

        # option F: use predict_proba() to find individual probabilities (i.e. P(X=3) = P(X>2) - P(X>3)) after applying a monotonic constraint
        classifier_probabilities = np.zeros((X.shape[0], len(self.thresholds)))
        for i, classifier in enumerate(self.classifier_objs):
            classifier_probabilities[:,i] = classifier.predict_proba(X)[:,1]

        # apply monotonic constraint:
        classifier_probabilities[:,self.best_split_ind:] = np.minimum.accumulate(classifier_probabilities[:,self.best_split_ind:], axis=1)
        classifier_probabilities[:,:self.best_split_ind+1] = np.flip(np.maximum.accumulate(np.flip(classifier_probabilities[:,:self.best_split_ind+1], axis=1), axis=1), axis=1)

        probabilities = np.zeros((X.shape[0], len(self.classes_)))
        probabilities[:,0] = 1 - classifier_probabilities[:,0]
        probabilities[:,-1] = classifier_probabilities[:,-1]
        probabilities[:,1:-1] = classifier_probabilities[:,:-1] - classifier_probabilities[:,1:]

        # for sample_ind in range(probabilities.shape[0]):
        #   probabilities[sample_ind,:] /= probabilities[sample_ind,:] # normalize

        assert((probabilities < -1e-8).sum() == 0)
        # assert(not np.isnan(probabilities).any())
        return probabilities



## Related helper functions:


# sklearn documentation: "Note that in binary classification, recall of the positive class is also known as “sensitivity”; recall of the negative class is “specificity”."
def print_classification_report(true, prediction, weights=None):
  true, prediction = np.array(true), np.array(prediction)
  # NOTE: ONLY THE AVERAGE METRIC IS WEIGHTED
  stats = sklearn.metrics.classification_report(true, prediction, output_dict=True)
  print(f"""F1 score: {sklearn.metrics.f1_score(true, prediction)}
Sensitivity: {stats['True']['recall']}
Specificity: {stats['False']['recall']}
Positive predictive value: {stats['True']['precision']}
Negative predictive value: {stats['False']['precision']}""")
  # print("print(true, prediction):")
  # print(true, prediction)
  # print(true==prediction)
  print("Accuracy (unweighted):", np.mean(true==prediction))
  if weights is not None: print(f"Accuracy (weighted): {np.average((true==prediction).astype(int), weights=weights)}\n")
  else: print(f"Accuracy (weighted by 0/1 class): {0.5*np.average(true[true==1]==prediction[true==1]) + 0.5*np.average(true[true==0]==prediction[true==0])}\n")


def regression_accuracy(true, min_class, max_class, print_=True, allowable_error=0):
  # allowable_error can be a list of errors to check [only useful when print_=True]
  # currently assumes that adjacent classes are 1 apart
  true = copy.deepcopy(true)
  predictions = copy.deepcopy(predictions)

  predictions[predictions < min_class] = min_class
  predictions[predictions > max_class] = max_class

  try:
    for i in allowable_error:
      regression_accuracy(true, predictions, i, mrs90=False)
  except:
    # accuracy plus or minus within 'error' number of mRS-90
    sub = np.abs(true - np.round(predictions))
    accuracy = np.mean(sub <= allowable_error)
    if print_: print(f"regression accuracy (+/-{allowable_error}):", accuracy)
    return accuracy

def find_best_F1(y_true, y_score, print_=False):
  # note: applies nanmax to the scores

  if print_: print("AUC:", sklearn.metrics.roc_auc_score(y_true, y_score))
  precisions, recalls, thresholds = sklearn.metrics.precision_recall_curve(y_true, y_score)
  f1_scores = 2*precisions*recalls/(precisions+recalls)
  best_F1 = np.nanmax(f1_scores)
  best_F1_threshold = thresholds[np.nanargmax(f1_scores)]
  if print:
    print(f"Best F1 score: {best_F1}; threshold: {best_F1_threshold}")
    print_classification_report(y_true, y_score>=best_F1_threshold)
  else: return best_F1, best_F1_threshold