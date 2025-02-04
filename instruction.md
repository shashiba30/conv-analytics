1. Install docker 
2. Install clickhouse using docker using following commands
   1. `code` docker pull clickhouse/clickhouse-server
   2. `code` docker run -d  --name clickhouse-server -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server
3. To check database run the following command 
   1. `code` docker exec -it clickhouse-server clickhouse-client
4.  Install Python 3.11
5.  Create virtual environment using `code` python -m venv test_hack 
6.  Activate virtual envrionment `code` test_hack\Scripts\activate  in windows search for similar command for your os
7.  Once Virtual envrionment is activate `code` Run the command pip install -r requirements.txt to install all required packages
8.  git clone the repo and change directory using command cd hackthon-kmart-team-innovators
9.  Once it is done execute code streamlit run  

### dataset download page https://archive.ics.uci.edu/dataset/352/online+retail