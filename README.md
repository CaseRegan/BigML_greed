# BigML_greed
Repo for my application project for BigML

### Setup:
Declare environment variables such that the api has authentication ([tutorial here](https://bigml.com/api/quick_start#qs_authentication)).

If you don't have a model which you expect to perform well on this problem, create one.

### How to use this project:
Read the comments on lines 139 and 159. Follow their instructions to choose what functions you want the program to perform when you run it.

To use the first function (comparing an optimal move to a bot-determined move), comment out the block quotes and set BEST_MODEL to the api identifier of the model you want to test.

To use the second function (generating data for teaching a bot), comment out the block quotes and edit F_NAME and NUM_ITER to choose where your data should be outputted and how many rows there should be respectively.
