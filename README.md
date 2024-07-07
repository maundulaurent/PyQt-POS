
A modularized Point of Sale System, designed using PyQt python GUI.

This an image of the products page in the system. 
![linkedin pos](https://github.com/maundulaurent/PyQt-POS/assets/79078172/3e8fd512-1884-40be-81c4-21c93d6e421d)


There A bunch of other pages and functionalities, most are still being developed.
Much will be posted here after the system has developed. 
Feel free and welcome to collaborate and pull request.


to run designer, use this command
pyqt5-tools designer
pyuic5
pyuic5 -x file_name.ui -o test.py


<!-- Delete this after -->


In this products class, I want you to show me where to change, I want you, in the add productdialog, add another entry, the low_stock_limit into the database, when a new product is being added.
2. In the display board of the products, add another column maybe, that has "add stock". This just inputs a number, an integer only. It cannot accepts any oother type. That number shows tthe number of items in the same product that has been added. So take after clicking ok, take that number, and add into the existing stock level