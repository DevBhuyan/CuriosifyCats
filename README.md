# CuriosifyML Category Recommendation Algorithm and API

The API is hosted on PythonAnywhere as [CuriosifyCats](https://curiosifycats.pythonanywhere.com)

To see a list of available categories, use: [`https://curiosifycats.pythonanywhere.com/view_cats`](https://curiosifycats.pythonanywhere.com/view_cats)
This will return the list of categories available and their corresponding numbers, these numbers you'd be using to denote different categories (Haven't kept string comparison as its prone to errors).

To choose any number of categories, you will need to know the "numbers" corresponding to each category, then use the numbers to build a query like: `https://curiosifycats.pythonanywhere.com/user_api?cats=1%202%203%204%205`
Here, the part up to the Question mark remains constant, that is the user_api's address. After the question mark, you need to supply `'cats=some numbers'` where the numbers will correspond to the categories the user have chosen. In the above URL, the `%20` represents a space. So the categories chosen in this example URL are `1, 2, 3, 4, 5`. The API will return the `json` file for the corresponding recommended categories.

To test the API, or see an example of its working, you can use: [`https://curiosifycats.pythonanywhere.com/test`](https://curiosifycats.pythonanywhere.com/test)
