# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

	config.vm.define "bftides" do |bftides|
		bftides.vm.box = "ubuntu/trusty64"
		bftides.vm.hostname = "bf-tideprediction.dev"
		bftides.vm.provision :shell, path: "vagrant/vagrant-bootstrap.sh"
		bftides.vm.network "forwarded_port", guest: 80, host: 8081
		bftides.vm.provider "virtualbox" do |vb|
	      vb.customize [
	      	"modifyvm", :id,
	      	"--natdnshostresolver1", "on",
	      	"--memory", "2048"
	      ]
		end
	end
	
end
