Snake Game!

This was a simple project two friends and I made for a school project

As the title says, we built a version of snake game using mainly the tkinter module of python, along with supplementary modules including mysql-connector, datetime, and more!

The scores are stored in a database created by the database_creation.py file. The password for the mysql shell is given as "bvme", but it can be edited to your password if needed.

The scores can be:
                    1. Shown either from highest to lowest or latest to earliest
                    2. Exported to a .csv file
                    3. Deleted

The program was designed to be run only on Windows (although we may add support for Linux in the future).

PRE-REQUISITES:
                1. MySQL should be installed and configured such that root password is 'bvme' (Unless you were to                       change it inside the database_creation.py file)
                2. MySQL-connector should be installed on the system
                3. Python should be installed (any version after version 3 should do)

How to Run the Game:
                1. Run database_creation.py, once it is done you need not run it again.
                2. Run SnakeGame.py every time you want to run the game.
                

Have fun setting scores on SnakeGame!
