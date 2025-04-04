To setup on a new device
Steps: 
1. Clone the repo, 
``` git clone https://github.com/heyush007/Hardware2-Assignments ```
2. Enter the directory as
``` cd Hardware2-Assignments ```
``` cd pico-test ```
3. Initialize the Submodule, since it consists of all the required libraries
``` git submodule init ```
4. Now update the submodule for the updated code in that specific submodule repo
``` git submodule update --init ```
5. To install mpremote, a Virtual Environment needs to be created. 
``` python3 -m venv myenv ``` or ``` python -m venv myenv ```
6. Now activate the venv 
``` source myenv/bin/activate   ```
7. Now install the mpremote
``` pip install mpremote  ```
8. Lastly, install all the libraries present in the submodule 
for Mac: ``` ./install.sh ```
for Windows: ``` ```
