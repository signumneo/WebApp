Folder components: 

1.) app.py - Main Python Application that can be deployed locally. This application renders templates stored in the templates folder and performs additional operations on the data stored in the Data Files folder. 

2.) templates - This folder contains the code for the interfaces the users will interact with. The CSS and JavaScript required to render the templates is embedded in the HTML files so there's no need to specify another path for the CSS code. However, the images need to be rendered from the static folder and hence the path should appropriately be specified. 

3.) local databases - This folder contains the local database files and can be modified according to the needs of the task. 

4.) static - This folder contains the images required to render the templates properly. 

5.) publish_data.py - This Python file contains code to mimic the role of a publisher. The app.py file has a subscriber route defined and is monitoring an endpoint URL at all times of execution. If the users need to test this subscriber route at any time, this python file would be useful. 

