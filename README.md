# Dimensional Gate Scripts 
 
Scripts that make life easier in automation and benchmarking 
- Plots 
- Test automation 
- Forwarding controller component
- Shell scripts
    - Launch controller
    - Update script of git branches

## Test automation
A messenger sends commands from the mininet VM to the other VMs so that they
execute and tear down the controller processes 
The test bed contains at least 2 VMs both of which are mininet VMs. The first
VM's purpose is to run mininet only, the other VMs run the controller
only. The test and automation scripts will handle that for you. So mainly, all 
what you need is to run the test scripts. 
 
To run the tests the simple wat 
1) launch `sync-to-vm.sh` in both the mininet VM and the other VM 
2) launch `test_automation/messenger/command_receiver/message_receiver.py` in
the controller VM 
3) launch `test_automation/test_one_controller.py` in the network VM 

## Adding custom dissector
I'm not using default wireshark ports, I edited the OF dissector for `Wireshark` a little bit
to display correct results, use the edited dissector

<<<<<<< HEAD
## No internet access on VMs
Edit `/etc/resolvconf/resolv.conf.d/base` to contain:
=======
## Config File sample
The `config.json` file placed in the `tests` directory must have the following format (replaces all `x`s with your values)
>>>>>>> boilerplate

```JSON
{
  "network_ip": "x.x.x.x",
  "proxy_port": "x",
  "cont_main_ip": "x.x.x.x",
  "cont_repl_ip": "x.x.x.x",
  "proxy_ip": "x.x.x.x"
}
```

## No internet access on VMs
Edit `/etc/resolvconf/resolv.conf.d/base` to contain:

```
nameserver 8.8.8.8
nameserver 8.8.8.4
```
<<<<<<< HEAD
=======

## Config File sample
The `config.json` file placed in the `tests` directory must have the following format (replaces all `x`s with your values)

```JSON
{
  "proxy_port": "x",
  "proxy_ip": "x.x.x.x"
}
```
>>>>>>> boilerplate
