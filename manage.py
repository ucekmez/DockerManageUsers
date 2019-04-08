import os, sys
from multiprocessing import Pool

# sys[1] : usernames seperated by comma. ex: ugur,umut,mehmet
# sys[2] : command. options: create / kill / remove / command
# sys[3:] : if you use command as sys[2], all remainings are the command that will be executed

users = sys.argv[1].split(",")
proxy = "http://194.138.0.5:9400"
image = "ubuntu"
try:
    F = " ".join(sys.argv[3:])
except:
    F = ""

# create containers
def create_containers(username):
    os.system("docker run -it -d --network host -v /home/{}:/workspace -v /var/run/docker.sock:/var/run/docker.sock -e http_proxy={} -e https_proxy={} --name {}_{} {}".format(username, proxy, proxy, username, image, image))


# kill containers
def kill_containers(username):
    os.system("docker kill {}_{}".format(username, image))

# rm containers
def remove_containers(username):
    os.system("docker rm {}_{}".format(username, image))

# send command to containers
def command(username):
    os.system("docker exec -it {}_{} bash -c \"{}\"".format(username, image, F))

# commit containers
def commit_containers(username):
    os.system("docker commit {}_{} {}_{}".format(username, image, username, image))

try:
    p = Pool(processes=16)
    if sys.argv[2] == "create":
        result = p.map(create_containers, users)
    elif sys.argv[2] == "kill":
        result = p.map(kill_containers, users)
    elif sys.argv[2] == "remove":
        result = p.map(remove_containers, users)
    elif sys.argv[2] == "commit":
        result = p.map(commit_containers, users)
    elif sys.argv[2] == "command":
        try:
            F = " ".join(sys.argv[3:])
            print("command: {}".format(F))
            result = p.map(command, users)
        except Exception as e:
            print("something is wrong with your commands")
            print (e)
    else:
        print ("2nd argument should be one of the pre-defined commands")
except Exception as e:
    print("something is wrong with your parameters..!")
    print (e)
