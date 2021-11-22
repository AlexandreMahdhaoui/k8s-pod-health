ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

$INSTALL_SCRIPT = <<-EOF
mv /tmp/test $HOME

cd /tmp
#### Prereq
yum update -y
yum install -y epel-release
yum install -y yum-utils

#### Install python 3.9 & python-pip
yum groupinstall "Development Tools" -y
yum install openssl-devel libffi-devel bzip2-devel -y
yum install wget -y
wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
tar xvf Python-3.9.7.tgz
cd Python-3.9*/
./configure --enable-optimizations
make altinstall
python3.9 -m pip install --upgrade pip

#### Docker install:
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
systemctl start docker

#### Kind install:
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind
export PATH=$PATH:/usr/local/bin
kind create cluster

#### kubectl install:
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl

#### Install pipenv & run main.py:
cd $HOME/test
python3.9 -m pip install pipenv
python3.9 -m pipenv install
python3.9 -m pipenv run python main.py

#### Run the webservice on port 80
python3.9 -m pipenv run uvicorn main:app --host 0.0.0.0 --port 80
EOF

Vagrant.configure("2") do |config|
  config.vm.provider "virtualbox" do |v|
     v.customize ["modifyvm", :id, "--memory", "2048"]
     v.customize ["modifyvm", :id, "--cpus", "2"]
  end
  config.vm.define "test" do |config|
  config.vm.hostname = "test"
  config.vm.network "public_network",ip: "10.10.10.21"
  config.vm.box = "centos/7"
  #config.vm.box = "ubuntu/trusty64"
  config.vm.post_up_message = "VM test Ok"

  config.vm.provision "file", source:".", destination: "/tmp/test"
  config.vm.provision "shell", inline: $INSTALL_SCRIPT
  end
end




