Vagrant.configure("2") do |config|
  config.vm.provider "virtualbox" do |vb|
    vb.default_nic_type = "Am79C973"
    vb.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
    vb.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]
  end

  config.vm.boot_timeout = 600
  config.ssh.insert_key = true
  config.vm.box = "bento/ubuntu-26.04"
end
