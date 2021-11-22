ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

$INSTALL_SCRIPT = <<-EOF
#### Docker install:
yum upgrade -y
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io
systemctl start docker

#### Kind install:
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind

#### kubectl install:
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl

#### Install pipenv & run main.py:
cd $HOME/test
pip install pipenv
pipenv install
pipenv run python -m main
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
  config.vm.post_up_message = "VM test Ok"

  config.vm.provision "file", source: ".", destination: "$HOME/test/"
  config.vm.provision "shell", inline: $INSTALL_SCRIPT
  end
end




