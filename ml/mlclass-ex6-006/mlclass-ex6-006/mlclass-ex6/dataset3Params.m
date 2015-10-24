function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%
dim = 8;
i = zeros(1,dim);
error_matrix = zeros(dim);

for d = 1:dim
    if d==1
        i(d) = 0.01;
    elseif rem(d,2)==0
        i(d) = i(d-1)*3;
    else
        i(d) = i(d-2)*10;
    end
end

for j = 1:length(i)
    C = i(j);
    for k = 1:length(i)
        sigma = i(k);
        fprintf('C: %f,  sigma: %f \n',C,sigma);
        model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma)); 
        error_matrix(j,k) = mean(double(svmPredict(model, Xval) ~= yval));
    end
end
[a,b] = find (error_matrix ==min(error_matrix(:)));
C = i(a(1));
sigma = i(b(1));

% =========================================================================

end
