# Installation

1. **Install [VirtualBox](https://www.virtualbox.org)**
2. **Install [Vagrant](https://docs.vagrantup.com/v2/installation/)**
3. **Install [Python](https://www.python.org/downloads/)**
4. **Install [Ansible](http://docs.ansible.com/ansible/ Ansible)**
  - Ubuntu/Debian: $ sudo apt-get install ansible
  - RH/CentOS: $ sudo yum install ansible
  - MacOSX: $ sudo pip install ansible
  - More [installing info](http://docs.ansible.com/ansible/intro_installation.html)
5. **Clone this repo to your prefered route in the local fs (ej: ~/git/)** 
  - Create dir

     ``$ mkdir ~/git``

  - Change to dir 

     ``$ cd ~/git``

  - Git clone 

     ``$ git clone https://github.com/eloyacosta/automate-example.git``

6. **Change to project dir**

     ``$ cd automate-example``

7. **Exec command:**

     ``$ vagrant up``

8. **You are all set!**

  **Note:** For further executions, if something goes wrong or if you just want to provision the machine again, you have to exec:
  
  - To boot the machine (if it's donw)
 
     ``$ vagrant up``

  - To provision the machine
 
     ``$ vagrant provision`` 

# Some request testing

  **Note:** Vagrant will run the virtual server using the IP address **192.168.100.2**

1. **You can try to post some data using CURL**

     ``curl -X POST http://192.168.100.2:8080/ep1 -H "Accept: application/json" -H "Content-Type: application/json" -d '[{"date": "2015-11-20T14:48:00.451765", "uid": "3", "name": "Perry Manson", "md5checksum": "2ebf36e266bae03f4f7c312d9c82a052"},{"date": "2015-11-20T14:50:00.451766", "uid": "4", "name": "Eloy Acosta", "md5checksum": "c193dab16230b3ef1eafc64570cff69e"},{"date": "2015-11-19T10:20:00.451770", "uid": "1", "name": "DataRobot user", "md5checksum": "8949b7957f976a5f0f4e8e88316f3cc6"},{"date": "2015-11-20T14:53:00.451768", "uid": "4", "name": "Eloy Acosta", "md5checksum": "6067ce211d11fc938e5ad835d82412b1"},{"date": "2015-11-20T12:00:00.451769", "uid": "3", "name": "Perry Manson", "md5checksum": "987ae0f34facc13a5b38434b5293a9e5"},{"date": "2015-11-19T10:20:00.451770", "uid": "1", "name": "DataRobot user", "md5checksum": "8949b7957f976a5f0f4e8e88316f3cc6"}]'``

2. **You can query the API**

     ``$ curl -i -X GET "http://192.168.100.2:8080/ep2?uid=1&date=2015-11-19"``

# Unit Tests 

  All the app tests has been written with [Unittest](https://docs.python.org/2/library/unittest.html).
  To run the tests, be sure you are still in the project directory (i.e: ~/git/automate-example) and exec:
  
  - Log in the VM

     ``$ vagrant ssh``

  - Change to the app deployment dir

     ``$ cd /home/www/``

  - Run the tests

     ``$ python test.py``
